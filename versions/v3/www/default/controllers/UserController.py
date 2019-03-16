
from www.__common.controllers.XscroController import *

class UserController(XscroController):
	
	def __init__(self, handler, session, query=None, isajax=False):
		XscroController.__init__(self, handler, session, query, isajax)


	@endpoint(1, True, True, None, "gateway", "^walletuser.userlogout", "Logout User")
	def walletUserLogout(self, postData=None, appVars=None, params=None, content=None):
		
		self.session.username = None
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Logged Out", "refresh":"window"})
		
	
	@endpoint(1, True, True, None, "gateway", "^walletuser.changepassword", "Login User")
	def walletUserChangePassword(self, postData=None, appVars=None, params=None, content=None):
	
		username_ = self.session.username
		currentpassword_ = params.currentpassword
		newpassword_ = params.newpassword
		
		if (username_ != None):
			
			tokentype_, nonce_ = username_.split(":")
			chainid_, walletid_, digest_ = nonce_.split(",")

			if (digest_ == currentpassword_):
				# ok to continue...

				success_ = XscroController.changePassword(self, chainid_, walletid_, newpassword_, None)
	
				if (success_ != None):
					self.session.username = None
					return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Password is changes - Now logging you out", "refresh":"window"})
						
			else:
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Your password is invalid"})
					
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Operation Failed"})

	
	@endpoint(1, True, True, None, "gateway", "^walletuser.userlogin", "Login User")
	def walletUserLogin(self, postData=None, appVars=None, params=None, content=None):
		
		now_ = self.epoch

		chainid_ = params.chainid
		walletid_ = params.walletid
		password_ = params.password
		
		success_, token_ = XscroController.authenticate(self, chainid_, walletid_, password_)
		
		if (success_):
			
			sessionid_ = self.session.id_session
			
			self.session.chainid = chainid_
			self.session.username = "wallet:%s,%s,%s" % (chainid_, walletid_, password_)
			
			self.handler.SESSIONS.sessions[sessionid_] = self.session
				
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Login Successful", "refresh":"window", "delay":100})
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Incorrect username/password"})

	
	@endpoint(1, False, True, "WALLET", "get", "^/api/user/transactions/(?P<count>[0-9][^-&*/\%]*)", "Get recent transactions")
	def getUserTransactions(self, postData=None, appVars=None, count=None):
		
		transactions_ = []
		username_ = self.session.username
		
		if (username_ != None):
		
			tokentype_, nonce_ = username_.split(":")
			chainid_, walletid_, digest_ = nonce_.split(",")

			transactions_ = XscroController.allTransactionsForWallet(self, chainid_, walletid_)

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"chainid":chainid_, "transactions":transactions_})
		
		
	@endpoint(1, False, True, "WALLET", "get", "^/api/user/open/transactions/(?P<count>[0-9][^-&*/\%]*)", "Get recent transactions")
	def getOpenUserTransactions(self, postData=None, appVars=None, count=None):
		
		transactions_ = []
		username_ = self.session.username
		
		if (username_ != None):
			
			tokentype_, nonce_ = username_.split(":")
			chainid_, walletid_, digest_ = nonce_.split(",")
			
			transactions_ = XscroController.allOpenTransactionsForWallet(self, chainid_, walletid_)
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"chainid":chainid_, "transactions":transactions_})
	
		
	@endpoint(98, True, True, None, "get", "^/user", "Fetch user page by name")
	def walletDefaultPage(self, postData=None, appVars=None):
	
		return self.walletPage(postData, appVars, None)
	
	
	@endpoint(97, True, True, None, "get", "^/user/(?P<pagename>[^ ]*)", "Fetch user page by name")
	def walletPage(self, postData=None, appVars=None, pagename=None):
		
		username_ = self.session.username
		chainid_ = self.session.chainid
		
		if (pagename != None):
			if (pagename[0:1:] == "/"):
				pagename = pagename[1:]

		content_ = None
	
		if (username_ == None):
			content_ = self.loadContent("user/__login.html.py", appVars)
		
		else:
			if (pagename == None) or (pagename == ""):
				pagename = "default"
			
			content_ = self.loadContent(("user/%s.html.py" % pagename), appVars)
	
		if (content_ != None):
			
			contentout_ = content_
			
			if self.isajax == False:
				contentout_ = self.appendView("template_web.html", content_, appVars)
			
			return FunctionResponse(HTTP_OK, TYPE_HTML, contentout_)
		
		return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
