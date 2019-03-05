
// Notification javascript code

App.Notify = {
	
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		this.__setup();
		
	},
	
	__setup : function() {
		
		var oHtml = "<div id='notifications__main' class='notifications'><ul></ul></div>";
		$("body").append(oHtml);
		
	},
	
	showMessage: function(status, message) {
		
		if (message == null || message == 'undefined') {
			return;
		}
		
		var root = $("#notifications__main > ul");
		var objectid = new String().guid();
				
		var oHtml = "<li id='" + objectid + "' class='message'><span>" + message + "</span></li>";
		
		if (status == 0) {
			oHtml = "<li id='" + objectid + "' class='message failed'><span>" + message + "</span></li>";
		}
		
		root.append(oHtml);

		$.doTimeout(2000, function(targetin) {
						$("#notifications__main > ul > li#" + objectid).remove();
					});
		
	}
	
};


$(document).ready(function() {
				  App.Notify.__preinit();
				  });
