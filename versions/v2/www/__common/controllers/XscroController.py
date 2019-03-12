
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

	def destroyToken(self, chainid, tokenid, transid=None, volume=0.0, additional="Token Destroyed", ipaddress="0.0.0.0", traderid=None):

		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid_.lower()
		
			xscro_ = ApplicationManager().get("xscro")
			msg_ = "Unknown error"
			
			if (xscro_ != None):

				if (chainid_ in xscro_.trees.keys()):
					
					# get the account tree for the chain requested
					tree_ = xscro_.trees[chainid_]
				
					# find the token in the sequence
					token_ = tree_.find(tokenid)
					
					if (token_ != None):
						
						if (token_.data.id_recipient == RECIPIENT_ETHER):
							return False, None, "Token already destroyed"

						balance_ = token_.balance
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
								id_parent = tokenid,
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
			
			if (chainid_ in xscro_.trees.keys()):
				
				# get the account tree for the chain requested
				tree_ = xscro_.trees[chainid_]
				
				# find the token in the sequence
				token_ = tree_.find(tokenid)
				
				if (token_ != None):
					return token_

		return None
	
	# Transfer a token to another
			
	def transferToken(self, chainid, tokenid, recipientid=None, transid=None, volume=0.0, price=0.0, additional="Token Transferred", ipaddress="0.0.0.0", traderid=None):
	
		msg_ = "Unknown error"

		if (chainid != None):
			chainid_ = chainid.lower()
		
			token_ = self.getToken(chainid_, tokenid)

			if (token_ != None):
				
				# if volume or price is < 0 then abort
				
				volume_ = float(volume)
				if (volume_ < 0):
					return False, None, "Volume invalid - must be > 0"
			
				price_ = float(price)
				if (price_ < 0):
					return False, None, "Price invalid - must be >= 0"

				# if token was destroyed, dont allow it to be transferred to another person
				if (token_.data.id_recipient == None) or (token_.data.id_recipient in ["", RECIPIENT_ETHER]):
					return False, None, "Token is destroyed"

				if (token_.data.id_recipient == recipientid):
					return False, None, "Recipient invalid"

				balance_ = token_.balance

				if (balance_ >= volume_):
					
					# we push a transaction into the chain with the new information !

					newcoin_ = extdict()
					newcoin_["$class"] = XSCRO_RECORDID

					uid_ = self.randomCode(50, (string.ascii_letters + string.digits))
					
					setattrs(newcoin_,
						uid = uid_,
						id_parent = tokenid,
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
					msg_ = "Insufficient balance"

		else:
			msg_ = "No such token"
		
		return False, None, msg_

	# Create a new wallet

	def createWallet(self, chainid, wallet, digest):
	
		chains_ = self.chains()
		
		if (chainid != None):
			chainid_ = chainid.lower()
	
			if (chainid_ in chains_):
				xscro_ = ApplicationManager().get("xscro")

				if (xscro_ != None):
					wallets_ = list(xscro_.wallets_.keys())
					
					if (wallet not in wallets_):
					
						newauth_ = extdict()
						newauth_["$class"] = XSCRO_AUTHID
						
						# we encrypt the passcode so even we dont know it !!
						nonce_ = ("%s:%s:%s" % (chainid_, digest, wallet))

						kpt1_ = hashlib.md5()
						kpt1_.update(nonce_.encode(UTF8))
						kpt1out_ = kpt1_.hexdigest()
						
						setattrs(newauth_,
							wallet = wallet,
							passtoken = kpt1out_
							)
							
						shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newauth_])

						return {"wallet":wallet, "status":STATUS_OK}
						
		return None

	# Authenticate a request
			
	def authenticate(self, chainid, wallet, password):
	
		chains_ = self.chains()
		token_ = None
		success_ = False
	
		if (password != None):
			if (chainid in chains_):
				
				xscro_ = ApplicationManager().get("xscro")

				if (xscro_ != None):
					wallets_ = list(xscro_.wallets_.keys())
					
					if (wallet in wallets_):
						
						token_ = xscro_.wallets_[wallet]
						nonce_ = ("%s:%s:%s" % (chainid, password, wallet))
						kpt1_ = hashlib.md5()
						kpt1_.update(nonce_.encode(UTF8))
						kpt1out_ = kpt1_.hexdigest()
						success_ = (kpt1out_ == token_)
	
		return success_, token_
			
	# Change Password for a user

	def changePassword(self, chainid, wallet, digest, token):
	
		chains_ = self.chains()
		
		if (chainid != None):
			chainid_ = chainid.lower()
			
			if (chainid_ in chains_):

				# we encrypt the passcode so even we dont know it !!
				nonce_ = ("%s:%s:%s" % (chainid_, digest, wallet))
				
				kpt1_ = hashlib.md5()
				kpt1_.update(nonce_.encode(UTF8))
				kpt1out_ = kpt1_.hexdigest()

				newauth_ = extdict()
				newauth_["$class"] = XSCRO_AUTHID
				writechange_ = False
				
				setattrs(newauth_,
					wallet = wallet,
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
					return {"wallet":wallet, "status":STATUS_OK}
					
		return None

	# Ack Transaction
	
	def ackTransaction(self, chainid, wallet, token=None, code=0):
		
		if (chainid != None) and (token != None):
	
			chainid_ = chainid.lower()
			code_ = int(code)
			
			xscro_ = ApplicationManager().get("xscro")
	
			if (xscro_ != None):
				
				if (chainid_ in xscro_.trees.keys()):
					
					tokens_ = list(xscro_.opentransactions.keys())
					tree_ = xscro_.trees[chainid_]

					if (token in tokens_):
						
						transaction_ = xscro_.opentransactions[token]
						
						newack_ = extdict()
						newack_["$class"] = XSCRO_ACKID

						setattrs(newack_,
							uid = token,
							ack = code_
							)
						
						if (transaction_.id_parent == RECIPIENT_ETHER):
							if (wallet == RECIPIENT_ETHER):
								shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newack_])
								return {"status":STATUS_OK, "chainid":chainid_, "token":token, "code":code_}
			
						# get the parent coin to the transaction - if the authenticated user owns it, allow the ack !
						else:
							origintoken_ = self.getToken(chainid_, transaction_.id_parent)
							if (origintoken_.data.id_recipient == wallet):
								
								if (code_ == 1):
									volume_ = float(transaction_.volume)
									balance_ = origintoken_.balance
									
									if (balance_ < volume_):
										newack_.ack = -1
										shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newack_])
										return {"status":STATUS_FAIL, "chainid":chainid_, "reason":"Insufficient balance", "code":newack_.ack}
							
								else:
									shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newack_])
									return {"status":STATUS_OK, "chainid":chainid_, "token":token, "code":code_}
	
		return None

