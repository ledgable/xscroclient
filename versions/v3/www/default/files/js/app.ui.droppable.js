

App.UI.Droppable = {
	
	hasInit : false,
	readers : null,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		App.UI.Droppable.readers = new Hashtable();
		
		$('*').bind('page-refresh data-refresh html-changed window-refresh', function(object, data) {
					// do nothing...
					});
		
		$(document).delegate('[data-component="droppable"]', 'dragover', function(oEvent) {
							 oEvent.preventDefault();
						 });
		
		$(document).delegate('[data-component="droppable"]', 'drop', function(e) {
							 e.stopPropagation();
							 e.preventDefault();
							 var files = e.originalEvent.dataTransfer.files;
							 App.UI.Droppable.loadFile(e.currentTarget, e.originalEvent, files);
						 });
		
	},
	
	processFile : function(target, oEvent, src, filename, format) {
		
		var params = {};
		params.filename = filename;
		params.src = src;
		params.format = format;
		
		App.Core.Application.__handleEvent(null, 'event', target, params);
		
	},
	
	loadFile : function(target, event, file) {
		
		//	Create our FileReader and run the results through the render function.
		
		for (var counter=0; counter < file.length; counter++) {
			
			var fileitem = file[counter];
			var reader = new FileReader();
			var format = fileitem.type.split("/")[1]
			
			reader.fileName = fileitem.name;
			reader.uid = new String().guid();
			
			reader.onload = function(e) {
				
				App.UI.Droppable.processFile(target, event, e.target.result, e.target.fileName, format);
				App.UI.Droppable.readers.remove(e.target.uid);
				
			};
			
			App.UI.Droppable.readers.add(reader.uid, reader);
			reader.readAsDataURL(fileitem);
			
		}
	
	}
	
};

$(document).ready(function() {
				  
	App.UI.Droppable.__preinit();
				  
});
