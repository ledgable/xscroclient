
App.Payments = {
	
	hasInit : false,
	
	__preinit : function() {
		if (this.hasInit) return;
		this.hasInit = true;
	},
	
	refresh : function(oEvent, oArgs) {
		$('*').triggerHandler('page-refresh', null);
	},
	
	cancel : function(oEvent, oArgs) {
		
		var oData = {};
		var oRequest = {actions:[{action:'payment.cancel',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	confirm : function(oEvent, oArgs) {
		
		var oData = {};
		var oRequest = {actions:[{action:'payment.confirm',data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	completed : function(oEvent, oArgs) {
		
		var oData = {};
		
		var oRequest= {actions:[{action:'payment.completed', data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	login : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'wallet__info'});
		
		oData.chainid = oArgs.chainid;
		oData.password = $.md5(oData.password);
		
		var oRequest= {actions:[{action:'payment.login', data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	pay : function(oEvent, oArgs) {
		
		var oData = $('*').triggerHandler('do-formdata', {'target':'payment__info'});

		var oRequest= {actions:[{action:'payment.accept', data:oData}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	}
	
};

$(document).ready(function() {
				  
	App.Payments.__preinit();

});

