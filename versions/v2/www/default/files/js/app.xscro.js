
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

$(document).ready(function() {
				  
				  App.Xscro.__preinit();
				  
				  });

