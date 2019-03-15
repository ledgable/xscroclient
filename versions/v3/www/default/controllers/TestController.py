
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


	@endpoint(1, True, True, None, "post", "^/callbackwatcher/(?P<chainid>[0-9a-z][^-&*/\%]*)", "check watcher works")
	def callBackWatcher(self, postData=None, appVars=None, chainid=None):
		
		MULTIPLIER = 2.0
		HOSTWALLET = "xscro"
		
		if (postData != None) and (chainid != None) and (HOSTWALLET != None):
			
			chainid_ = chainid.lower()
			xscro_ = ApplicationManager().get("xscro")
			
			if (chainid_ in xscro_.containers.keys()):

				transactions_ = extlist(json.loads(postData))
				container_ = xscro_.containers[chainid_]
				
				if (transactions_ != None) and (len(transactions_) > 0):
					
					for transaction_ in transactions_:
					
						self.log(transaction_)

						recipientid_ = transaction_.sender
						transactionid_ = transaction_.transactionid
						volume_ = float(Decimal(transaction_.volume)) * MULTIPLIER
						price_ = 0.0
						
						storedtransaction_ = container_.findTransaction(transactionid_)
						
						if (storedtransaction_):
							# already processed this transaction
						
							self.log("Already noted this! - Skipping")
						
						else:
							success_, uid_, status = XscroController.transferValue(self, chainid_, HOSTWALLET, recipientid_, transactionid_, volume_, price_, "Token Transferred From Ether", None, "TransferDesk")
	
		return FunctionResponse(HTTP_OK, TYPE_JSON, {})


	@endpoint(1, False, True, None, "get", "^/requestauth/123", "Request Authentication test")
	def testAuthenticationProcess(self, postData=None, appVars=None, person=None):
	
		authinfo_ = appVars.authentication
		self.log(authinfo_)
		
		if (authinfo_ == None):
			return FunctionResponse(HTTP_SESSION_FAILURE, TYPE_JSON, "123")

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"message":"hello"})
