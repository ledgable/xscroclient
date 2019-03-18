

App.Security = {
	
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
	},
	
	copyToClipboard : function(oEvent, oArgs) {
		
		// clear selection if these is already something selected
		
		if (window.getSelection) {
			if (window.getSelection().empty) {  // Chrome
				window.getSelection().empty();
			} else if (window.getSelection().removeAllRanges) {  // Firefox
				window.getSelection().removeAllRanges();
			}
		} else if (document.selection) {  // IE?
			document.selection.empty();
		}
		
		var target = $(oArgs.field)[0];
		var visible = $(oArgs.field).is(":visible");
		
		if (!visible) {
			$(oArgs.field).css({"display":"block"});
		}
		
		var currentFocus = document.activeElement;
		
		var oElement = target.tagName.toLowerCase();
		var type = (oElement=='input') ? $(target).attr('type') : oElement;
		var succeed;
		
		switch (type) {
			case "div":
			case "span": {
				var range = document.createRange();
				range.selectNode(target);
				window.getSelection().addRange(range);
				break;
			}
			default: {
				target.focus();
				target.setSelectionRange(0, target.value.length);
				break;
			}
		}
		
		// copy the selection
		try {
			succeed = document.execCommand("copy");
		} catch(e) {
			succeed = false;
		}
		
		if (!visible) {
			$(oArgs.field).css({"display":"none"});
		}
		
		if (succeed) {
			App.Notify.showMessage(true, "The item was copied to the clipboard");
			setTimeout(function(){ App.Core.Application.__clearMsg(); return true; }, '3000');
		} else {
			App.Notify.showMessage(false, "Operation failed");
			setTimeout(function(){ App.Core.Application.__clearMsg(); return true; }, '3000');
		}
		
	},
	
	cancelDialog : function(oEvent, oArgs) {
		App.UI.DialogManager.close();
	},
	
};


App.Security.User = {

	logout : function(oEvent, oArgs) {
	
		var oData = {};
		var oRequest = {actions:[{action:'user.logout',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	login : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'user__info'});
		
		var sessionId = App.Core.Security.sessionId;
		var md5pass = $.md5(oData.password);
		var tokentosend = $.md5((sessionId + ":" + md5pass));
		
		oData.password = tokentosend;
		
		var oRequest = {actions:[{action:'user.login',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},

};


$(document).ready(function() {
				  
	App.Security.__preinit();
				  
});


