
from modules.helpers import *
from urllib.parse import unquote

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


	@endpoint(1, True, True, None, "gateway", "^payment.login", "Login Wallet User")
	def paymentLogin(self, postData=None, appVars=None, params=None, content=None):

		payment_ = self.session.payment

		if (payment_ != None):
			
			walletid_ = params.walletid
			digest_ = params.password
			chainid_ = params.chainid
			
			nonce_ = "%s:%s:%s" % (chainid_, digest_, walletid_)
			
			kpt1_ = hashlib.md5()
			kpt1_.update(nonce_.encode(UTF8))
			kpt1out_ = kpt1_.hexdigest()
			
			xscro_ = ApplicationManager().get("xscro")
				
			if (xscro_ == None):
				pass

			else:
				
				if (chainid_ in xscro_.containers.keys()):
					container_ = xscro_.containers[chainid_]
					
					if (container_):
						walletids_ = list(container_.wallets.keys())
						
						if (walletid_ in walletids_):
							
							wallet_ = container_.walletFor(walletid_)
							success_ = (kpt1out_ == wallet_.digest)
							
							if (success_):
								payment_.sender = {"walletid":walletid_}
								payment_.page = "balance"
								payment_.balance = float(wallet_.balance)
								payment_.remaining = (wallet_.balance - payment_.amount)
								
								self.session.payment = payment_

								return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Logged In", "refresh":"window"})
					
						else:
							pass # wallet isnt registered...
			
					return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Credentials are invalid"})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Something critical went wrong"})

	
	@endpoint(1, True, True, None, "gateway", "^payment.cancel", "Cancel Wallet Payment")
	def paymentCancel(self, postData=None, appVars=None, params=None, content=None):
		
		payment_ = None
		
		if (self.session.payment != None):
			payment_ = self.session.payment
			
		if (payment_ != None):
			redirecttocancel_ = None
			callbackroot_ = payment_.callbacks
			paymenttoken_ = payment_.paymenttoken
			
			# we cancel the payment token as payment has been cancelled...
			
			if (paymenttoken_ != None):
				chainid_ = payment_.chainid
				senderwallet_ = payment_.sender.walletid
				success_, response_ = XscroController.ackTransaction(self, chainid_, senderwallet_, paymenttoken_, 0)
		
			self.session.payment = None
			redirecttocancel_ = callbackroot_.cancel
			
			if (redirecttocancel_ != None):
				
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Payment Cancelled", "refresh":"redirect", "url":redirecttocancel_})
			
		return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)

			
	@endpoint(1, True, True, None, "gateway", "^payment.accept", "Accept Wallet Payment")
	def paymentAccept(self, postData=None, appVars=None, params=None, content=None):
		
		payment_ = self.session.payment
		
		if (payment_ != None):
			
			senderwallet_ = payment_.sender.walletid
			chainid_ = payment_.chainid
			transactionid_ = payment_.transactionid
			recipientwallet_ = payment_.recipient.walletid
			volume_ = payment_.amount
			price_ = payment_.default("price" , 0.0)
			paymentdesc_ = payment_.description
			
			if (paymentdesc_ == None):
				paymentdesc_ = "Payment requested"
					
			ipaddress_ = self.session.ip_address
			traderid_ = "eSelfService"
						
			success_, paymenttoken_, msg_ = XscroController.transferValue(self, chainid_, senderwallet_, recipientwallet_, transactionid_, volume_, price_, paymentdesc_, ipaddress_, traderid_)
			
			if (success_):
				payment_.page = "confirm"
				payment_.paymenttoken = paymenttoken_
				self.session.payment = payment_
				
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Payment Accepted", "refresh":"window"})
			
			else:
				return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":msg_})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Something critical went wrong"})
	
	
	@endpoint(1, True, True, None, "gateway", "^payment.completed", "Return to vendor site")
	def paymentCompleted(self, postData=None, appVars=None, params=None, content=None):
	
		payment_ = None
		
		if (self.session.payment != None):
			payment_ = self.session.payment
			self.session.payment = None
	
		if (payment_ != None):
			
			callbackroot_ = payment_.callbacks
			
			if (callbackroot_ != None) and (payment_.ack == 1):
				
				redirecttosuccess_ = callbackroot_.success
				
				if (redirecttosuccess_ != None):
					return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Redirecting to client portal", "refresh":"redirect", "url":redirecttosuccess_})

		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Something critical went wrong"})
			

	@endpoint(1, True, True, None, "gateway", "^payment.confirm", "Confirm Wallet Payment")
	def paymentConfirm(self, postData=None, appVars=None, params=None, content=None):
	
		payment_ = None
		
		if (self.session.payment != None):
			payment_ = self.session.payment
	
		if (payment_ != None):
		
			chainid_ = payment_.chainid
			paymenttoken_ = payment_.paymenttoken
			senderwallet_ = payment_.sender.walletid
			callbackroot_ = payment_.callbacks
			
			if (callbackroot_ != None):
				
				redirecttonotify_ = callbackroot_.notify
				
				redirecttofail_ = callbackroot_.fail
				success_, response_ = XscroController.ackTransaction(self, chainid_, senderwallet_, paymenttoken_, 1)
			
				if (success_):
					payment_.page = "finish"
					payment_.ack = 1
					self.session.payment = payment_
					return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":1, "mode":"notify", "message":"Payment Confirmed", "refresh":"window"})
				
				else:
					return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":"Payment Failed - Redirecting to client portal", "refresh":"redirect", "url":redirecttofail_})
				
		return FunctionResponse(HTTP_OK, TYPE_JSON, {"status":0, "mode":"notify", "message":response_})
	

	@endpoint(96, True, True, None, "post", "^/pay", "Post a payment")
	def payRedirectPage(self, postData=None, appVars=None):
		
		datain_ = unquote(postData.decode(UTF8))
		
		paramsin_ = extdict()

		if (datain_ != None):
			
			splitout_ = datain_.split("&")
			
			if (len(splitout_) > 0):
				for string_ in splitout_:
					key_, value_ = string_.split("=")
					value_ = unquote_plus(value_)
					paramsin_[key_] = value_
	
		if (self.session.payment == None) or (len(paramsin_) > 0):
			
			payment_ = None
			
			if (self.session.payment != None) and (self.session.payment.page != "finish"):
				
				payment_ = self.session.payment
		
				if (paramsin_.transactionid == payment_.transactionid):
		
					setattrs(payment_,
						recipient = {"walletid":paramsin_.recipientwallet, "displayas":paramsin_.recipientdisplay},
						description = paramsin_.description,
						amount = float(paramsin_.amount),
						token = paramsin_.currency,
						callbacks = {"success":paramsin_.callbacksuccess, "fail":paramsin_.callbackfailure, "cancel":paramsin_.callbackcancel}
						)
	
				else:

					if (paramsin_.transactionid == None) and (payment_.transactionid != None):
					
						# we continue with the old transaction
						pass
					
					else:
						transactionid_ = paramsin_.default("transactionid", self.uniqueId)

						payment_ = extdict({"transactionid":transactionid_, "chainid":paramsin_.chainid,
							"recipient":{"walletid":paramsin_.recipientwallet, "displayas":paramsin_.recipientdisplay},
							"sender":{"walletid":paramsin_.default("sender", "")},
							"description":paramsin_.description,
							"amount":float(paramsin_.amount), "token":paramsin_.currency,
							"callbacks":{"success":paramsin_.callbacksuccess, "fail":paramsin_.callbackfailure, "cancel":paramsin_.callbackcancel},
							"pagename":"default"
							})

			else:
			
				transactionid_ = paramsin_.default("transactionid", self.uniqueId)
				
				payment_ = extdict({"transactionid":transactionid_, "chainid":paramsin_.chainid,
					"recipient":{"walletid":paramsin_.recipientwallet, "displayas":paramsin_.recipientdisplay},
					"sender":{"walletid":paramsin_.default("sender", "")},
					"description":paramsin_.description,
					"amount":float(paramsin_.amount), "token":paramsin_.currency,
					"callbacks":{"success":paramsin_.callbacksuccess, "fail":paramsin_.callbackfailure, "cancel":paramsin_.callbackcancel},
					"pagename":"default"
					})
						
			self.session.payment = payment_

		return self.payPage(postData, appVars)

			
	@endpoint(97, True, True, None, "get", "^/pay", "Fetch payment page by name")
	def payPage(self, postData=None, appVars=None):

		payment_ = None
		
		if (appVars.payment != None):
			
			try:
				encoded_ = appVars.payment				
				paymentjson_ = decode_base64(bytes(encoded_, UTF8)).decode(UTF8)
				
				payment_ = extdict.fromJson(paymentjson_)
				payment_.page = "default"
				
				self.session.payment = payment_
			
			except Exception as exception:
				self.log(exception)
				self.session.payment = None
			
		else:
			if (self.session.payment != None):
				payment_ = self.session.payment

		if (payment_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
		
		pagename_ = "default"

		if (payment_.page != None):
			pagename_ = payment_.page

		callbackroot_ = payment_.callbacks

		if (callbackroot_ != None):
			
			appVars.payment = payment_
			content_ = self.loadContent(("payments/%s.html.py" % pagename_), appVars)
		
			if (content_ != None):
				contentout_ = content_
			
				if (self.isajax == False):
					contentout_ = self.appendView("template_web.html", content_, appVars)
			
				return FunctionResponse(HTTP_OK, TYPE_HTML, contentout_)
		
		return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
