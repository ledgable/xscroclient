
from www.__common.controllers.XscroController import *

class TestController(XscroController):
	
	def __init__(self, handler, session, query=None, isajax=False):
		Controller.__init__(self, handler, session, query, isajax)
	
	
	@endpoint(2, False, True, None, "get", "^/helloworld", "Say Hello World")
	def callHelloWorld(self, postData=None, appVars=None):
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"greeting":"Hello World"})

	
	@endpoint(1, False, True, None, "get", "^/helloworld/(?P<person>[0-9a-z][^-&*/\%]*)", "Say Hello World to person")
	def callHelloWorldPerson(self, postData=None, appVars=None, person=None):
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"greeting":("Hello World %s" % (person))})


	@endpoint(1, True, True, None, "gateway", "^testjscallserverside", "Test Ajax submission call")
	def testJSCallServerside(self, postData=None, appVars=None, params=None, content=None):
				
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "message":("Well this worked !! - Received %s" % params), "mode":"messagebox"})


	@endpoint(1, True, True, None, "post", "^/callbackwatcher", "check watcher works")
	def callBackWatcher(self, postData=None, appVars=None, person=None):
		
		self.log(postData)
		
		if (postData != None):
			transactions_ = json.loads(postData)
			
			if (transactions_ != None) and (len(transactions_) > 0):
				
				for transaction_ in transactions_:
					
					self.log(transaction_)
		
#					date_ = transaction_.date
#
#					# replace the value with the token hosting the minted coin...
#					token_ = "mymintedtoken"
#
#					recipientid_ = transaction_.sender
#					volume_ = float(transaction_.volume) * 50.0
#					price_ = 0.0
#					transactionid_ = transaction_.transactionid
#
#					# some functionality here...
#					chainid_ = "some chain"
#
#					if (chainid_ != None):
#						chainid_ = chainid.lower()
#
#					if (recipientid != None) and (tokenid != None) and (chainid_ != None) and (transid != None):
#						success_, uid_, status = self.transferToken(chainid_, token_, recipientid, transactionid_, volume_, price_, "Token Transferred", None, "TransferDesk")

		return FunctionResponse(HTTP_OK, TYPE_JSON, {})


	@endpoint(1, False, True, None, "get", "^/requestauth/123", "Request Authentication test")
	def testAuthenticationProcess(self, postData=None, appVars=None, person=None):
	
		authinfo_ = appVars.authentication
		self.log(authinfo_)
		
		if (authinfo_ == None):
			return FunctionResponse(HTTP_SESSION_FAILURE, TYPE_JSON, "123")

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"message":"hello"})
