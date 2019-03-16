
from www.__common.controllers.XscroController import *

class CallBackController(XscroController):
	
	def __init__(self, handler, session, query=None, isajax=False):
		XscroController.__init__(self, handler, session, query, isajax)


	@endpoint(1, True, True, None, "post", "^/callbackwatcher/(?P<chainid>[0-9a-z][^-&*/\%]*)", "check watcher works")
	def callBackWatcher(self, postData=None, appVars=None, chainid=None):
		
		MULTIPLIER = 2.0 # change the multiple 1 eth in, 5 tokens out (for instance)
		HOSTWALLET = None # replace with the receiving wallet address
		
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
