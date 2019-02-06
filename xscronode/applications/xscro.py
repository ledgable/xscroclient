
from modules.daoobject import *
from modules.tree import *
from modules.websocket import *


class TokenTree(TreeNode):
	
	
	def __init__(self, uid=None, data=None, parent=None):
		TreeNode.__init__(self, uid, data, parent)

	
	@property
	def marketCap(self):
	
		cap_ = 0.0
		
		if (self.data != None):
			if (self.parent != None):
				if (self.parent.data_ != None):
					cap_ += -(self.data_.volume * self.parent.data_.token_price)
		
			cap_ += (self.data_.volume * self.data_.token_price)
	
		if (len(self.children_) > 0):
			for child_ in list(self.children_.values()):
				cap_ += child_.marketCap
	
		return cap_
	
	
	def transactionsFor(self, idperson=None):
		
		transactions_ = []

		if (idperson != None):
	
			if (self.data != None):
				if (self.data.id_recipient == idperson):
					copy_ = self.data_.copy()
					copy_.balance = self.balance
					transactions_.append(copy_)
		
			if (len(self.children_) > 0):
				for child_ in list(self.children_.values()):
					results_ = child_.transactionsFor(idperson)
					if (len(results_) > 0):
						transactions_.extend(results_)
		
		return transactions_

			
	def balanceFor(self, idperson=None):
	
		balance_ = 0
	
		if (self.data != None):
			if (self.data.id_recipient == idperson):
				balance_ += self.balance
		
		if (len(self.children_) > 0):
			for child_ in list(self.children_.values()):
				balance_ += child_.balanceFor(idperson)

		return balance_
	
	
	@property
	def volume(self):
		
		volume_ = 0
		
		if (self.data != None):
			balance_ += self.data_.volume
		
		if (len(self.children_) > 0):
			for child_ in list(self.children_.values()):
				volume_ += child_.data_.volume
	
		return volume_
		
			
	@property
	def balance(self):
		
		balance_ = 0
		
		if (self.data == None):
			
			# we are pretty much at the root !
			
			if (len(self.children_) > 0):
				
				for child_ in list(self.children_.values()):
					balance_ += child_.balance
	
		else:
			balance_ = self.data.volume

			if (len(self.children_) > 0):
				toremove_ = 0
				
				for child_ in list(self.children_.values()):
					toremove_ += child_.data.volume
				
				balance_ += -toremove_

		return balance_


class XscroApplication(BaseClass, metaclass=Singleton):
	
	trees_ = None
	websocket_ = None
	datapoints_ = None
	stats_ = None
	appInstance_ = None
	opentransactions_ = None
	
	
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
	def trees(self):
		return self.trees_

	
	@property
	def stats(self):
		return self.stats_

	
	@property
	def datapoints(self):
		return self.datapoints_

	
	@property
	def opentransactions(self):
		return self.opentransactions_
	
	
	@property
	def chains(self):
		
		configctrl_ = ApplicationManager().get("config")
		
		if (configctrl_ != None):
			return configctrl_.chains
		
		return None
	
	
	def calculateStats(self, chainid=None):
	
		if (chainid in self.trees_.keys()):
			
			stats_ = None
			tree_ = self.trees_[chainid]

			if (tree_ != None):
				
				oldmarketppt_ = 0.0

				if (chainid in self.stats_.keys()):
					stats_ = self.stats_[chainid]
					oldmarketppt_ = stats_.default("marketppt", 0.0)
				else:
					stats_ = extdict({})
				
				balance_ = tree_.balance
				volume_ = tree_.volume
				allocated_ = volume_ - balance_
				cap_ = tree_.marketCap
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
		tree_ = None
		datapoints_ = None
		
		if (chainid_ in self.datapoints_.keys()):
			datapoints_ = self.datapoints_[chainid_]
		
		else:
			datapoints_ = extlist([])
			self.datapoints_[chainid_] = datapoints_
		
		if (chainid_ in self.trees_.keys()):
			tree_ = self.trees_[chainid_]

		else:
			tree_ = TokenTree()
			self.trees_[chainid_] = tree_

		if (tree_ != None):
			
			xscroTransactions_ = []
			
			for transaction_ in transactions:
				
				classid_ = transaction_["$class"]
					
				if (classid_ == XSCRO_RECORDID):
						
					uid_ = transaction_.uid
						
					if (uid_ != None):
						self.opentransactions_[uid_] = transaction_
				
				elif (classid_ == XSCRO_ACKID):
						
					uid_ = transaction_["uid"]
					ack_ = int(transaction_.default("ack", 0))
						
					if (uid_ in self.opentransactions_.keys()):
							
						# remove the transaction from the wait queue...
							
						originaltransaction_ = self.opentransactions_[uid_]
						del self.opentransactions_[uid_]
							
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
				
				tree_.append(xscroTransactions_)
				
				self.calculateStats(chainid_)
				self.sendToSocketListeners(dict({"transactions":xscroTransactions_, "target":{"domain":"Xscro.Notify", "event":"processTransactions"}}))


	def notificationTransactionsReceived(self, caller, object):
	
		self.transactionsReceived(caller, object)

	
	def notificationChainInitialized(self, caller, object):
		
		chainid_ = caller.uid_
		
	
	def notificationChainReset(self, caller, object):

		chainid_ = caller.uid_

		# basically we need to dump the tree asscicated and then reload...
		self.trees_[chainid_] = TokenTree()
	
	
	def notificationChainLoaded(self, caller, object):

		chainid_ = caller.uid_

		# chain loaded at this point - should have a propogated tree or something wrong occurred
	
	def poller(self, args):
		
		keys_ = list(self.opentransactions_.keys())
		
		if (len(keys_) > 0):
			topurge_ = []
			now_ = self.epoch
			
			for uid_ in keys_:
				originaltransaction_ = self.opentransactions_[uid_]
				time_ = int(originaltransaction_["$time"])
				
				if ((time_ + ACK_TIMEOUT) < now_):
					topurge_.append(uid_)
		
			if (len(topurge_) > 0):
				for uid_ in topurge_:
					del self.opentransactions_[uid_]
	
	
	def shutdown(self):
	
		self.timer_.stop()
	
	
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
		
		self.opentransactions_ = {}
		self.datapoints_ = {}
		self.stats_ = {}
		self.trees_ = {}
		
		NotificationCenter().addObserver(NOTIFY_CHAIN_RESET, self.notificationChainReset)
		NotificationCenter().addObserver(NOTIFY_CHAIN_INITIALIZED, self.notificationChainInitialized)
		NotificationCenter().addObserver(NOTIFY_CHAIN_LOADED, self.notificationChainLoaded)
		NotificationCenter().addObserver(NOTIFY_CHAIN_TRANSACTIONS, self.notificationTransactionsReceived)
		
		self.timer_ = Repeater(60.0, self.poller, self)
		self.timer_.start()

