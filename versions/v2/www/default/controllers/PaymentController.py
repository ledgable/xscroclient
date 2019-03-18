
from www.__common.controllers.XscroController import *

#		payment_ = extdict({"transactionid":"12345", "chainid":"12345",
#			"recipient":{"walletid":"1234", "displayas":"Icecat NV"},
#			"sender":{"walletid":"0xE80A9aBF289549F5a0F1F6e56871aF88837ACEd5"},
#			"description":"This is a test transaction for data-sheet purchases - maybe some other text here",
#			"amount":30.0, "token":"icury",
#			"callbacks":{"success":"", "fail":"", "cancel":""}
#			})

#		strpayment_ = payment_.toJson()
#		base64encoded_ = base64.b64encode(bytes(strpayment_, UTF8))
#		self.log(base64encoded_)

class PaymentController(XscroController):

	def __init__(self, handler, session, query=None, isajax=False):
		XscroController.__init__(self, handler, session, query, isajax)

	
	@endpoint(1, False, True, None, "get", "^/api/tokens", "Get tokens")
	def getTokensForSession(self, postData=None, appVars=None, chainid=None):
		
		payment_ = self.session.payment
		tokens_ = []
		
		if (payment_ != None):
		
			chainid_ = payment_.chainid
			senderid_ = payment_.sender.walletid
			tokens_ = self.allTransactions(chainid_, senderid_)
			
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"tokens":tokens_})
	

	@endpoint(1, True, True, None, "gateway", "^payment.login", "Login Wallet User")
	def paymentLogin(self, postData=None, appVars=None, params=None, content=None):

		payment_ = self.session.payment

		if (payment_ != None):
			
			wallet_ = params.walletid
			digest_ = params.password
			chainid_ = params.chainid
			
			nonce_ = "%s:%s:%s" % (chainid_, digest_, wallet_)
			
			kpt1_ = hashlib.md5()
			kpt1_.update(nonce_.encode(UTF8))
			kpt1out_ = kpt1_.hexdigest()
			
			xscro_ = ApplicationManager().get("xscro")
				
			if (xscro_ == None):
				pass

			else:
				wallets_ = list(xscro_.wallets_.keys())
				success_ = False
				
				if (wallet_ in wallets_):
					token_ = xscro_.wallets_[wallet_]
					success_ = (kpt1out_ == token_)
			
					if (success_):
						payment_.sender = {"walletid":wallet_}
						payment_.page = "balance"
						self.session.payment = payment_

						return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Logged In", "refresh":"internal", "url":"/pay"})
							
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Credentials are invalid"})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Something critical went wrong"})

	
	@endpoint(1, True, True, None, "gateway", "^payment.cancel", "Cancel Wallet Payment")
	def paymentCancel(self, postData=None, appVars=None, params=None, content=None):
		
		payment_ = None
		
		if (self.session.payment != None):
			payment_ = self.session.payment
	
		if (payment_ != None):
			redirecttocancel_ = None
			
			try:
				redirecttocancel_ = payment_.callbacks.cancel
			
			except Exception as exception:
				pass
			
			if (redirecttocancel_ != None):
				
				self.session.payment = None
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Payment Cancelled", "refresh":"redirect", "url":redirecttocancel_})
			
		return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
			
			
	@endpoint(1, True, True, None, "gateway", "^payment.accept", "Accept Wallet Payment")
	def paymentAccept(self, postData=None, appVars=None, params=None, content=None):
		
		tokenid_ = params.tokenid
		
		if (tokenid_ == None):
			return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"You must select a token to which to pay with"})
		
		payment_ = self.session.payment
		
		if (payment_ != None):
			
			chainid_ = payment_.chainid
			transactionid_ = payment_.transactionid
			recipientwallet_ = payment_.recipient.walletid
			tokenselected_ = tokenid_
			volume_ = payment_.amount
			paymentdesc_ = "Some Payment Description"
			ipaddress_ = self.session.ip_address
			traderid_ = "ePurchase"
						
			success_, token_, msg_ = self.transferToken(chainid_, tokenselected_, recipientwallet_, transactionid_, volume_, 0.0, paymentdesc_, ipaddress_, traderid_)
			
			if (success_):
				payment_.page = "confirm"
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Payment Accepted", "refresh":"internal", "url":"/pay"})
			
			else:
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":msg_})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Something critical went wrong"})
			

	@endpoint(1, True, True, None, "gateway", "^payment.confirm", "Confirm Wallet Payment")
	def paymentConfirm(self, postData=None, appVars=None, params=None, content=None):
	
		payment_ = None
		
		if (self.session.payment != None):
			payment_ = self.session.payment
	
		if (payment_ == None):
			pass
		
		
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Payment Confirmed - Redirecting to client portal", "refresh":"window"})
	
	
	@endpoint(97, True, True, None, "get", "^/pay", "Fetch payment page by name")
	def payPage(self, postData=None, appVars=None):

		payment_ = None

		if (appVars.payment != None):
			
			try:
				encoded_ = appVars.payment
				paymentjson_ = base64.b64decode(encoded_).decode(UTF8)
				
				payment_ = extdict.fromJson(paymentjson_)
				payment_.page = "default"
				
				self.session.payment = payment_
			
			except Exception as exception:
				self.session.payment = None
			
		else:
			if (self.session.payment != None):
				payment_ = self.session.payment

		if (payment_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
		
		pagename_ = "default"

		if (payment_.page != None):
			pagename_ = payment_.page
		
		appVars.payment = payment_
		content_ = self.loadContent(("payments/%s.html.py" % pagename_), appVars)
	
		if (content_ != None):
			contentout_ = content_
		
			if (self.isajax == False):
				contentout_ = self.appendView("template_web.html", content_, appVars)
		
			return FunctionResponse(HTTP_OK, TYPE_HTML, contentout_)
		
		return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
