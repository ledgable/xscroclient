
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
		
			self.log(self.session.id_session)
		
			kpt1_ = hashlib.md5()
			kpt1_.update(("%s:%s" % (sessionid_, password_)).encode(UTF8))
			digestknown_ = kpt1_.hexdigest()
			
			if (digestknown_ == digestin_):
				
				self.session.username = username_
				
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Login Successful", "refresh":"window"})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Incorrect username/password"})
	
