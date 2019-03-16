
App.Admin = {
	
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
	},
	
	refresh : function(oEvent, oArgs) {
		$('*').triggerHandler('page-refresh', null);
	},
	
	switchChain : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'chain__selector'});
		
		var oRequest = {actions:[{action:'admin.switchchain', data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	}
	
};

App.Admin.Transactions = {
	
	ackTransaction : function(oEvent, oArgs) {
		
		var oData = {};
		oData.chainid = oArgs.chainid;
		oData.token = oArgs.token;
		oData.code = oArgs.code;
		
		var oRequest= {actions:[{action:'admin.acktransaction', data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	}
	
};

App.Admin.Wallets = {
	
	showAddWallets : function(oEvent, oArgs) {

		var wallets = [];
		
		wallets.push({"uid":new String().guid()});
		
		App.UI.DataServices.dataitems.add("newwallets", wallets);
		App.UI.DialogManager.createDialog(null, ("/show/dialog/addwallets/" + oArgs.uid), {'width':650, 'height':0});

	},
	
	uploadFile : function(oEvent, oArgs) {
		
		console.info("params = " + oArgs);
		
		var file = oArgs.file;
		
		if (file != null && file != 'undefined') {
			
			var filename = file.filename;
			var extension = filename.substr( (filename.lastIndexOf('.')+1));
			
			switch (extension) {
			
				case "csv": {
					var src = file.src;
					var userlist = [];
					
					try {
						var base64str = src.substr(21);
						var decodedString = atob(base64str);
						var splitstring = decodedString.split("\n");
						var wallets = [];
						
						for (var counter=0; counter < splitstring.length; counter++) {
							
							var line = splitstring[counter];
							var parts = line.split(",")
							
							if (parts.length == 2) {
								var walletid = parts[0];
								var password = parts[1];
								var uid = new String().guid();
								
								wallets.push({"uid":uid, "walletid":walletid, "password":password});
							}
							
						}
						
						App.UI.DataServices.dataitems.add("newwallets", wallets);
						
						$('*').triggerHandler('data-refresh', null);
						
					} catch (ex) {
						App.Notify.showMessage(0, "Data is incorrectly formatted");
					}
					
					break;
				}
					
				default: {
					App.Notify.showMessage(0, "Unsupported filetype");
					break;
				}
				
			}
			
		}
		
	},
	
	createWallets : function(oEvent, oArgs) {
		
		var oData = {};
		oData.chainid = oArgs.uid;
		
		var wallets = App.UI.DataServices.dataitems.get("newwallets");
		var out = [];
		
		if (wallets != null && wallets != 'undefined') {
			
			for (var counter=0; counter<wallets.length; counter++) {
				
				var wallet = wallets[counter];
				
				if (wallet.password != null && wallet.walletid != null) {
					out.push({"walletid":wallet.walletid, "password":$.md5(wallet.password)});
				}
				
			}
			
		}
		
		if (out.length > 0) {
			
			oData.wallets = out;
			var oRequest= {actions:[{action:'admin.addwallets', data:oData}], jw:App.Core.Security.code};
			$('*').triggerHandler('handle-app', oRequest);
		
		}
		
	},
	
	updateWallet : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'edit__addwallets'});
		var uid = oArgs.uid;
		
		var walletid = oData["wallet_" + uid];
		if (walletid == null || walletid == 'undefined') walletid = null;
		
		var password = oData["password_" + uid];
		if (password == null || password == 'undefined') password = null;
		
		var wallets = App.UI.DataServices.dataitems.get("newwallets");
		
		for (var counter=0; counter < wallets.length; counter++) {
			wallet = wallets[counter];
			if (wallet.uid == uid) {
				wallet.password = password;
				wallet.walletid = walletid;
				wallets[counter] = wallet;
			}
		}
		
		App.UI.DataServices.dataitems.add("newwallets", wallets);
		console.info(wallets);
		
	},
	
	addWalletLine : function(oEvent, oArgs) {
		
		var wallets = App.UI.DataServices.dataitems.get("newwallets");
		if (wallets == null || wallets == 'undefined') {
			wallets = [];
		}
		
		wallets.push({"uid":new String().guid()});
		App.UI.DataServices.dataitems.add("newwallets", wallets);
		
		var id = $(oEvent).parents("section[data-component='repeater']").attr("id");
		
		$('*').triggerHandler('data-refresh', "#" + id);
		
	}
	
};


App.Admin.Tokens = {

	showMintToken : function(oEvent, oArgs) {
		
		App.UI.DialogManager.createDialog(null, ("/show/dialog/minttoken/" + oArgs.uid), {'width':650, 'height':0});
		
	},
	
	mintToken : function (oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'edit__minttoken'});
		oData.chainid = oArgs.uid;
		
		var oRequest = {actions:[{action:'admin.minttoken',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	}
	
};


App.Admin.Security = {
	
	logout : function(oEvent, oArgs) {
		
		var oData = {};
		var oRequest = {actions:[{action:'admin.userlogout',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	login : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'user__info'});
		
		var sessionId = App.Core.Security.sessionId;
		var md5pass = $.md5(oData.password);
		var tokentosend = $.md5((sessionId + ":" + md5pass));
		
		oData.password = tokentosend;
		
		var oRequest = {actions:[{action:'admin.userlogin',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
};


$(document).ready(function() {
				  
				  App.Admin.__preinit();
				  
				  });

