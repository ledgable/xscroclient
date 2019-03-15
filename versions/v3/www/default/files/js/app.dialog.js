
/*
 * Copyright (C) 2016/2017 Ledgable BV
 * All Rights Reserved
 * No copying, duplication or replication of code permitted without
 * express permission of Ledgable BV
 */

Dialog = function(callback, url, params) { return this.init(callback, url, params); };

$.extend(Dialog.prototype, {	
	
	id : null,	
	url : null,	
	visible : false,
	params : null,
	callback : null,
	refresh : false,
	onclose : null,
	width: 0,
	height: 0,
	content: function() { return $('#'+this.id+' .dialogbox_content'); },
	
	__loadContent : function() {

		if (this.visible) {
			// clear content just in case...
			$(this.content).html('');		
		}
		
		this.__reload();
		
	},
	
	__reload : function() {
		
		if ((this.url != null) && (this.url != '')) {
			
			var oData = {};
			var id = this.id;
			
			$.ajax({
				type: "get",
				error: function(data) {
					App.UI.DialogManager.__signalLoad('error', id);
				},
				success: function(data) {					
					$('#'+id+' .dialogbox_content').html(data);					
					App.UI.DialogManager.__signalLoad('success', id);
					var oData = ("#" + id);
					$('*').triggerHandler('window-refresh', oData);
				},
				headers: {
					"session_id":App.Core.Security.sessionId
				},
				url: this.url,
				data: oData
			});				
			
		}
		
	},
	
	__showDialog : function() {
		 
		if (this.visible) return;
		this.visible = true;
		
		var params = this.params;		
		var metrics = this.__getWindowMetrics();

		$('#page').addClass("blur");
		$('.dialogbox_overlay[data-link="'+this.id+'"]').css({'display':'block'});
		$('#'+this.id + '.dialogbox').fadeIn('fast');

		if (params.validate != null) App.Forms.doValidation(params.validate.fid);
		if (params.tiny != null) App.UI.Tiny.loadTiny({'id':this.params.tiny.id, 'theme':params.tiny.theme});						

		var refresh = ((params != null) && (params.refresh != null)) ? params.refresh.toString().bool() : this.refresh;
		 
		if (refresh) {
			var oData = ("#" + this.id);
			$('*').triggerHandler('page-refresh', oData);
		}
		 
		if (this.callback) this.callback(this);
		 
	},

	__getWindowMetrics : function() {
		 
		if ($(window) == null) return null;
		return { width: $('.dialogbox_overlay').width(), height: $('.dialogbox_overlay').height() };
		 
	},

	__closeDialog : function() {
		 
		var id = this.id;
		var onclose = this.onclose;
		 
		$('#'+this.id + '.dialogbox').fadeOut('fast', function() {
											  
			$('#'+this.id).remove();
			$('.dialogbox_overlay[data-link="'+id+'"]').remove();
			$('*').triggerHandler('remove-dialog', id);
											  
			if (onclose != null) {
				App.Core.Nav.changeMenu(onclose);
			}
											  
		    $('#page').removeClass("blur");
											  
		});
		 
	},
	
	reload : function() {
		 
		this.__reload();
		 
	},
	
	close : function() {
		 
		if (this.visible) {
			// hide the dialogbox gracefully....
			this.__closeDialog();
			this.visible = false;
		}
		 
	},
	
	init : function(callback, url, params) {
		
		this.id = new String().guid();
		this.url = url;
		this.params = params;
		this.callback = callback;
		
		var windowclass = (params != null) ? params.windowclass : null;
		var contentclass = (params != null) ? params.contentclass : null;
		var hasclose = ((params != null) && (params.hasclose != null)) ? params.hasclose.toString().bool() : true;
		var hasoverlay = ((params != null) && (params.hasoverlay != null)) ? params.hasoverlay.toString().bool() : true;
		
		this.width = ((params != null) && (params.width != null)) ? parseInt(params.width) : 100;		
		this.height = ((params != null) && (params.height != null)) ? parseInt(params.height) : 0;

		if ((windowclass=='undefined') || (windowclass==null)) windowclass='';
		if ((contentclass=='undefined') || (contentclass==null)) contentclass='';
		
		var dialog = '';
		var style = '';

		// if we are using an overlay.... allow this....
		if (hasoverlay) dialog += '<div class="dialogbox_overlay" data-link="'+this.id+'"></div>';
		 
		if (params.height == 0) {
			style = 'width: '+params.width + 'px; height: auto;';
		} else {
			style = 'width: '+params.width + 'px; height: '+params.height + 'px;';
		}
		
		dialog += '<div id="'+this.id+'" class="dialogbox clear'+ (windowclass!=''?' '+windowclass:'') +'" ><div class="dialogbox_shadow"></div><div class="dialogbox_inner" style="'+ style +'" >';
		
		if (hasclose) dialog +=	'<div class="dialogbox_close"></div>';
		 
		dialog += '<div class="dialogbox_content'+ (contentclass!=''?' '+contentclass:'') +'"></div></div></div>';
		
		$('body').append(dialog);

		return this;
		
	}
		
});

App.UI.DialogManager = {
		
	dialogs : new Hashtable(),
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		$('*').bind('remove-dialog', function(oEvent, data) { App.UI.DialogManager.__removeDialog(data); });
		$(document).delegate('.dialogbox_close', 'click', function(oEvent) { App.UI.DialogManager.__close(oEvent); });
		
	},
	
	count : function() {
		
		return (App.UI.DialogManager.dialogs != null) ? App.UI.DialogManager.dialogs.count() : 0;
		
	},
	
	__relocate : function() {
		
		// a window resize event is occuring - relocate the window JIC !!
		count = this.count();
		if (count==0) return;
		
		for (var counter=0; counter<count; counter++) {
			var dialog = App.UI.DialogManager.dialogs.itemat(counter);
			if (dialog != null) dialog.relocate();
		}
		
	},
	
	__close : function(oEvent) {
		
		if (oEvent==null) return;
		var target = $(oEvent.currentTarget).parents('.dialogbox');
		
		if ((target==null) || (target=='undefined')) return;		
		var id = $(target).attr('id');
		App.UI.DialogManager.close(id);
		
	},
	
	__removeDialog : function(id) {
		
		var dialog = App.UI.DialogManager.dialogs.get(id);
		
		if (dialog != null) {
			App.UI.DialogManager.dialogs.remove(id);
			dialog = null; // kill the instance...
		}
		
	},
	
	__signalLoad : function(mode, id) {
		
		var dialog = App.UI.DialogManager.dialogs.get(id);
		if (dialog==null) return;
		
		switch (mode) {
			case 'success': {
				if (!dialog.visible) dialog.__showDialog();				
				break;
			}
			case 'error': {
				dialog.close();
				console.info('content load failure / '+id);
				break;
			}
		}
		
	},

	createDialog : function(callback, url, params) {
		
		var newDialog = new Dialog(callback, url, params);
		App.UI.DialogManager.dialogs.add(newDialog.id, newDialog);		
		newDialog.__loadContent();
		return newDialog;
		
	},
	
	closeByObject : function(initator) {
		
		if (initator==null) return this.close();
		var target = $(initator).parents('.dialogbox');
		
		if ((target==null) || (target=='undefined')) return;		
		var id = $(target).attr('id');
		App.UI.DialogManager.close(id);
		
	},
	
	reload : function(url) {
		
		var dialog = null;
		dialog = App.UI.DialogManager.dialogs.itemat(App.UI.DialogManager.dialogs.count()-1);
		
		if (dialog==null) return;
		dialog.url = url;
		dialog.reload();
		
	},
	
	close : function(id) {
		
		if ((id==null) || (id=='undefined')) id = null;
		var dialog = null;
		
		if (id==null) { 
			dialog = App.UI.DialogManager.dialogs.itemat(App.UI.DialogManager.dialogs.count()-1);
		} else {
			dialog = App.UI.DialogManager.dialogs.get(id);
		}
		
		if (dialog==null) return;
		dialog.close();
		
	},	
	
	closeWithRedirect : function(url) {
		
		var dialog = null;
		dialog = App.UI.DialogManager.dialogs.itemat(App.UI.DialogManager.dialogs.count()-1);
		
		if (dialog==null) return;
		dialog.onclose = url;
		dialog.close();
		
	},
	
	closeAll : function() {
		
		// close all dialogs regardless....
		while (App.UI.DialogManager.dialogs.count()>0) {
			dialog = App.UI.DialogManager.dialogs.pop();
			if (dialog==null) return;
			dialog.close();
		}
		
	}
		
};


$(document).ready(function() {
	
	App.UI.DialogManager.__preinit();
	
});
