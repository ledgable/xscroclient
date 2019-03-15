
/*
 * Copyright (C) 2016-2018 Ledgable BV
 * All Rights Reserved
 * No copying, duplication or replication of code permitted without
 * express permission of Ledgable BV
 */

App.Validate = {
	
	hasInit : false,
	aPopulate : [],
	
	commonValidators : new Hashtable(),
	
	aItems : [],
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		this.setupRegExp();
		
		$(document).delegate('form', 'keypress', function(oEvent){
			if (oEvent.which == 13) {
				var allowEnter = $(oEvent.target).attr("data-allowreturn");
				if ((allowEnter == null) || (allowEnter == 'undefined')) {
					allowEnter = false;
				} else {
					allowEnter = parseInt(allowEnter) == 1;
				}
				if (!allowEnter) oEvent.preventDefault();
			}
		});

		$(document).delegate('.controldata :input:not([readonly])', 'focusin', function(oEvent){ App.Validate.clearDefault(oEvent); });
		$(document).delegate('.controldata :input:not([readonly])','focusout change', function(oEvent) { App.Validate.__checkContent(oEvent); });
		$(document).delegate('.controldata :input', 'change keyup', function(oEvent) { App.Validate.__formChecker(oEvent); });
		
		$(document).delegate('.controldata textarea:not([readonly])', 'focusin', function(oEvent){ App.Validate.clearDefault(oEvent); });
		$(document).delegate('.controldata textarea:not([readonly])','focusout change', function(oEvent) { App.Validate.__checkContent(oEvent); });
		$(document).delegate('.controldata textarea', 'change', function(oEvent) { App.Validate.__formChecker(oEvent); });

		$(document).delegate('select.autopop[data-datasource!=""][data-target!=""]', 'change', function(oEvent) { App.Validate.autopopulate(oEvent); });
		$(document).delegate('select', 'change', function(oEvent) { App.Validate.checkVerified(oEvent.target); });
		
		$('*').bind('page-refresh window-refresh dialog-refresh', function(object, data) {
					App.Validate.refresh(data);
				});
		
		$('*').bind('html-changed', function(object, data) {
					App.Validate.refresh(data);
				});

	},
	
	refresh : function(target) {
		
		if ((target=='undefined') || (target==null)) target = null;
		
		if ((target==null) || (typeof(target) == 'object')) {
			$('body').find('select').each(function() {
										  App.Validate.checkVerified(this);
										  });
			$('body').find(':input').each(function() {
										  App.Validate.__checkContent(this);
										  });
		} else {
			$(target).find('select').each(function() {
										  App.Validate.checkVerified(this);
										  });
			$(target).find(':input').each(function() {
										  App.Validate.__checkContent(this);
										  });
		}
		
	},
	
	resetDefault : function(oEvent, oArgs) {
	
		if((oArgs == 'undefined') || (oArgs == null)) {
			oArgs = {};
			oArgs.form = $('#mainbody');
		}
		
		var items = $('#'+ oArgs.form).find(':input[type="text"][data-default|=""]');
		if (items.length > 0) {
			for (var counter=0; counter< items.length; counter++) {
				
				var defaultval = $(items[counter]).attr('data-default');
				
				switch ($(items[counter]).attr('type')) {
				
					case 'text': {
						$(items[counter]).val(defaultval);						
						break;				
					}
					
					default: {
						break;
					}
				
				}				
			}
		}
		
	},
	
	checkVerified : function(target) {
		
		var classes = $("option", target).filter(":selected").attr('class');
		var found = false;
		
		if ((classes != null) && (classes != 'undefined')) {
			
			var classesSplit = classes.split(" ");
			for (var counter=0; counter<classesSplit.length; counter++) {
				if (classesSplit[counter] == "verified") {
					found = true;
				}
			}
			
			if (found) {
				if (!$(target).hasClass('verified')) {
					$(target).addClass('verified');
				}
			} else {
				if ($(target).hasClass('verified')) {
					$(target).removeClass('verified');
				}
			}
			
		}
		
	},
	
	setupRegExp : function() {
		
		var sequences = [
		                 	{ 'name':'textonly', 'value':'[a-zA-Z0-9]+' },
							{ 'name':'username', 'value':'[a-zA-Z0-9._-]+' },
							{ 'name':'fieldname', 'value':'[a-zA-Z0-9]+[a-zA-Z0-9_.\-]+' },
							{ 'name':'website', 'value':'([da-z.-]+).([a-z.]{2,6})([/w .-]*)*' },
		                 	{ 'name':'alltext', 'value':'[a-zA-Z0-9_. \-]+' },
		                 	{ 'name':'alltextmin', 'value':'[a-zA-Z0-9]+[a-zA-Z0-9_. \-]{{0}}' },
							{ 'name':'alltextcomma', 'value':'[a-zA-Z0-9_., \-]+' },							
		                 	{ 'name':'textminmax', 'value':'[a-zA-Z0-9]{{0},{1}}' },
		                 	{ 'name':'textmin', 'value':'[a-zA-Z0-9]{{0}}' },
		                 	{ 'name':'email', 'value':'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}' },
							{ 'name':'zip_dutch', 'value':'[0-9]{4}[a-zA-Z]{2}' },
							{ 'name':'digits', 'value':'[0-9]+' },
							{ 'name':'2fa', 'value':'[0-9]{6}' },
							{ 'name':'color', 'value':'[a-fA-F0-9]{6}' },
							{ 'name':'decimal', 'value':'[0-9.]+' },
							{ 'name':'uuid', 'value':'[a-fA-F0-9]{32}' },
							{ 'name':'hex', 'value':'[a-fA-F0-9]+' },
							{ 'name':'phone', 'value':'[\+0-9]+' },
							{ 'name':'anychar', 'value':'.+' },
							{ 'name':'quikname', 'value':'[a-zA-Z]+[a-zA-Z0-9_.]+' }
		                 ];
		
		for (var counter=0; counter<sequences.length; counter++) {
			this.commonValidators.add(sequences[counter].name, sequences[counter].value);
		}
				
	},
	

	__formChecker : function(oEvent) {
		
		if (oEvent == null) return;		
		var parent = $(oEvent.currentTarget).parents('.controldata'); // look for the form tag
		
		if (parent==null) return; // no form, no point !		
		var reqInputs = $(':input[data-req="true"]', parent);
		var failed = false;
		
		if (reqInputs.length > 0) {
			var counter = 0;
			// i need to validate these inputs....
			while (counter < reqInputs.length) {
				failed = !($(reqInputs[counter]).hasClass('ok'));
				if (failed) break;
				counter++;
			}
			if (failed) { 
				if ($(parent).hasClass('ok')) $(parent).removeClass('ok');
				if (!$(parent).hasClass('error')) $(parent).addClass('error');
			} else {
				if ($(parent).hasClass('error')) $(parent).removeClass('error');
				if (!$(parent).hasClass('ok')) $(parent).addClass('ok');
			}
		}
				
	},
	
	__checkContent : function(oEvent) {
		
		if (oEvent == null) return;

		var target = oEvent;
		if (oEvent.currentTarget != null) {
			target = oEvent.currentTarget;
		}
		
		var defaultval = $(target).attr('data-default');
		if ((defaultval == 'undefined') || (defaultval == null)) defaultval = '';
		
		switch (oEvent.type) {
		
			case 'focusin': {
				if ($(target).val() == defaultval) $(target).val('');
				break;
			}
			
			case 'focusout': {
				if ($(target).val() == '') $(target).val(defaultval);
				break;
			}
			
			default: {
				break;
			}
		
		}		
		
		var oElement = target.tagName.toLowerCase();
		var type = (oElement=='input') ? $(target).attr('type') : oElement;
		
		var status = '';
		var valueToValidate = $(target).val();
		
		var required = $(target).attr('data-req');
		required = ((required == 'undefined') || (required == null)) ? false : required.bool(); 
		
		switch (type)
		{
		
			case 'password':
			case 'text': {

				var validatorIn = $(target).attr('data-validator');
				var defaultval = $(target).attr('data-default');
				
				if ((validatorIn=='undefined') || (validatorIn == null) || (validatorIn == '')) return;
								
				var regExp = null;
				
				var exp = '';
				var posOfHash = validatorIn.indexOf('#');
				
				if (posOfHash != -1) {
					var vars = validatorIn.substring(posOfHash+1);
					vars = vars.split(',');
					exp = this.commonValidators.get(validatorIn.substring(0, posOfHash)).formatArray(vars);
				} else {
					exp = this.commonValidators.get(validatorIn);
				}

				regExp = new RegExp(exp);				
				if (regExp == null) return; // no validator
												
				var result = regExp.exec(valueToValidate);		
				
				if ((valueToValidate=='') && required) {
					status = 'error';
				} else {
					if (valueToValidate == defaultval) {
						status = 'default';
					} else {
						if ($.isArray(result)) {
							status = (result[0] == valueToValidate) ? 'ok' : 'error';
						} else {
							status = (result == valueToValidate) ? 'ok' : 'error';
						}
					}
				}
				
				break;
			}
			
			case 'select':{
				if ((valueToValidate=='') && required) {
					status = 'error';
				} else {		
					status = 'ok';
				}
				break;
			}

			default: {				
				// unsupported object type (at the moment)...
				break;
			}
			
		}
								
		switch (status) {
		
			case "ok": {
				if ($(target).hasClass('default')) {
					$(target).removeClass('default');
				}
				if (!$(target).hasClass('ok')) {
					$(target).addClass('ok');
				}
				if ($(target).hasClass('error')) {
					$(target).removeClass('error');
				}				
				break;
			}
				
			case "default": {
				if ($(target).hasClass('error')) {
					$(target).removeClass('error');
				}
				if ($(target).hasClass('ok')) {
					$(target).removeClass('ok');
				}
				if (!$(target).hasClass('default')) {
					$(target).addClass('default');
				}
				break;
			}
			
			case "error": {
				if ($(target).hasClass('default')) {
					$(target).removeClass('default');
				}
				if ($(target).hasClass('ok')) {
					$(target).removeClass('ok');
				}
				if (!$(target).hasClass('error')) {
					$(target).addClass('error');
				}						
				break;
			}
			
			default: {
				// no error or condition to set
				break;
			}
		
		}
		
	},
	
	clearDefault : function(oEvent){
		if(!$(oEvent.currentTarget) == true) return;
		var defaultval = $(oEvent.currentTarget).data('default');
		if ((defaultval == 'undefined') || (defaultval == null)) defaultval = '';
		if ($(oEvent.currentTarget).val() == defaultval) {
			$(oEvent.currentTarget).val('');
			if ($(oEvent.currentTarget).hasClass('default')) {
				$(oEvent.currentTarget).removeClass('default');
			}
		}
	},
	
	autopopulate : function(oEvent) {
				
		var datasource = $(oEvent.currentTarget).attr('data-datasource');
		if ((datasource == 'undefined') || (datasource == null)) datasource = null;
		
		var target = $(oEvent.currentTarget).attr('data-target');
		if ((target == 'undefined') || (target == null)) target = null;

		var propname = $(oEvent.currentTarget).attr('data-propname');
		if ((propname == 'undefined') || (propname == null)) propname = 'display';

		if ((target==null) || (datasource==null)) return;
				
		var currentVal = $(oEvent.currentTarget).val();
		if ((currentVal != '') && (currentVal != null)) {
			datasource += '/' + currentVal;
		}
				
		$.ajax({
			   
			type: "get",
			dataType: "text",
			error: function(data) {				
			},
			success: function(datain) {
				
				var data = jQuery.parseJSON(datain);
				if (data == null) return;
												
				var oHtml = '';
				if (data.length >0) {
					for (var counter=0; counter< data.length; counter++) {
						oHtml += '<option value="'+ data[counter].id +'">'+ data[counter][propname] +'</option>';												
					}
				}
				
				$('#'+ target).html(oHtml);
				$('#'+ target).change();
				
			},				
			url: datasource, 
			data: {}
		});	
		
	}
			
};


$(document).ready(function() {
	
	App.Validate.__preinit();
	
});
