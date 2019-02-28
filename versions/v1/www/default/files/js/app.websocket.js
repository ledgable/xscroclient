
App.WebSocket = {
	
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		var header = document.location;
		var siteurl = "ws:" + '//' + header.hostname + ":9001/";
		
		// modify this to point to the service location.. may use different servers !!
		ws = new WebSocket(siteurl);
		
		ws.onopen = function() {
			// channel opened successfully
			console.info("opened");
		};
		
		ws.onmessage = function(e) {
			
			var data = jQuery.parseJSON(e.data);
			
			if ((data != null)) {
				
				if (data.target != null && data.target != 'undefined') {
					
					var target = data.target;
					var domain = Object.byString(App, target.domain);
					var functionFound = null;
					
					if ((domain != null) && (domain != 'undefined')) {
						if (typeof domain[target.event] == 'function') {
							functionFound = domain[target.event];
						}
					}
					
					if (functionFound != null) {
						functionFound(this, data);
					}
					
				} else {
					console.info(data)
				}
				
			}
			
		};
		
		ws.onclose = function() {
			// channel closed successfully
			console.info("onclose");
		};
		
		ws.onerror = function(e) {
			// channel error occurred
			console.info("onerror = " + e);
		};
		
	},
	
};

$(document).ready(function() {
				  App.WebSocket.__preinit();
				  });

