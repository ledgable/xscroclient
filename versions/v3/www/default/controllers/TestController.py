
from www.__common.controllers.XscroController import *

class TestController(XscroController):
	
	def __init__(self, handler, session, query=None, isajax=False):
		XscroController.__init__(self, handler, session, query, isajax)
	
	
	@endpoint(2, False, True, None, "get", "^/helloworld", "Say Hello World")
	def callHelloWorld(self, postData=None, appVars=None):
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"greeting":"Hello World"})

	
	@endpoint(1, False, True, None, "get", "^/helloworld/(?P<person>[0-9a-z][^-&*/\%]*)", "Say Hello World to person")
	def callHelloWorldPerson(self, postData=None, appVars=None, person=None):
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"greeting":("Hello World %s" % (person))})


	@endpoint(1, True, True, None, "gateway", "^testjscallserverside", "Test Ajax submission call")
	def testJSCallServerside(self, postData=None, appVars=None, params=None, content=None):
				
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "message":("Well this worked !! - Received %s" % params), "mode":"messagebox"})

	
	@endpoint(1, False, True, None, "get", "^/requestauth/123", "Request Authentication test")
	def testAuthenticationProcess(self, postData=None, appVars=None, person=None):
	
		authinfo_ = appVars.authentication
		self.log(authinfo_)
		
		if (authinfo_ == None):
			return FunctionResponse(HTTP_SESSION_FAILURE, TYPE_JSON, "123")

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"message":"hello"})
