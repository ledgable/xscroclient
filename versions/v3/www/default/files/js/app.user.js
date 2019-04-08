
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
	
	newuser : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'user__info'});
		
		var md5pass = $.md5(oData.password);
		var md5pass_confirm = $.md5(oData.confirm_password);
		
		if (md5pass != md5pass_confirm) {
			App.Notify.showMessage(false, "The passwords do not match");
			return;
			
		} else if (md5pass == $.md5("Password")) {
			App.Notify.showMessage(false, "You must specify a password");
			return;
		}
		
		oData.password = md5pass;
		
		var oRequest = {actions:[{action:'user.newuser',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
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
		
	}
	
};

App.User.Transactions = {
	
	ackTransaction : function(oEvent, oArgs) {
		
		var oData = {};
		oData.token = oArgs.token;
		oData.code = oArgs.code;
		
		var oRequest= {actions:[{action:'walletuser.acktransaction', data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	}
	
};

App.User.Tokens = {
	
	showTransfer : function(oEvent, oArgs) {
		
		var transfers = [];
		transfers.push({"uid":new String().guid()});
		App.UI.DataServices.dataitems.add("newtransfers", transfers);
		
		App.UI.DialogManager.createDialog(null, "/show/dialog/newtransfer", {'width':650, 'height':0});
		
	},
	
	updateTransfer : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'edit__newtransfer'});
		var uid = oArgs.uid;
		
		var walletid = oData["walletid_" + uid];
		if (walletid == null || walletid == 'undefined') walletid = null;
		
		var volume = oData["volume_" + uid];
		if (volume == null || volume == 'undefined') volume = 0;

		var ppt = oData["ppt_" + uid];
		if (ppt == null || ppt == 'undefined') ppt = 0;

		var transfers = App.UI.DataServices.dataitems.get("newtransfers");
		
		for (var counter=0; counter < transfers.length; counter++) {
			
			var transfer = transfers[counter];
			
			if (transfer.uid == uid) {
				transfer.walletid = walletid;
				transfer.volume = volume;
				transfer.ppt = ppt;
				transfers[counter] = transfer;
			}
			
		}
		
		App.UI.DataServices.dataitems.add("newtransfers", transfers);
		console.info(transfers);
		
	},
	
	removeLine : function(oEvent, oArgs) {
		
		var uid = oArgs.uid;
		var transfers = App.UI.DataServices.dataitems.get("newtransfers");
		if (transfers == null || transfers == 'undefined') {
			transfers = [];
		}
		
		var index = -1;
		for (var counter=0; counter < transfers.length; counter++) {
			var transfer = transfers[counter];
			if (transfer.uid == uid) {
				index = counter;
			}
		}
		
		if (index != -1) {
			transfers[index]
			transfers.splice(index,1);
			App.UI.DataServices.dataitems.add("newtransfers", transfers);
			var id = $(oEvent).parents("section[data-component='repeater']").attr("id");
			$('*').triggerHandler('data-refresh', "#" + id);
		}
		
	},
	
	transferFunds : function(oEvent, oArgs) {

		var oData = {};
		var formData = $('*').triggerHandler('do-formdata', {'target':'edit__newtransfer'});
		var transfers = App.UI.DataServices.dataitems.get("newtransfers");
		
		var out = [];
		
		if (transfers != null && transfers != 'undefined') {
			
			for (var counter=0; counter<transfers.length; counter++) {
				var transfer = transfers[counter];
				if (transfer.volume > 0 && transfer.walletid != null && transfer.ppt >= 0) {
					out.push({"walletid":transfer.walletid, "transid":transfer.uid, "volume":transfer.volume, "ppt":transfer.ppt});
				}
			}
			
		}
	
		if (out.length > 0) {
			oData.note = formData.note;
			oData.transfers = out;
			var oRequest = {actions:[{action:'walletuser.transferfunds', data:oData}], jw:App.Core.Security.code};
			$('*').triggerHandler('handle-app', oRequest);
		}
		
	},
	
	addTransferLine : function(oEvent, oArgs) {
		
		var transfers = App.UI.DataServices.dataitems.get("newtransfers");
		if (transfers == null || transfers == 'undefined') {
			transfers = [];
		}
		
		transfers.push({"uid":new String().guid()});
		App.UI.DataServices.dataitems.add("newtransfers", transfers);
		
		var id = $(oEvent).parents("section[data-component='repeater']").attr("id");
		
		$('*').triggerHandler('data-refresh', "#" + id);
		
	}
	
};


$(document).ready(function() {
				  
	App.User.__preinit();

});
