
from www.__common.controllers.XscroController import *

class AuthenticationController(XscroController):

	def __init__(self, handler, session, query=None, isajax=False):
		XscroController.__init__(self, handler, session, query, isajax)

	
	@endpoint(1, True, True, None, "gateway", "^user.logout", "Logout User")
	def userLogout(self, postData=None, appVars=None, params=None, content=None):
		
		self.session.username = None
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Logged Out", "refresh":"window"})
	
	
	@endpoint(1, True, True, None, "gateway", "^user.login", "Login User")
	def userLogin(self, postData=None, appVars=None, params=None, content=None):
		
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
	
	@endpoint(1, True, True, None, "gateway", "^user.newuser", "Create New User")
	def createUser(self, postData=None, appVars=None, params=None, content=None):
		
		now_ = self.epoch
		
		walletid_ = params.walletid
		digest_ = params.password
		chainid_ = params.chainid
		
		xscro_ = ApplicationManager().get("xscro")
		
		if (digest_ != None) and (xscro_ != None):
				
			container_ = xscro_.containers[chainid_]
			transactions_ = []

			walletids_ = list(container_.wallets_.keys())
			
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

				transactions_.append(newauth_)

				if (len(transactions_) > 0):
					shadowhash_, discarded_, deferred_ = self.writeTransactionsToChain(chainid_, transactions_)
						
					return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Wallet Created Successful", "refresh":"redirect", "url":"/user", "delay":100})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Incorrect username/password"})

