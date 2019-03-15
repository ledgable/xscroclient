
# Copyright (C)2017 Ledgable BV
from dataobjects import *
from modules import sessions

from www.__common.controllers.XscroController import *

class DialogsController(XscroController):
	
	def __init__(self, handler, session, query=None, isajax=False):
		XscroController.__init__(self, handler, session, query, isajax)
	
	
	def loadDialog(self, appVars=None, pagename=None):
		
		if (pagename == None) or (pagename == "/"):
			pagename = "default"
		
		content_ = self.loadContent(("__dialogs/dialogs.%s.html.py" % pagename), appVars)
		
		return content_
	
	
	@endpoint(1, True, True, None, "get", "^/show/dialog/(?P<dialogName>[0-9a-z.][^-&*/\%]*)/(?P<argin>[0-9a-z][^-&*/\%]*)", "Show a dialog with optional argument")
	def showDialogWithArg(self, postData=None, appVars=None, dialogName=None, argin=None):
		
		if (argin != None):
			appVars.uidin = argin
		
		content_ = self.loadDialog(appVars, dialogName)
		
		if (content_ == None):
			return FunctionResponse(HTTP_PAGE_DOES_NOT_EXIST, None, None)
		
		return FunctionResponse(HTTP_OK, TYPE_HTML, content_)
	
	
	@endpoint(2, True, True, None, "get", "^/show/dialog/(?P<dialogName>[0-9a-z.][^-&*/\%]*)", "Show a dialog")
	def showDialog(self, postData=None, appVars=None, dialogName=None):
		
		return self.showDialogWithArg(postData, appVars, dialogName, None)

