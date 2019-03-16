
App.User = {
	
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
	},
	
	refresh : function(oEvent, oArgs) {
		$('*').triggerHandler('page-refresh', null);
	}
	
};


App.User.Security = {
	
	changePassword : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'manage__password'});

		oData.currentpassword = $.md5(oData.currentpassword);
		oData.newpassword = $.md5(oData.newpassword);
		oData.confirmpassword = $.md5(oData.confirmpassword);

		if (oData.newpassword == "" || oData.newpassword == null || oData.newpassword == 'undefined') {
			App.Notify.showMessage(0, "The passwords do not match");
			return;
		}
		
		if (oData.newpassword != oData.confirmpassword) {
			App.Notify.showMessage(0, "The passwords do not match");
			return;
		}

		if (oData.currentpassword == oData.newpassword) {
			App.Notify.showMessage(0, "Your new password is the same as your current password");
			return;
		}
		
		var oRequest = {actions:[{action:'walletuser.changepassword',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	showChangePassword : function(oEvent, oArgs) {
		
		App.UI.DialogManager.createDialog(null, "/show/dialog/changepassword", {'width':650, 'height':0});
		
	},
	
	logout : function(oEvent, oArgs) {
		
		var oData = {};
		var oRequest = {actions:[{action:'walletuser.userlogout',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	login : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'user__info'});
		oData.password = $.md5(oData.password);
		
		var oRequest = {actions:[{action:'walletuser.userlogin',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
};


$(document).ready(function() {
				  
	App.User.__preinit();

});
