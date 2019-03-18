
from www.default.controllers.PaymentController import *

class AdminController(PaymentController):

	def __init__(self, handler, session, query=None, isajax=False):
		PaymentController.__init__(self, handler, session, query, isajax)

	
	@endpoint(98, True, True, None, "get", "^/admin", "Fetch admin page by name")
	def adminDefaultPage(self, postData=None, appVars=None):
	
		return self.adminPage(postData, appVars, None)

	
	@endpoint(97, True, True, None, "get", "^/admin/(?P<pagename>[^ ]*)", "Fetch admin page by name")
	def adminPage(self, postData=None, appVars=None, pagename=None):
		
		username_ = self.session.username
		
		if (pagename != None):
			if (pagename[0:1:] == "/"):
				pagename = pagename[1:]

		content_ = None
		
		if (username_ == None):
			content_ = self.loadContent("__bits/auth/login.html.py", appVars)

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
