
from www.__common.controllers.XscroController import *

from modules.applicationmanager import *

RECIPIENT_ETHER = "0"
STATUS_FAIL = 0
STATUS_OK = 1

class AccessController(XscroController):
	
	
	def __init__(self, handler, session, query=None, isajax=False):
		
		XscroController.__init__(self, handler, session, query, isajax)
	
	
	@endpoint(1, False, True, "ADMIN", "post", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/newwallet/(?P<wallet>[0-9a-z][^-&*/\%]*)/(?P<digest>[0-9a-f][^-&*/\%]*)", "Create a new wallet with passcode")
	def createWallet(self, postData=None, appVars=None, chainid=None, wallet=None, digest=None):
	
		chainid_ = chainid
		chains_ = self.chains()
		
		if (chainid_ != None):
			chainid_ = chainid.lower()
			
			info_ = XscroController.createWallet(self, chainid, wallet, digest)

			if (info_ != None):
				return FunctionResponse(HTTP_OK, TYPE_JSON, info_)
						
		return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)

			
	@endpoint(1, True, True, None, "put", "^/api/changepassword/(?P<digest>[0-9a-f][^-&*/\%]*)", "Create a new wallet with passcode")
	def changePassword(self, postData=None, appVars=None, digest=None):
	
		authinfo_ = appVars.authentication
		
		# the chainid is the domain of the authentication - defer to "basic"
		
		if (authinfo_ == None):
			return FunctionResponse(HTTP_AUTHENTICATION_REQ, TYPE_JSON, {"status":"Authentication required"})
	
		chainid_ = authinfo_.realm
		wallet_ = authinfo_.username
		password_ = authinfo_.password
		success_, token_ = XscroController.authenticate(self, chainid_, wallet_, password_)
		
		if (success_):
			
			self.log("Success - authenticated !!")
			info_ = XscroController.changePassword(self, chainid_, wallet_, digest, token_)
			
			if (info_ != None):
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"chain":chainid_, "wallet":wallet_, "status":STATUS_OK})
					
		return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)

	
	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/data/(?P<since>[0-9][^-&*/\%]*)", "Fetch data since x for chain")
	def dataForChain(self, postData=None, appVars=None, chainid=None, since=0):

		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)

		since_ = int(since)
		chains_ = self.chains()
		datapoints_ = {}
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid_.lower()
		
			if (chainid_ in chains_):
				
				if (chainid_ in xscro_.datapoints_.keys()):
					# get the account dataplot for the chain requested
					datapoints_ = xscro_.datapoints_[chainid_]

		return FunctionResponse(HTTP_OK, TYPE_JSON, datapoints_)
			

	@endpoint(94, True, True, None, "get", "^/chain/(?P<chainid>[0-9a-f][^-&*/\%]*)/(?P<mode>(token|owner))/(?P<argid>[0-9a-z][^-&*/\%]*)", "Fetch page for detail")
	def pageForDetailDefault(self, postData=None, appVars=None, chainid=None, mode="token", argid=None):
		
		return self.pageForDetail(postData, appVars, chainid, mode, argid, "/")

	
	@endpoint(93, True, True, None, "get", "^/chain/(?P<chainid>[0-9a-f][^-&*/\%]*)/(?P<mode>(token|owner))/(?P<argid>[0-9a-z][^-&*/\%]*)/(?P<pagename>[^ ]*)", "Fetch detail page by name")
	def pageForDetail(self, postData=None, appVars=None, chainid=None, mode="token", argid=None, pagename=None):
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
		
		chains_ = self.chains()
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid_.lower()
				
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
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
	
		chains_ = self.chains()
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid_.lower()
			
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
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)

		chains_ = self.chains()
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid_.lower()
				
			if (chainid_ in chains_):
			
				# get the account tree for the chain requested
				tree_ = xscro_.trees[chainid_]
				volume_ = tree_.balance
				
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "volume":volume_})
					
		return FunctionResponse(HTTP_OK, TYPE_JSON, {})

	# /api/<chainid>/path/<tokenid>
	# returns the path of the token
	
	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/enumerate/(?P<tokenid>[0-9a-z][^-&*/\%]*)", "Enumerate path for token")
	def enumeratePathForToken(self, postData=None, appVars=None, chainid="", tokenid="0"):
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
	
		chains_ = self.chains()
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid_.lower()
				
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

	# /api/mint/<transid>/<volume>/<recipientid>/<price>
	# creates a new token given volume - assigns this to recipientid

	@endpoint(1, False, True, None, "put", "^/api/mint/(?P<transid>[0-9a-f][^-&*/\%]*)/(?P<volume>[0-9.][^-&*/\%]*)/(?P<recipientid>[0-9a-z][^-&*/\%]*)/(?P<price>[0-9.][^-&*/\%]*)", "Mint a new token")
	def mintNewToken(self, postData=None, appVars=None, transid=None, volume=0.0, recipientid=None, price=0.0):
	
		authinfo_ = appVars.authentication
		
		if (authinfo_ == None):
			return FunctionResponse(HTTP_AUTHENTICATION_REQ, TYPE_JSON, {"status":"Authentication required"})
				
		chainid_ = authinfo_.realm
		wallet_ = authinfo_.username
		password_ = authinfo_.password
		status_ = "Unknown"

		success_, token_ = XscroController.authenticate(self, chainid_, wallet_, password_)

		if (success_):
		
			if (wallet_ == RECIPIENT_ETHER):
				
				if (recipientid != None) and (chainid_ != None):
					success_, uid_, status_ = XscroController.mintNewToken(self, chainid_, RECIPIENT_ETHER, recipientid, transid, volume, price, "Token Minted", appVars.ip_address, None)
				
					if (success_):
						return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "token":uid_, "reason":status_})
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":status_})

	# /api/transfer/<tokenid>/<transid>/<volume>/<recipientid>/<price>
	# transfer part of a token (defined by tokenid) to another recipient given volume and price

	@endpoint(1, False, True, None, "put", "^/api/transfer/(?P<token>[0-9a-z][^-&*/\%]*)/(?P<transid>[0-9a-f][^-&*/\%]*)/(?P<volume>[0-9.][^-&*/\%]*)/(?P<recipientid>[0-9a-z][^-&*/\%]*)/(?P<price>[0-9.][^-&*/\%]*)", "Buy a new token")
	def transferToken(self, postData=None, appVars=None, token=None, transid=None, volume=0.0, recipientid=None, price=0.0):
		
		# perform challenge here...
		authinfo_ = appVars.authentication
		
		if (authinfo_ == None):
			return FunctionResponse(HTTP_AUTHENTICATION_REQ, TYPE_JSON, {"status":"Authentication required"})

		chainid_ = authinfo_.realm
		wallet_ = authinfo_.username
		password_ = authinfo_.password
		
		success_, token_ = XscroController.authenticate(self, chainid_, wallet_, password_)

		if (success_):
			
			# get the token thats being transferred...
			coin_ = XscroController.getToken(self, chainid_, token)
			
			self.log(coin_)
			
			if (coin_ != None):
				if (coin_.data.id_recipient == wallet_):
					success_, uid_, status = XscroController.transferToken(self, chainid_, token, recipientid, transid, volume, price, "Token Transferred", appVars.ip_address, None)

					if (success_):
						return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "token":uid_})
					
					else:
						return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":status})
			
				else:
					return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":"Not owner"})
	
		return FunctionResponse(HTTP_OK, TYPE_JSON, {})
			
	# /api/destroy/<tokenid>/<volume>
	# transfer a token to receipient 0 - effectively destorying it
	
	@endpoint(1, False, True, None, "delete", "^/api/destroy/(?P<tokenid>[0-9a-z][^-&*/\%]*)/(?P<transid>[0-9a-f][^-&*/\%]*)/(?P<volume>[0-9.][^-&*/\%]*)", "Destroy a token")
	def destroyToken(self, postData=None, appVars=None, tokenid=None, transid=None, volume=0.0):

		# perform challenge here...
		authinfo_ = appVars.authentication
		
		if (authinfo_ == None):
			return FunctionResponse(HTTP_AUTHENTICATION_REQ, TYPE_JSON, {"status":"Authentication required"})

		chainid_ = authinfo_.realm
		wallet_ = authinfo_.username
		password_ = authinfo_.password
		
		success_, token_ = XscroController.authenticate(self, chainid_, wallet_, password_)

		if (success_):

			# get the token thats being destroyed...
			coin_ = XscroController.getToken(self, chainid_, tokenid)
			
			if (coin_ != None) and (coin_.data.id_recipient == wallet_):
				success_, uid_, status = XscroController.destroyToken(self, chainid_, tokenid, transid, volume, "Token Destroyed", appVars.ip_address, None)

				if (success_):
					return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "token":uid_})

				else:
					return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":status})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {})
		
	# /api/<chainid>/children/<tokenid>
	# get the child tokens of a specified token
	
	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/children/(?P<tokenid>[0-9a-z][^-&*/\%]*)", "Get child tokens")
	def childrenForToken(self, postData=None, appVars=None, chainid="", tokenid=None):
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
		
		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid_.lower()

			if (tokenid != None) and (chainid_ != None):
				
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
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)

		chainid_ = chainid
		
		if (chainid_ != None):
			chainid_ = chainid_.lower()
			
			if (argid != None) and (chainid_ != None):
				
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

		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
	
		chainid_ = chainid
		transactions_ = []
		
		if (chainid_ != None):
			chainid_ = chainid_.lower()
			
			if (chainid_ in xscro_.trees.keys()):
				if (mode == "open"):
					
					transactions_ = list(xscro_.opentransactions.values())
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_OK, "chainid":chainid_, "data":transactions_})

	# /api/ack/<transactionid>/<code>

	@endpoint(1, False, True, None, "put", "^/api/ack/(?P<token>[0-9a-z][^-&*/\%]*)/(?P<code>[0-9][^-&*/\%]*)", "Acknowledge transaction with code")
	def ackTransaction(self, postData=None, appVars=None, token=None, code=0):

		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)

		# perform challenge here...
		authinfo_ = appVars.authentication
		
		if (authinfo_ == None):
			return FunctionResponse(HTTP_AUTHENTICATION_REQ, TYPE_JSON, {"status":"Authentication required"})

		chainid_ = authinfo_.realm
		wallet_ = authinfo_.username
		password_ = authinfo_.password
		
		success_, token_ = XscroController.authenticate(self, chainid_, wallet_, password_)

		# get the token thats being transferred...

		if (success_) and (token != None):
						
			response_ = XscroController.ackTransaction(self, chainid_, wallet_, token, code)
			
			if (response_ != None):
				return FunctionResponse(HTTP_OK, TYPE_JSON, response_)
					
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":STATUS_FAIL, "reason":"no such token"})

	# /api/<chainid>/balance/<token|owner>/<argid>
	# get balance for appropriate request

	@endpoint(1, False, True, None, "get", "^/api/(?P<chainid>[0-9a-f][^-&*/\%]*)/balance/(?P<mode>(token|owner))/(?P<argid>[0-9a-z][^-&*/\%]*)", "Get value of token or owner")
	def balanceFor(self, postData=None, appVars=None, chainid="", mode="token", argid=None):
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (xscro_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
	
		if (chainid != None):
			chainid_ = chainid.lower()
		
			if (argid != None):
				
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

