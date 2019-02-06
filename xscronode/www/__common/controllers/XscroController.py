
from www.__common.controllers.NodeController import *

from modules.applicationmanager import *

RECIPIENT_ETHER = "0"
STATUS_FAIL = 0
STATUS_OK = 1

class XscroController(NodeController):
	
	
	def __init__(self, handler, session, query=None, isajax=False):
		
		NodeController.__init__(self, handler, session, query, isajax)
	
	# create a new token from the ether (parent address = 0)
	
	def __mintNewToken(self, chainid, parentid=RECIPIENT_ETHER, recipientid=None, transid=None, volume=0.0, price=0.0, additional="Token Minted", ipaddress="0.0.0.0", traderid=None):
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
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
		
		uid_ = self.uniqueId
	
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

	# transfer a token into the ether (address = 0) effectively destorying it

	def __destroyToken(self, chainid, tokenid, transid=None, volume=0.0, additional="Token Destroyed", ipaddress="0.0.0.0", traderid=None):

		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
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
						
						uid_ = self.uniqueId

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
			
	# transfer a token to another
			
	def __transferToken(self, chainid, tokenid, recipientid=None, transid=None, volume=0.0, price=0.0, additional="Token Transferred", ipaddress="0.0.0.0", traderid=None):
	
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
		xscro_ = ApplicationManager().get("xscro")
		msg_ = "Unknown error"
		
		if (xscro_ != None):
			
			# if volume or price is < 0 then abort
			
			volume_ = float(volume)
			if (volume_ < 0):
				return False, None, "Volume invalid - must be > 0"
		
			price_ = float(price)
			if (price_ < 0):
				return False, None, "Price invalid - must be >= 0"
			
			if (chainid_ in xscro_.trees.keys()):
				
				# get the account tree for the chain requested
				tree_ = xscro_.trees[chainid_]
				
				# find the token in the sequence
				token_ = tree_.find(tokenid)
					
				if (token_ != None):
						
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

						uid_ = self.uniqueId
						
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

			else:
				msg_ = "Chain invalid"
								
		return False, None, msg_

			
	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/data/(?P<since>[0-9][^-&*/\%]*)", "Fetch data since x for chain")
	def dataForChain(self, postData=None, appVars=None, chainid=None, since=0):
		
		since_ = int(since)
		chains_ = self.chains()
		datapoints_ = {}
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
		if (chainid_ in chains_):
			xscro_ = ApplicationManager().get("xscro")
			
			if (xscro_ != None):
		
				if (chainid_ in xscro_.datapoints_.keys()):
					# get the account dataplot for the chain requested
					datapoints_ = xscro_.datapoints_[chainid_]

		return FunctionResponse(HTTP_OK, TYPE_JSON, datapoints_)
			

	@endpoint(94, True, True, None, "get", "^/chain/(?P<chainid>[0-9a-f][^-&*/\%]*)/(?P<mode>(token|owner))/(?P<argid>[0-9a-z][^-&*/\%]*)", "Fetch page for detail")
	def pageForDetailDefault(self, postData=None, appVars=None, chainid=None, mode="token", argid=None):
		
		return self.pageForDetail(postData, appVars, chainid, mode, argid, "/")

	
	@endpoint(93, True, True, None, "get", "^/chain/(?P<chainid>[0-9a-f][^-&*/\%]*)/(?P<mode>(token|owner))/(?P<argid>[0-9a-z][^-&*/\%]*)/(?P<pagename>[^ ]*)", "Fetch detail page by name")
	def pageForDetail(self, postData=None, appVars=None, chainid=None, mode="token", argid=None, pagename=None):
		
		chains_ = self.chains()
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ != None):
		
			if (chainid_ in xscro_.trees.keys()):
			
				# get the account tree for the chain requested
				tree_ = xscro_.trees[chainid_]
		
				if (pagename != None):
					if (pagename[0:1:] == "/"):
						pagename = pagename[1:]

				if (pagename == None) or (pagename == ""):
					pagename = "default"

				appVars.chainid = chainid_

				if (mode == "token"):
					appVars.tokenid = argid
					appVars.token = tree_.find(argid)

				elif (mode == "owner"):
					appVars.tree = tree_
					appVars.ownerid = argid

				content_ = self.loadContent(("__%s/%s.html.py" % (mode, pagename)), appVars)

				if (content_ == None):
					return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)

				contentout_ = content_

				if (not self.isajax):
					contentout_ = self.appendView("template_web.html", content_, appVars)

				return FunctionResponse(HTTP_OK, TYPE_HTML, contentout_)
		
		return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
	

	# /chain/<chainid>
	# fetch default chain page

	@endpoint(96, True, True, None, "get", "^/chain/(?P<chainid>[0-9a-f][^-&*/\%]*)", "Fetch page for chain")
	def pageForChainDefault(self, postData=None, appVars=None, chainid=None):
		
		return self.pageForChain(postData, appVars, chainid, "/")

	# /chain/<chainid>/<pagename>
	# fetch page for chain
	
	@endpoint(95, True, True, None, "get", "^/chain/(?P<chainid>[0-9a-f][^-&*/\%]*)/(?P<pagename>[^ ]*)", "Fetch chain page by name")
	def pageForChain(self, postData=None, appVars=None, chainid=None, pagename=None):
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
		chains_ = self.chains()
		
		if (chainid_ in chains_):
		
			if (pagename != None):
				if (pagename[0:1:] == "/"):
					pagename = pagename[1:]
			
			if (pagename == None) or (pagename == ""):
				pagename = "default"
			
			appVars.chainid = chainid_
			
			content_ = self.loadContent(("__chain/%s.html.py" % pagename), appVars)
			
			if (content_ == None):
				return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
		
			contentout_ = content_
			
			if (not self.isajax):
				contentout_ = self.appendView("template_web.html", content_, appVars)

			return FunctionResponse(HTTP_OK, TYPE_HTML, contentout_)

		return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
	
	# /api/<chainid>/check
	# returns the balance of the chain
	
	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/check", "Check application access")
	def checkService(self, postData=None, appVars=None, chainid=""):
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ != None):
		
			if (chainid_ in xscro_.trees.keys()):
			
				# get the account tree for the chain requested
				tree_ = xscro_.trees[chainid_]
				volume_ = tree_.balance
				
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "volume":volume_})
					
		return FunctionResponse(HTTP_OK, TYPE_JSON, {})

	# /api/<chainid>/path/<tokenid>
	# returns the path of the token
	
	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/enumerate/(?P<tokenid>[0-9a-f][^-&*/\%]*)", "Enumerate path for token")
	def enumeratePathForToken(self, postData=None, appVars=None, chainid="", tokenid="0"):
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ != None):
		
			if (chainid_ in xscro_.trees.keys()):
				
				# get the account tree for the chain requested
				tree_ = xscro_.trees[chainid_]
				token_ = None
				path_ = []
				
				if (tokenid == RECIPIENT_ETHER):
					pass
				
				else:
					token_ = tree_.find(tokenid)
				
				if (token_ != None):
					while (token_.parent != None):
						token_ = token_.parent
						
						if (token_.data != None):
							data_ = token_.data
							data_.balance = token_.balance
							path_.append(data_)
							
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "data":path_})
	
		return FunctionResponse(HTTP_OK, TYPE_JSON, {})

	# /api/<chainid>/mint/<transid>/<volume>/<recipientid>/<price>
	# creates a new token given volume - assigns this to recipientid

	@endpoint(1, False, True, None, "put", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/mint/(?P<transid>[0-9a-f][^-&*/\%]*)/(?P<volume>[0-9.][^-&*/\%]*)/(?P<recipientid>[0-9a-z][^-&*/\%]*)/(?P<price>[0-9.][^-&*/\%]*)", "Mint a new token")
	def mintNewToken(self, postData=None, appVars=None, chainid="", transid=None, volume=0.0, recipientid=None, price=0.0):
	
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
		if (recipientid != None) and (chainid_ != None):
		
			success_, uid_, status = self.__mintNewToken(chainid_, RECIPIENT_ETHER, recipientid, transid, volume, price, "Token Minted", appVars.ip_address, None)
		
			if (success_):
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "token":uid_})
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":status})

	# mint a token via ajax
	
	@endpoint(1, True, True, None, "gateway", "^mintNewToken", "Mint a new token")
	def mintNewTokenAjax(self, postData=None, appVars=None, params=None, content=None):
		
		chainid_ = params.chainid
		if (chainid_ != None):
			chainid_ = chainid_.lower()
		else:
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":("Invalid chain"), "mode":"notify"})

		recipientid_ = params.id_recipient
		if (recipientid_ != None):
			recipientid_ = recipientid_.lower()
		else:
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":("Invalid recipient"), "mode":"notify"})

		transactionid_ = params.id_transaction
		if (transactionid_ != None):
			transactionid_ = transactionid_.lower()
		else:
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":("Invalid transaction-id"), "mode":"notify"})

		traderid_ = params.id_trader
		if (traderid_ != None):
			traderid_ = traderid_.lower()

		additional_ = params.default("additional", "Token Minted")

		success_, uid_, status = self.__mintNewToken(chainid_, RECIPIENT_ETHER, recipientid_, transactionid_, params.volume, params.price, additional_, appVars.ip_address, traderid_)

		if (success_):
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "message":("Token created with id %s" % uid_), "mode":"notify", "refresh":"page"})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":status, "mode":"notify"})

	# transfer a token to someone else via ajax
	
	@endpoint(1, True, True, None, "gateway", "^transferToken", "Mint a new token")
	def transferTokenAjax(self, postData=None, appVars=None, params=None, content=None):

		chainid_ = params.chainid
		if (chainid_ != None):
			chainid_ = chainid_.lower()
		else:
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":("Invalid chain"), "mode":"notify"})

		tokenid_ = params.tokenid
		if (tokenid_ != None):
			tokenid_ = tokenid_.lower()
		else:
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":("Invalid token"), "mode":"notify"})

		recipientid_ = params.id_recipient
		if (recipientid_ != None):
			recipientid_ = recipientid_.lower()
		else:
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":("Invalid recipient"), "mode":"notify"})

		transactionid_ = params.id_transaction
		if (transactionid_ != None):
			transactionid_ = transactionid_.lower()
		else:
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":("Invalid transaction-id"), "mode":"notify"})

		traderid_ = params.id_trader
		if (traderid_ != None):
			traderid_ = traderid_.lower()
		
		additional_ = params.default("additional", "Token transferred")

		success_, uid_, status = self.__transferToken(chainid_, tokenid_, recipientid_, transactionid_, params.volume, params.price, additional_, appVars.ip_address, traderid_)

		if (success_):
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "message":("Token transferred with id %s" % uid_), "mode":"notify", "refresh":"page"})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":status, "mode":"notify"})

	# /api/<chainid>/buy/<tokenid>/<transid>/<volume>/<recipientid>/<price>
	# transfer part of a token (defined by tokenid) to another recipient given volume and price

	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/buy/(?P<tokenid>[0-9a-f][^-&*/\%]*)/(?P<transid>[0-9a-f][^-&*/\%]*)/(?P<volume>[0-9.][^-&*/\%]*)/(?P<recipientid>[0-9a-z][^-&*/\%]*)/(?P<price>[0-9.][^-&*/\%]*)", "Buy a new token")
	def transferToken(self, postData=None, appVars=None, chainid="", tokenid=None, transid=None, volume=0.0, recipientid=None, price=0.0):
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()

		if (recipientid != None) and (tokenid != None) and (chainid_ != None) and (transid != None):
		
			success_, uid_, status = self.__transferToken(chainid_, tokenid, recipientid, transid, volume, price, "Token Transferred", appVars.ip_address, None)

			if (success_):
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "token":uid_})
						
			else:
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":status})
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {})

	# /api/<chainid>/destroy/<tokenid>/<volume>
	# transfer a token to receipient 0 - effectively destorying it
	
	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/destroy/(?P<tokenid>[0-9a-f][^-&*/\%]*)/(?P<transid>[0-9a-f][^-&*/\%]*)/(?P<volume>[0-9.][^-&*/\%]*)", "Destroy a token")
	def destroyToken(self, postData=None, appVars=None, chainid="", tokenid=None, transid=None, volume=0.0):

		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
		if (tokenid != None) and (chainid_ != None):
			
			success_, uid_, status = self.__destroyToken(chainid_, tokenid, transid, volume, "Token Destroyed", appVars.ip_address, None)

			if (success_):
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "token":uid_})

			else:
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":status})
	
		return FunctionResponse(HTTP_OK, TYPE_JSON, {})
	
	# destroy a token over ajax
	
	@endpoint(1, True, True, None, "gateway", "^destroyToken", "Destroy a token")
	def destroyTokenAjax(self, postData=None, appVars=None, params=None, content=None):

		chainid_ = params.chainid
		if (chainid_ != None):
			chainid_ = chainid_.lower()
		else:
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":("Invalid chain"), "mode":"notify"})

		tokenid_ = params.tokenid
		if (tokenid_ != None):
			tokenid_ = tokenid_.lower()
		else:
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":("Invalid token"), "mode":"notify"})

		success_, uid_, status = self.__destroyToken(chainid_, tokenid_, self.uniqueId, 0, "Token Destroyed", appVars.ip_address, None)
	
		if (success_):
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "message":("Token %s destroyed" % uid_), "mode":"notify", "refresh":"page"})
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "message":status, "mode":"notify"})
	
	# /api/<chainid>/children/<tokenid>
	# get the child tokens of a specified token
	
	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/children/(?P<tokenid>[0-9a-f][^-&*/\%]*)", "Get child tokens")
	def childrenForToken(self, postData=None, appVars=None, chainid="", tokenid=None):
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()

		if (tokenid != None) and (chainid_ != None):
			
			xscro_ = ApplicationManager().get("xscro")
			
			if (xscro_ != None):
				
				if (chainid_ in xscro_.trees.keys()):
					
					# get the account tree for the chain requested
					tree_ = xscro_.trees[chainid_]
					token_ = None
					
					if (tokenid == RECIPIENT_ETHER): # this is the root !
						token_ = tree_
					
					else:
						# find the token in the sequence
						token_ = tree_.find(tokenid)
					
					if (token_ != None):
						
						children_ = token_.children
						childtokens_ = []
						
						if (children_ != None) and (len(children_) > 0):
							for child_ in children_:
								childtokens_.append({"token":child_.uid, "volume":child_.data.volume, "balance":child_.balance})
						
						return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "token":tokenid, "tokens":childtokens_})
					
					else:
						return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":"no such token", "tokens":[]})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {})
	
	# /api/<chainid>/list/<token|owner>/<argid>
	# list transactions for a given token

	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/list/(?P<mode>(token|owner))/(?P<argid>[0-9a-z][^-&*/\%]*)", "List info for token or user")
	def listInfoFor(self, postData=None, appVars=None, chainid="", mode="token", argid=None):
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
		if (argid != None) and (chainid_ != None):
			
			xscro_ = ApplicationManager().get("xscro")

			if (xscro_):
	
				if (chainid_ in xscro_.trees.keys()):
	
					# get the account tree for the chain requested
					tree_ = xscro_.trees[chainid_]
					
					if (mode == "token"):

						token_ = None

						if (argid == RECIPIENT_ETHER): # this is the root !
							token_ = tree_
					
						else:
							# find the token in the sequence
							token_ = tree_.find(argid)

						if (token_ != None):
							
							volume_ = token_.balance
							transactions_ = []
							
							if (token_.data != None):
								transactions_.append(token_.data)

							childdata_ = token_.childdata
							if (childdata_ != None):
								transactions_.extend(childdata_)
							
							return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "token":argid, "volume":volume_, "data":transactions_})
				
						else:
							return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":"no such token"})

					elif (mode == "owner"):
						
						volume_ = 0
						tokens_ = tree_.transactionsFor(argid)
						
						if (len(tokens_) > 0):
							for token_ in tokens_:
								volume_ += token_.balance
						
						return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "owner":argid, "volume":volume_, "data":tokens_})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {})

	# /api/<chainid>/open/transactions
	# get transactions that have received no acknowledgement
	
	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/(?P<mode>(open))/transactions", "Get open transactions")
	def getOpenTransactions(self, postData=None, appVars=None, chainid="", mode="open"):

		chainid_ = chainid
		transactions_ = []
		
		if (chainid_ != None):
			
			chainid_ = chainid.lower()
			xscro_ = ApplicationManager().get("xscro")
			
			if (xscro_ != None):
				if (chainid_ in xscro_.trees.keys()):
					if (mode == "open"):
						
						transactions_ = list(xscro_.opentransactions.values())
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "chainid":chainid_, "data":transactions_})

	# /api/<chainid>/ack/<transactionid>/<code>

	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/ack/(?P<transactionid>[0-9a-f][^-&*/\%]*)/(?P<code>[0-9][^-&*/\%]*)", "Acknowledge transaction with code")
	def ackTransaction(self, postData=None, appVars=None, chainid="", transactionid=None, code=0):

		chainid_ = chainid
		
		if (chainid_ != None) and (transactionid != None):
			
			chainid_ = chainid.lower()
			code_ = int(code)
			transactionid_ = transactionid.lower()
			xscro_ = ApplicationManager().get("xscro")
	
			if (xscro_ != None):
				if (chainid_ in xscro_.trees.keys()):
					
					transactions_ = list(xscro_.opentransactions.keys())
	
					if (transactionid_ in transactions_):
						
						newack_ = extdict()
						newack_["$class"] = XSCRO_ACKID

						setattrs(newack_,
							uid = transactionid_,
							ack = code_
							)

						shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, [newack_])
						
						return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "chainid":chainid_, "transactionid":transactionid_})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":"no such token"})

	# /api/<chainid>/balance/<token|owner>/<argid>
	# get balance for appropriate request

	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/balance/(?P<mode>(token|owner))/(?P<argid>[0-9a-z][^-&*/\%]*)", "Get value of token or owner")
	def balanceFor(self, postData=None, appVars=None, chainid="", mode="token", argid=None):

		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
		
		if (chainid_ != None) and (argid != None):
		
			xscro_ = ApplicationManager().get("xscro")

			if (xscro_ != None):
				
				if (chainid_ in xscro_.trees.keys()):
					
					# get the account tree for the chain requested
					tree_ = xscro_.trees[chainid_]
					
					if (mode == "token"):
						token_ = None
					
						if (argid == RECIPIENT_ETHER): # this is the root !
							token_ = tree_
					
						else:
							# find the token in the sequence
							token_ = tree_.find(argid)
						
						if (token_ != None):
							volume_ = token_.balance
							return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "token":argid, "volume":volume_})
						
						else:
							return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":"no such token"})
								
					elif (mode == "owner"):
						volume_ = tree_.balanceFor(argid)
						
						return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "ownerid":argid, "volume":volume_})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {})

