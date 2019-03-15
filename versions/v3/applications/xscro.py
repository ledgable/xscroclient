
from operator import itemgetter

from modules.applicationmanager import *
from modules.daoobject import *
from modules.tree import *
from modules.websocket import *

class WalletContainer(BaseClass):

	uid_ = None
	transactions_ = None
	tokens_ = None
	digest_ = None
	balance_ = 0.0
	
	
	@property
	def transactions(self):
		
		return self.transactions_
	
	
	@property
	def uid(self):
		
		return self.uid_
	
	
	@property
	def digest(self):
		
		return self.digest_
	
	
	@property
	def balance(self):
		
		if (self.balance_ == 0.0):
		
			balance_ = 0.0
			
			for transaction_ in self.transactions_:
				if (transaction_.id_recipient == self.uid_):
					balance_ += transaction_.volume
				
				else:
					balance_ += -transaction_.volume
		
			self.balance_ = balance_
	
		return self.balance_

	
	@property
	def marketcap(self):
	
		value_ = 0.0
	
		for transaction_ in self.transactions_:
			if (transaction_.id_recipient == self.uid_):
				value_ += (transaction_.volume * transaction_.token_price)
			
			else:
				value_ += -(transaction_.volume * transaction_.token_price)

		return value_

	
	def append(self, transaction=None):
		
		if (transaction == None):
			return
	
		self.balance_ = 0.0
		
		self.tokens_.append(transaction.uid)
		self.transactions_.append(transaction)

	
	def findWithParent(self, uid):
	
		out_ = []
	
		if (len(self.transactions_) > 0):
		
			for transaction_ in self.transactions_:
				if (transaction_.id_parent == uid):
					out_.append(transaction_)
	
		return out_


	def getTransactionForTransactionId(self, uid):

		for transaction_ in self.transactions_:
			if (transaction_.id_transaction == uid):
				return transaction_

		return None
			
		
	def getTransactionForUid(self, uid):
	
		if (uid in self.tokens_):
			for transaction_ in self.transactions_:
				if (transaction_.uid == uid):
					return transaction_

		return None

	
	def __init__(self, uid):
		
		self.uid_ = uid
		self.digest_ = None
		self.tokens_ = []
		self.transactions_ = []


class WalletManager(BaseClass):

	uid_ = None
	wallets_ = None
	pending_ = None
	
	
	@property
	def wallets(self):
		
		return self.wallets_

	
	@property
	def pending(self):
	
		return self.pending_
	
	
	@property
	def uid(self):
		
		return self.uid_
	
	
	def find(self, uid):
	
		if (uid == None):
			return None
	
		walletids_ = list(self.wallets_.keys())
	
		if (len(walletids_) > 0):
			
			for walletid_ in walletids_:
				wallettemp_ = self.wallets_[walletid_]
				transaction_ = wallettemp_.getTransactionForUid(uid)
				
				if (transaction_ != None):
					return transaction_
	
		return None
			
			
	def findTransaction(self, idtransaction):
		
		if (idtransaction == None):
			return None
		
		# check open transactions
		
		keys_ = list(self.pending_.keys())
		
		if (len(keys_) > 0):
			for key_ in keys_:
				transaction_ = self.pending_[key_]
				
				if (transaction_ != None):
					if (transaction_.id_transaction == idtransaction):
						return transaction_
		
		# check wallets
		
		walletids_ = list(self.wallets_.keys())
		
		if (len(walletids_) > 0):
			
			for walletid_ in walletids_:
				wallettemp_ = self.wallets_[walletid_]
				transaction_ = wallettemp_.getTransactionForTransactionId(idtransaction)
				
				if (transaction_ != None):
					return transaction_
			
		return None

	
	def getChildrenOfToken(self, uid):

		out_ = []
		
		if (uid == None):
			return None
		
		walletkeys_ = list(self.wallets_.keys())

		if (len(walletkeys_) > 0):
			
			for walletkey_ in walletkeys_:
				wallet_ = self.wallets_[walletkey_]
				
				for transaction_ in wallet_.transactions_:
					
					if (transaction_.id_parent == uid):
						out_.append(transaction_)
		
		return out_

	
	@property
	def volume(self):
	
		volume_ = 0.0
		transactions_ = self.getChildrenOfToken("0")
		
		for transaction_ in transactions_:
			volume_ += transaction_.volume
	
		return volume_
	
	
	@property
	def balance(self):
	
		return 0.0
	
	
	@property
	def marketcap(self):
	
		value_ = 0.0
		walletkeys_ = list(self.wallets_.keys())
	
		if (len(walletkeys_) > 0):
		
			for walletkey_ in walletkeys_:
				wallet_ = self.wallets_[walletkey_]
				value_ += wallet_.marketcap

		return value_
			

	def walletFor(self, uid=None):

		wallet_ = None
		
		if (uid in self.wallets_.keys()):
			wallet_ = self.wallets_[uid]

		else:
			wallet_ = WalletContainer(uid)
			self.wallets_[uid] = wallet_

		return wallet_
	
	
	def append(self, transactions=None):
	
		if (transactions == None) or (len(transactions) == 0):
			return

		for transaction_ in transactions:
			
			walletto_ = None
			walletfrom_ = None
			
			walletkeys_ = list(self.wallets_.keys())
			parentid_ = transaction_.id_parent
			recipientid_ = transaction_.id_recipient

			# if destination is 0, then the token is "killed"
			
			if (recipientid_ != "0"):
				walletto_ = self.walletFor(recipientid_)
				walletto_.append(transaction_)

			# if we found a parent transaction, add the new one as we need to adjust the balance...

			if (parentid_ != "0"):
				walletfrom_ = self.walletFor(parentid_)
				walletfrom_.append(transaction_)


	def __init__(self, uid=None):

		self.uid_ = uid
		self.wallets_ = {}
		self.pending_ = {}


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
			return configctrl_.chains
		
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
			
			for transaction_ in transactions:
				
				classid_ = transaction_["$class"]
					
				if (classid_ == XSCRO_RECORDID):
						
					uid_ = transaction_.uid
					
					if (uid_ != None):
						container_.pending_[uid_] = transaction_
			
				elif (classid_ == XSCRO_AUTHID):
				
					walletid_ = transaction_.wallet
					wallet_ = container_.walletFor(walletid_)
					wallet_.digest_ = transaction_.passtoken
						
				elif (classid_ == XSCRO_ACKID):
						
					uid_ = transaction_.uid
					ack_ = int(transaction_.default("ack", 0))
					
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
	
#	def poller(self, args):
#
#		keys_ = list(self.opentransactions_.keys())
#
#		if (len(keys_) > 0):
#			topurge_ = []
#			now_ = self.epoch
#
#			for uid_ in keys_:
#				originaltransaction_ = self.opentransactions_[uid_]
#				time_ = int(originaltransaction_["$time"])
#
#				if ((time_ + ACK_TIMEOUT) < now_):
#					topurge_.append(uid_)
#
#			if (len(topurge_) > 0):
#				for uid_ in topurge_:
#					del self.opentransactions_[uid_]

	
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
		
#		self.timer_ = Repeater(60.0, self.poller, self)
#		self.timer_.start()

