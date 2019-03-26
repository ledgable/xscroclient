
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
				
				if (walletkey_ != uid):
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
	
		volume_ = 0.0
		
		transactions_ = self.getChildrenOfToken("0")
		walletids_ = []
		
		for transaction_ in transactions_:
			if (transaction_.id_recipient not in walletids_):
				walletids_.append(transaction_.id_recipient)
	
		for walletid_ in walletids_:
			wallet_ = self.wallets_[walletid_]
			volume_ += wallet_.balance
		
		return volume_
	
	
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

