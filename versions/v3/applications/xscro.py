
from operator import itemgetter

from modules.applicationmanager import *
from modules.daoobject import *
from modules.tree import *
from modules.websocket import *

from .walletmanager import *

class XscroApplication(BaseClass, metaclass=Singleton):
	
	containers_ = None
	websocket_ = None
	datapoints_ = None
	stats_ = None
	appInstance_ = None
	
	
	@property
	def appInstance(self):
		return self.appInstance_
	
	
	# websocket handlers...
	
	def new_client(self, client, server):
		
		self.log("client connected")
	
	
	def client_left(self, client, server):
		
		self.log("client left")
	
	
	def message_received(self, client, server, message):
		
		self.log("message received")
	
	
	def data_recevied(self, client, server, message):
		pass

	
	def sendToSocketListeners(self, message):
		
		from modules.customencoder import CustomEncoder
		tosend_ = json.dumps(message, cls=CustomEncoder)
		self.websocket_.send_message_to_all(tosend_)
	
	# main application engine...
	
	@property
	def containers(self):
		return self.containers_
	
	
	@property
	def stats(self):
		return self.stats_

	
	@property
	def datapoints(self):
		return self.datapoints_


	@property
	def containers(self):
		return self.containers_
	
	
	@property
	def chains(self):
		
		configctrl_ = ApplicationManager().get("config")
		
		if (configctrl_ != None):
			
			chains_ = configctrl_.chains
			out_ = []
			
			for chain_ in chains_:
				config_ = configctrl_.configForChain(chain_)
				recordtypes_ = config_.structure.keys()
				if (XSCRO_RECORDID in recordtypes_):
					out_.append(chain_)
			
			return out_
		
		return None
	
	
	def calculateStats(self, chainid=None):
	
		if (chainid in self.containers_.keys()):
			
			stats_ = None
			container_ = self.containers_[chainid]

			if (container_ != None):
				
				oldmarketppt_ = 0.0

				if (chainid in self.stats_.keys()):
					stats_ = self.stats_[chainid]
					oldmarketppt_ = stats_.default("marketppt", 0.0)
				else:
					stats_ = extdict({})
			
				volume_ = container_.volume
				balance_ = container_.balance
				cap_ = container_.marketcap
				
				allocated_ = volume_ - balance_
				marketppt_ = 0.0
				change_ = 0.0
				direction_ = "same"

				if (allocated_ > 0):
					marketppt_ = cap_ / allocated_

				if (oldmarketppt_ == 0.0):
					direction_ = "same"

				else:
					change_ = marketppt_ - oldmarketppt_

					if (oldmarketppt_ > marketppt_):
						direction_ = "down"
					
					elif (oldmarketppt_ < marketppt_):
						direction_ = "up"
						
				setattrs(stats_,
					volume = volume_,
					balance = balance_,
					allocated = allocated_,
					marketcap = cap_,
					marketppt = marketppt_,
					direction = direction_,
					change = change_
					)

				self.stats_[chainid] = stats_


	def transactionsReceived(self, chain, transactions):
		
		chainid_ = chain.uid_
		container_ = None
		datapoints_ = None
		
		if (chainid_ in self.datapoints_.keys()):
			datapoints_ = self.datapoints_[chainid_]
		
		else:
			datapoints_ = extlist([])
			self.datapoints_[chainid_] = datapoints_
		
		if (chainid_ in self.containers_.keys()):
			container_ = self.containers_[chainid_]

		else:
			container_ = WalletManager(chainid_)
			self.containers_[chainid_] = container_

		if (container_ != None):
			
			xscroTransactions_ = []
			notifySocket_ = False
			
			for transaction_ in transactions:
				
				classid_ = transaction_["$class"]
					
				if (classid_ == XSCRO_RECORDID):
						
					uid_ = transaction_.uid
					notifySocket_ = True

					if (uid_ != None):
						container_.pending_[uid_] = transaction_
			
				elif (classid_ == XSCRO_AUTHID):
				
					walletid_ = transaction_.wallet
					wallet_ = container_.walletFor(walletid_)
					wallet_.digest_ = transaction_.passtoken
					notifySocket_ = True

				elif (classid_ == XSCRO_ACKID):
						
					uid_ = transaction_.uid
					ack_ = int(transaction_.default("ack", 0))
					notifySocket_ = True

					if (uid_ in container_.pending_.keys()):
						
						# remove the transaction from the wait queue...
							
						originaltransaction_ = container_.pending_[uid_]
						del container_.pending_[uid_]
							
						if (ack_ == 1):
								
							if (originaltransaction_.id_parent == "0") or (originaltransaction_.id_recipient == "0"):
								pass # ignore - creation or destruction of coin !
						
							else:
								time_ = originaltransaction_["$time"]
								volume_ = float(originaltransaction_.volume)
								price_ = float(originaltransaction_.token_price)
								
								datapoints_.append({"time":time_, "price":price_, "volume":volume_})
							
							xscroTransactions_.append(originaltransaction_)
							
						elif (ack_ == 9):
							pass # deny transaction
		
			if (len(xscroTransactions_) > 0):
				container_.append(xscroTransactions_)
				self.calculateStats(chainid_)
				
			if (notifySocket_):
				self.sendToSocketListeners(dict({"transactions":xscroTransactions_, "target":{"domain":"Xscro.Notify", "event":"processTransactions"}}))


	def notificationTransactionsReceived(self, caller, object):
	
		self.transactionsReceived(caller, object)

	
	def notificationChainInitialized(self, caller, object):
		
		chainid_ = caller.uid_
		
	
	def notificationChainReset(self, caller, object):

		chainid_ = caller.uid_

		# basically we need to dump the tree asscicated and then reload...
		self.containers_[chainid_] = WalletManager()
	
	
	def notificationChainLoaded(self, caller, object):

		chainid_ = caller.uid_

		# chain loaded at this point - should have a propogated tree or something wrong occurred
	
	
	def shutdown(self):
	
		pass
	
	
	def __init__(self, appInstance=None):
		
		self.appInstance_ = appInstance
		
		self.log("Created instance of XSCRO application")
		
		self.websocket_ = WebsocketServer(9001, "0.0.0.0", BaseSocketClient, "cert.pem")
				
		self.websocket_.set_fn_new_client(self.new_client)
		self.websocket_.set_fn_client_left(self.client_left)
		self.websocket_.set_fn_message_received(self.message_received)
		self.websocket_.set_fn_data_received(self.data_recevied)
		
		t = threading.Thread(target=self.websocket_.run_forever, args=[])
		t.daemon = True
		t.start()

		self.datapoints_ = {}
		self.stats_ = {}
		self.containers_ = {}
		
		NotificationCenter().addObserver(NOTIFY_CHAIN_RESET, self.notificationChainReset)
		NotificationCenter().addObserver(NOTIFY_CHAIN_INITIALIZED, self.notificationChainInitialized)
		NotificationCenter().addObserver(NOTIFY_CHAIN_LOADED, self.notificationChainLoaded)
		NotificationCenter().addObserver(NOTIFY_CHAIN_TRANSACTIONS, self.notificationTransactionsReceived)

