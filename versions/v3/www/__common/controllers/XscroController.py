
from www.__common.controllers.NodeController import *

from modules.applicationmanager import *

RECIPIENT_ETHER = "0"
STATUS_FAIL = 0
STATUS_OK = 1

class XscroController(NodeController):
	
	
	def __init__(self, handler, session, query=None, isajax=False):
		
		NodeController.__init__(self, handler, session, query, isajax)
	
	# Create a new token from the ether (parent address = 0)
	
	def mintNewToken(self, chainid, parentid=RECIPIENT_ETHER, recipientid=None, transid=None, volume=0.0, price=0.0, additional="Token Minted", ipaddress="0.0.0.0", traderid=None):
		
		chainid_ = chainid
		
		if (chainid_ != None):
			
			chainid_ = chainid_.lower()
		
			if (recipientid in ["", RECIPIENT_ETHER]):
				return False, None, "Recipient invalid"
			
			volume_ = float(volume)
			if (volume_ < 0):
				return False, None, "Volume invalid - must be > 0"

			price_ = float(price)
			if (price_ < 0):
				return False, None, "Price invalid - must be >= 0"

			newcoin_ = extdict()
			newcoin_["$class"] = XSCRO_RECORDID
			
			uid_ = self.randomCode(50, (string.ascii_letters + string.digits))
		
			setattrs(newcoin_,
				uid = uid_,
				id_parent = parentid,
				id_transaction = transid,
				ip_address = ipaddress,
				id_recipient = recipientid,
				id_trader = traderid,
				token_price = price_,
				volume = volume_,
				additional = additional
				)
			
			shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newcoin_])
			
			return True, uid_, "ok"

		return False, None, "Chain Invalid"

	# Transfer a token into the ether (address = 0) effectively destorying it

	def destroyValue(self, chainid, walletid, transid=None, volume=0.0, additional="Token Destroyed", ipaddress="0.0.0.0", traderid=None):

		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid_.lower()
		
			xscro_ = ApplicationManager().get("xscro")
			msg_ = "Unknown error"
			
			if (xscro_ != None):

				if (chainid_ in xscro_.containers.keys()):
					
					# get the account tree for the chain requested
					container_ = xscro_.containers[chainid_]
				
					# find the token in the sequence
					wallet_ = container_.wallets[walletid]
					
					if (wallet_ != None):
						
						balance_ = wallet_.balance
						volume_ = float(volume)
						
						if (volume_ < 0):
							return False, None, "Volume invalid - must be > 0"
				
						if (volume_ == 0):
							volume_ = balance_
					
						if (balance_ == 0):
							return False, None, "Token has no balance"
					
						if (balance_ >= volume_):
							
							# we push a transaction into the chain with the new information !

							newcoin_ = extdict()
							newcoin_["$class"] = XSCRO_RECORDID
							
							uid_ = self.randomCode(50, (string.ascii_letters + string.digits))

							setattrs(newcoin_,
								uid = uid_,
								id_parent = walletid,
								id_transaction = transid,
								ip_address = ipaddress,
								id_recipient = RECIPIENT_ETHER,
								id_trader = traderid,
								token_price = 0,
								volume = volume_,
								additional = additional
								)

							shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newcoin_])
						
							return True, uid_, "ok"
						
						else:
							msg_ = "Insufficient balance"
			
					else:
						msg_ = "No such token"
			
				else:
					msg_ = "Chain invalid"
							
		return False, None, msg_

	# Get token
	
	def getToken(self, chainid, tokenid):
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
			xscro_ = ApplicationManager().get("xscro")
			
			if (xscro_ != None):
				
				if (chainid_ in xscro_.containers.keys()):
					
					# get the account tree for the chain requested
					container_ = xscro_.containers[chainid_]
					
					# find the token in the sequence
					token_ = container_.find(tokenid)
					
					if (token_ != None):
						return token_

		return None
	
	# Transfer a token to another
			
	def transferValue(self, chainid, senderid, recipientid, transid=None, volume=0.0, price=0.0, additional="Token Transferred", ipaddress="0.0.0.0", traderid=None):
	
		msg_ = "Unknown error"
		xscro_ = ApplicationManager().get("xscro")

		if (chainid != None):
			
			chainid_ = chainid.lower()

			if (chainid_ in xscro_.containers.keys()):
			
				container_ = xscro_.containers[chainid_]
				wallet_ = container_.walletFor(senderid)
				
				# if volume or price is < 0 then abort
				
				volume_ = float(volume)
				if (volume_ < 0):
					return False, None, "Volume invalid - must be > 0"
			
				price_ = float(price)
				if (price_ < 0):
					return False, None, "Price invalid - must be >= 0"
				
				balance_ = wallet_.balance

				if (balance_ < volume_):
				
					msg_ = "Insufficient balance"

				else:
					
					# we push a transaction into the chain with the new information !

					newcoin_ = extdict()
					newcoin_["$class"] = XSCRO_RECORDID

					uid_ = None
					
					# need to check the token is unique...
					
					while (True):
						uid_ = self.randomCode(50, (string.ascii_letters + string.digits))
						oldtoken_ = container_.find(uid_)
						if (oldtoken_ == None):
							break
					
					setattrs(newcoin_,
						uid = uid_,
						id_parent = senderid,
						id_transaction = transid,
						ip_address = ipaddress,
						id_recipient = recipientid,
						id_trader = traderid,
						token_price = price_,
						volume = volume_,
						additional = additional
						)

					shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newcoin_])

					return True, uid_, "ok"

		else:
			msg_ = "No such token"
		
		return False, None, msg_

	# Create a new wallet

	def createWallet(self, chainid, walletid, digest):
	
		chains_ = self.chains()
		
		if (chainid != None):
			
			chainid_ = chainid.lower()
	
			if (chainid_ in chains_):
				xscro_ = ApplicationManager().get("xscro")

				if (xscro_ != None):
					
					container_ = xscro_.containers[chainid_]
					walletids_ = list(container_.wallets.keys())
					
					if (walletid not in walletids_):
					
						newauth_ = extdict()
						newauth_["$class"] = XSCRO_AUTHID
						
						# we encrypt the passcode so even we dont know it !!
						nonce_ = ("%s:%s:%s" % (chainid_, digest, walletid))

						kpt1_ = hashlib.md5()
						kpt1_.update(nonce_.encode(UTF8))
						kpt1out_ = kpt1_.hexdigest()
						
						setattrs(newauth_,
							wallet = walletid,
							passtoken = kpt1out_
							)
							
						shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newauth_])

						return {"walletid":walletid, "status":STATUS_OK}
						
		return None

	# Authenticate a request
			
	def authenticate(self, chainid, walletid, password):
	
		chains_ = self.chains()
		token_ = None
		success_ = False
	
		if (password != None):
			chainid_ = chainid.lower()
			
			if (chainid_ in chains_):
				xscro_ = ApplicationManager().get("xscro")

				if (xscro_ != None):
					
					if (chainid_ in xscro_.containers.keys()):
					
						container_ = xscro_.containers[chainid_]
						walletids_ = list(container_.wallets.keys())
						
						# do not use walletfor otherwise it is created and we get alot of crap...
						if (walletid in walletids_):
							digest_ = container_.wallets[walletid].digest
							nonce_ = ("%s:%s:%s" % (chainid, password, walletid))
							kpt1_ = hashlib.md5()
							kpt1_.update(nonce_.encode(UTF8))
							kpt1out_ = kpt1_.hexdigest()
							
							success_ = (kpt1out_ == digest_)
							if (success_):
								token_ = digest_
	
		return success_, token_
			
	# Change Password for a user

	def changePassword(self, chainid, walletid, digest, token):
	
		chains_ = self.chains()
		
		if (chainid != None):
			
			chainid_ = chainid.lower()
			
			if (chainid_ in chains_):

				# we encrypt the passcode so even we dont know it !!
				nonce_ = ("%s:%s:%s" % (chainid_, digest, walletid))
				
				kpt1_ = hashlib.md5()
				kpt1_.update(nonce_.encode(UTF8))
				kpt1out_ = kpt1_.hexdigest()

				newauth_ = extdict()
				newauth_["$class"] = XSCRO_AUTHID
				writechange_ = False
				
				setattrs(newauth_,
					wallet = walletid,
					passtoken = kpt1out_
					)
				
				if (token != None):
					if (kpt1out_ == token):
						self.log("passwords are the same!")

					else:
						writechange_ = True

				else:
					writechange_ = True

				if (writechange_):
					shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newauth_])
					return {"walletid":walletid, "status":STATUS_OK}
					
		return None

	# Get Transactions For Wallet

	def allTransactions(self, chainid):

		out_ = []

		if (chainid != None):
			
			chainid_ = chainid.lower()
			xscro_ = ApplicationManager().get("xscro")
			
			if (xscro_ != None):
				
				if (chainid_ in xscro_.containers.keys()):
				
					self.log("here")

					container_ = xscro_.containers[chainid_]
					walletkeys_ = list(container_.wallets.keys())
					
					for walletkey_ in walletkeys_:
						wallet_ = container_.wallets[walletkey_]
						
						for transaction_ in wallet_.transactions_:
							if (transaction_.id_recipient == wallet_.uid):
								out_.append(transaction_)
							
		return out_

	
	def allWallets(self, chainid):
	
		out_ = []
	
		if (chainid != None):
		
			chainid_ = chainid.lower()
			xscro_ = ApplicationManager().get("xscro")
		
			if (xscro_ != None):
			
				if (chainid_ in xscro_.containers.keys()):
				
					container_ = xscro_.containers[chainid_]
					walletkeys_ = list(container_.wallets.keys())
				
					for walletkey_ in walletkeys_:
						wallet_ = container_.wallets[walletkey_]
						out_.append({"uid":walletkey_, "balance":wallet_.balance})
	
		return out_
	
	
	def allTransactionsForWallet(self, chainid, walletid):
	
		out_ = []
		
		if (chainid != None):
			
			chainid_ = chainid.lower()
			xscro_ = ApplicationManager().get("xscro")
		
			if (xscro_ != None):
			
				if (chainid_ in xscro_.containers.keys()):
					
					container_ = xscro_.containers[chainid_]
					wallet_ = container_.walletFor(walletid)
					out_ = wallet_.transactions_
	
		return out_
	
	
	def allOpenTransactionsForWallet(self, chainid, walletid):
		
		out_ = []
		
		if (chainid != None):
			
			chainid_ = chainid.lower()
			xscro_ = ApplicationManager().get("xscro")
			
			if (xscro_ != None):
				
				if (chainid_ in xscro_.containers.keys()):
					
					container_ = xscro_.containers[chainid_]
					pending_ = list(container_.pending.values())

					for transaction_ in transactions_:
						if (transaction_.id_parent == walletid):
							out_.append(transaction_)
								
		return out_

	
	# Ack Transaction
	
	def ackTransaction(self, chainid, walletid, token=None, code=0):
		
		if (chainid != None) and (token != None):
	
			chainid_ = chainid.lower()
			code_ = int(code)
			
			xscro_ = ApplicationManager().get("xscro")
	
			if (xscro_ != None):
				
				if (chainid_ in xscro_.containers.keys()):

					container_ = xscro_.containers[chainid_]
					tokens_ = list(container_.pending.keys())
					
					if (token in tokens_):
						
						transaction_ = container_.pending[token]
						
						newack_ = extdict()
						newack_["$class"] = XSCRO_ACKID

						setattrs(newack_,
							uid = token,
							ack = code_
							)
						
						if (transaction_.id_parent == RECIPIENT_ETHER):
							if (walletid == RECIPIENT_ETHER):
								shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newack_])
								return True, {"status":STATUS_OK, "chainid":chainid_, "token":token, "code":code_}
			
						# get the parent coin to the transaction - if the authenticated user owns it, allow the ack !
						else:
							if (transaction_.id_parent == walletid):
								
								if (code_ == 1):
									wallet_ = container_.walletFor(transaction_.id_parent)

									volume_ = float(transaction_.volume)
									balance_ = wallet_.balance
																		
									if (balance_ < volume_):
										newack_.ack = -1
										shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newack_])
										return False, {"status":STATUS_FAIL, "chainid":chainid_, "reason":"Insufficient balance", "code":newack_.ack}
											
								shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newack_])
								return True, {"status":STATUS_OK, "chainid":chainid_, "token":token, "code":code_}
	
		return False, None

