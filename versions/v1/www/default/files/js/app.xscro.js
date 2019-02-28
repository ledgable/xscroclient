
App.Xscro = {
	
	hasInit : false,
	
	__preinit : function() {
		if (this.hasInit) return;
		this.hasInit = true;
	},
	
	refresh : function(oEvent, oArgs) {
		$('*').triggerHandler('page-refresh', null);
	}
	
};

App.Xscro.Notify = {
	
	processTransactions : function(oEvent, oArgs) {
		
		var transactions = oArgs.transactions;
		
		if (transactions != null && transactions != 'undefined') {
			
			var count = transactions.length;
			
			for (var counter=0; counter<count; counter++) {
				var transaction = transactions[counter];
			}
			
		}
		
		$('*').triggerHandler('page-refresh', null);
		
	}
	
};

App.Xscro.Tokens = {
	
	mintNewToken : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'token__info'});
		oData.chainid = oArgs.chainid;
		
		var oRequest = {actions:[{action:'mintNewToken', data:oData}]};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	transferToken : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'token__info'});
		oData.chainid = oArgs.chainid;
		oData.tokenid = oArgs.tokenid;
		
		var oRequest = {actions:[{action:'transferToken', data:oData}]};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	destroyToken : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'token__info'});
		oData.chainid = oArgs.chainid;
		oData.tokenid = oArgs.tokenid;
		
		var oRequest = {actions:[{action:'destroyToken', data:oData}]};
		$('*').triggerHandler('handle-app', oRequest);
		
	}
	
	
};

$(document).ready(function() {
				  
				  App.Xscro.__preinit();
				  
				  });

