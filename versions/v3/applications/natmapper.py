
from .baseapplication import *

from modules import *
from modules.natpmp import *


class NatMap(BaseClass):

	
	manager_ = None
	timer_ = None
	port_ = 0
	refresh_ = 0
	ipaddress_ = None
	
	
	def refreshNat(self, args=None):
	
		self.log("Refreshing NAT for %s" % self.ipaddress_)
		gateway_ = get_gateway_addr()
		
		try:
			map_port(NATPMP_PROTOCOL_TCP, self.port_, self.port_, self.refresh_, gateway_ip=gateway_)
			
		except Exception as exception_:
			self.logException(exception_)
			self.manager_.failedWithResponse(self, "Nat failed to refresh")

				
	def shutdown(self):
	
		self.log("Natmap shutdown")
		
		self.timer_.stop()
	
	
	def __init__(self, manager, port, refreshInterval=3600):

		self.manager_ = manager
		self.port_ = port
		self.refresh_ = refreshInterval

		if (self.timer_ == None):
			self.timer_ = Repeater(self.refresh_, self.refreshNat, self)
			self.timer_.start()

		gateway_ip = get_gateway_addr()
		addr_request = PublicAddressRequest()
		addr_response = send_request_with_retry(gateway_ip, addr_request, response_data_class=PublicAddressResponse,retry=9, response_size=12)

		if (addr_response.result != 0):
			# could not get nat punch...
			self.manager_.failedWithResponse(self, "Nat failed to get response")

		else:
			self.ipaddress_ = "%s:%s" % (addr_response.ip, self.port_)
			self.refreshNat()



class NatMapper(BaseApplication):
	
	mappings_ = None

	@property
	def mappings(self):
		
		return self.mappings_
	
	
	def failedWithResponse(self, mapping, reason):
	
		self.logError("Nat failed: %s" % reason)
	
		self.removeMapping(mapping.port)
	
	
	def removeMapping(self, port=0):
	
		counter_ = 0
		port_ = int(port)
		
		for mapping_ in self.mappings_:
			if (mapping_.port == port_):
				mapping_ = self.mapping_[counter]
				mapping_.shutdown()
				del self.mapping_[counter_]
				break
					
			counter += 1
				
	
	def __init__(self, appInstance=None):

		BaseApplication.__init__(self, appInstance)
		self.mappings_ = []


	def mappingForPort(self, port):
	
		for mapping_ in self.mappings_:
			if (mapping_.port == port):
				return self.mapping_[counter_]
					
			counter += 1

		return None

	
	def addPort(self, port, refreshInterval=3600):

		port_ = int(port)
		
		if (self.mappingForPort(port_) == None):
			mapping_ = NatMap(self, port_, refreshInterval)
			self.mappings_.append(mapping_)
			

	def shutdown(self):

		for mapping_ in self.mappings_:
			mapping_.shutdown()
