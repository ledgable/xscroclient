
from www.__common.controllers.XscroController import *

class AdminController(XscroController):

	def __init__(self, handler, session, query=None, isajax=False):
		XscroController.__init__(self, handler, session, query, isajax)

	
	@endpoint(1, True, True, None, "gateway", "^admin.userlogout", "Logout User")
	def adminUserLogout(self, postData=None, appVars=None, params=None, content=None):
		
		self.session.username = None
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Logged Out", "refresh":"window"})
	
	
	@endpoint(1, True, True, None, "gateway", "^admin.userlogin", "Login User")
	def adminUserLogin(self, postData=None, appVars=None, params=None, content=None):
		
		now_ = self.epoch
		
		username_ = params.username
		digestin_ = params.password
		password_ = self.handler.AUTHENTICATION.getDigestForUser(username_, "basic")
		
		if (password_ != None):
			
			sessionid_ = self.session.id_session
			
			kpt1_ = hashlib.md5()
			kpt1_.update(("%s:%s" % (sessionid_, password_)).encode(UTF8))
			digestknown_ = kpt1_.hexdigest()
			
			if (digestknown_ == digestin_):
				self.session.username = username_
				self.handler.SESSIONS.sessions[sessionid_] = self.session
				
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Login Successful", "refresh":"window", "delay":100})
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Incorrect username/password"})
		
	
	@endpoint(1, True, True, "ADMIN", "gateway", "^admin.addwallets", "Add Wallets")
	def adminAddWallets(self, postData=None, appVars=None, params=None, content=None):
		
		chainid_ = params.chainid
		wallets_ = params.wallets

		if (chainid_ != None):
			
			chainid_ = chainid_.lower()
			chains_ = self.chains()
			
			if (chainid_ in chains_):
				
				xscro_ = ApplicationManager().get("xscro")
				
				if (xscro_ != None):
					
					container_ = xscro_.containers[chainid_]
					transactions_ = []

					if (wallets_ != None):
						
						walletids_ = list(container_.wallets_.keys())
						
						for wallet_ in wallets_:
							
							digest_ = wallet_.password
							walletid_ = wallet_.walletid
							
							if (walletid_ not in walletids_):
							
								newauth_ = extdict()
								newauth_["$class"] = XSCRO_AUTHID
								
								nonce_ = ("%s:%s:%s" % (chainid_, digest_, walletid_))
								
								kpt1_ = hashlib.md5()
								kpt1_.update(nonce_.encode(UTF8))
								kpt1out_ = kpt1_.hexdigest()
								
								setattrs(newauth_,
									wallet = walletid_,
									passtoken = kpt1out_
									)
							
								walletids_.append(walletid_)
								transactions_.append(newauth_)
						
						if (len(transactions_) > 0):
							shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, transactions_)
							
							return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"%d Wallets Created" % (len(transactions_))})
	
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Invalid operation"})
	
	
	@endpoint(1, True, True, "ADMIN", "gateway", "^admin.acktransaction", "Acknowledge Transaction")
	def adminAckTransaction(self, postData=None, appVars=None, params=None, content=None):
		
		paymenttoken_ = params.token
		chainid_ = params.chainid
		code_ = int(params.code)
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (chainid_ != None) and (paymenttoken_ != None):
			
			chainid_ = chainid_.lower()
			
			if (chainid_ in xscro_.containers.keys()):
				
				container_ = xscro_.containers[chainid_]
				transaction_ = container_.pending[paymenttoken_]
	
				if (transaction_ != None):
					success_, response_ = XscroController.ackTransaction(self, chainid_, transaction_.id_parent, paymenttoken_, code_)
	
					if (success_):
						if (code_ == 1):
							return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Transaction acknowledged"})
						else:
							return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":("Transaction rejected (code=%d)" % code_)})

					else:
						return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":response_})
	
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Invalid operation"})


	@endpoint(1, False, True, "ADMIN", "gateway", "^admin.minttoken", "Create new token")
	def adminMintToken(self, postData=None, appVars=None, params=None, content=None):

		chainid_ = params.chainid
		walletid_ = params.walletid
		volume_ = float(params.default("volume", 0.0))
		ppt_ = float(params.default("ppt", 0.0))
		note_ = params.note
		
		if (note_ == None):
			note_ = "Token Minted via eSelfService process"
		
		transid_ = self.uniqueId
		ipaddress_ = self.session.ip_address
		
		if (ppt_ < 0.0):
			ppt_ = 0.0
		
		if (volume_ <= 0.0):
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Volume must be set"})
				
		else:
			success_, token_, msg_ = XscroController.mintNewToken(self, chainid_, RECIPIENT_ETHER, walletid_, transid_, volume_, ppt_, note_, ipaddress_, "eSelfService")
		
			if (success_):
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Token Created", "refresh":"page"})
			
			else:
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Token Creation failed - %s" % msg_, "refresh":"page"})

			
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Operation Failed"})

			
	@endpoint(1, False, True, "ADMIN", "gateway", "^admin.switchchain", "Switch Chain")
	def adminSwitchChain(self, postData=None, appVars=None, params=None, content=None):
	
		self.session.chainid = params.chainid
	
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Chain Switched", "refresh":"window", "delay":1000})
		
		#return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Failed to perform operation"})
	
	
	@endpoint(1, False, True, "ADMIN", "get", "^/api/admin/chains", "Get chains")
	def getAdminChains(self, postData=None, appVars=None):
		
		chains_ = self.chains()
		out_ = []
		
		if (len(chains_) > 0):
			for chain_ in chains_:
				out_.append({"uid":chain_, "display":chain_})
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, out_)
	
	
	@endpoint(1, False, True, "ADMIN", "get", "^/api/admin/(?P<chainid>[0-9a-f][^-&*/\%]*)/transactions/(?P<count>[0-9][^-&*/\%]*)", "Get recent transactions")
	def getAdminTransactionsForChain(self, postData=None, appVars=None, chainid=None, count=None):
		
		transactions_ = XscroController.allTransactions(self, chainid)
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"chainid":chainid, "transactions":transactions_})
	
	
	@endpoint(1, False, True, "ADMIN", "get", "^/api/admin/(?P<chainid>[0-9a-f][^-&*/\%]*)/wallets", "Get wallets for chain")
	def getAdminWalletsForChain(self, postData=None, appVars=None, chainid=None, count=None):
		
		wallets_ = XscroController.allWallets(self, chainid)
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"chainid":chainid, "wallets":wallets_})
	
	
	@endpoint(98, True, True, None, "get", "^/admin", "Fetch admin page by name")
	def adminDefaultPage(self, postData=None, appVars=None):
	
		return self.adminPage(postData, appVars, None)

	
	@endpoint(97, True, True, None, "get", "^/admin/(?P<pagename>[^ ]*)", "Fetch admin page by name")
	def adminPage(self, postData=None, appVars=None, pagename=None):
		
		username_ = self.session.username
		chainid_ = self.session.chainid
		
		if (chainid_ == None):
			xscro_ = ApplicationManager().get("xscro")
			chains_ = self.chains()
			
			if (len(chains_) > 0):
				chainid_ = chains_[0]
				
		self.session.chainid = chainid_
		
		if (pagename != None):
			if (pagename[0:1:] == "/"):
				pagename = pagename[1:]

		content_ = None
		
		if (username_ == None) or ("ADMIN" not in self.session.permissions):
			content_ = self.loadContent("admin/__login.html.py", appVars)

		else:
			if (pagename == None) or (pagename == ""):
				pagename = "default"
		
			content_ = self.loadContent(("admin/%s.html.py" % pagename), appVars)
		
		if (content_ != None):
	
			contentout_ = content_
		
			if self.isajax == False:
				contentout_ = self.appendView("template_web.html", content_, appVars)

			return FunctionResponse(HTTP_OK, TYPE_HTML, contentout_)

		return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
