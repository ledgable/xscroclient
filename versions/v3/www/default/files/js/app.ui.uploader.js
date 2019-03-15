
App.UI.Uploader = {
	
	hasInit : false,
	hashMap : null,
	readers : null,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		App.UI.Uploader.hashMap = new Hashtable();
		App.UI.Uploader.readers = new Hashtable();
		
		$('*').bind('page-refresh data-refresh html-changed window-refresh', function(object, data) {
					if (object.type == "page-refresh") {
						App.UI.Uploader.hashMap.clear();
					}
					App.UI.Uploader.refresh(data);
					});
		
		$(document).delegate('[data-component="uploader"]', 'dragover', function(oEvent) {
							 oEvent.preventDefault();
							 });
		
		$(document).delegate('[data-component="uploader"]', 'drop', function(e) {
							 e.stopPropagation();
							 e.preventDefault();
							 var files = e.originalEvent.dataTransfer.files;
							 App.UI.Uploader.loadFile(e.originalEvent, files);
							 });
		
		$(document).delegate('[data-component="uploader"]', 'click', function(e) {
							 console.info("Here");
							 });
		
	},
	
	reloadImage : function(target) {
		
		var id = $(target).attr("id");
		
		if ((id != null) && (id != 'undefined')) {
			
			var imageData = $(target).data("src");
			
			if ((imageData != null) && (imageData != "undefined")) {
				
				var MAX_HEIGHT = 256;
				var MAX_WIDTH = 256;
				
				if (($(target).data("height") != null) && ($(target).data("height") != "undefined")) {
					MAX_HEIGHT = parseInt($(target).data("height"));
				}
				
				if (($(target).data("width") != null) && ($(target).data("width") != "undefined")) {
					MAX_WIDTH = parseInt($(target).data("width"));
				}
				
				var image = null;
				
				if (App.UI.Uploader.hashMap.exists(id)) {
					image = App.UI.Uploader.hashMap.get(id);
				} else {
					var image = new Image();
					App.UI.Uploader.hashMap.add(id, image);
				}
				
				image.onload = (function(targetId) {
								
									return function(e) {
								
										var canvas = $('canvas#'+targetId)[0];
								
										if ((canvas != null) && (canvas != 'undefined')) {
								
											if (image.width == image.height) {
												if (image.height > MAX_HEIGHT) {
													image.width *= MAX_HEIGHT / image.height;
													image.height = MAX_HEIGHT;
												}
											} else {
												if (image.height > MAX_HEIGHT) {
													image.width *= MAX_HEIGHT / image.height;
													if (image.width > MAX_WIDTH) {
														image.width = MAX_WIDTH;
													}
													image.height = MAX_HEIGHT;
												}
											}
								
											var context = canvas.getContext("2d");
								
											context.clearRect(0, 0, canvas.width, canvas.height);
											canvas.width = image.width;
											canvas.height = image.height;
											context.drawImage(image, 0, 0, image.width, image.height);
								
										}
								
									};
								
								})(id);
				
				if ((imageData != null) && (imageData[0] != "%")) {
				   image.src = imageData;
				}
				
			}
			
		}
		
	},
	
	refresh : function(oEvent) {
		
		$('body').find('[data-component="uploader"]').each(function() {
																App.UI.Uploader.reloadImage(this);
																});
		
	},
	
	uploadImage : function(oEvent, src, filename, format) {
		
		var fnUpload = $(oEvent.target).attr("data-call");
		
		var MAX_HEIGHT = 256;
		var MAX_WIDTH = 256;
		
		var dataParams = {}
		var id = $(oEvent.target).attr("id");
		
		if (($(oEvent.target).data("height") != null) && ($(oEvent.target).data("height") != "undefined")) {
			MAX_HEIGHT = parseInt($(oEvent.target).data("height"));
		}
		
		if (($(oEvent.target).data("width") != null) && ($(oEvent.target).data("width") != "undefined")) {
			MAX_WIDTH = parseInt($(oEvent.target).data("width"));
		}
		
		if (($(oEvent.target).data("params") != null) && ($(oEvent.target).data("params") != "undefined")) {
			dataParams = eval("("+$(oEvent.target).data("params")+")");
			console.info("Params = " + dataParams);
		}
		
		var image = null;
		
		if (App.UI.Uploader.hashMap.exists(id)) {
			image = App.UI.Uploader.hashMap.get(id);
		} else {
			var image = new Image();
			App.UI.Uploader.hashMap.add(id, image);
		}
		
		image.onload = (function(targetId, format, callfn) {
					
				return function(e) {
				
					var canvas = $('canvas#'+targetId)[0];
				
					if ((canvas != null) && (canvas != 'undefined')) {

						var context = canvas.getContext("2d");
						context.clearRect(0, 0, canvas.width, canvas.height);
				
						if (image.width == image.height) {
							if (image.height > MAX_HEIGHT) {
								image.width *= MAX_HEIGHT / image.height;
								image.height = MAX_HEIGHT;
							}
						} else {
							if (image.height > MAX_HEIGHT) {
								image.width *= MAX_HEIGHT / image.height;
								if (image.width > MAX_WIDTH) {
									image.width = MAX_WIDTH;
								}
								image.height = MAX_HEIGHT;
							}
						}
			
						canvas.width = image.width;
						canvas.height = image.height;
						context.drawImage(image, 0, 0, image.width, image.height);
						dataParams.format = 'image';
						
						var rawdata = null;
				
						if (format == "png") {
							rawdata = canvas.toDataURL("image/png");
				
						} else if ((format == "jpg") || (format == "jpeg")) {
							rawdata = canvas.toDataURL("image/jpeg", 0.92);
				
						} else {
							console.info("Unsupported type");
						
						}
				
						if (rawdata != null) {
				
							$(canvas).attr('data-src', rawdata);
							var oRequest= {actions:[{action:callfn, content:rawdata, data:dataParams}], jw:App.Core.Security.code};
							$('*').triggerHandler('handle-app', oRequest);
				
						}
				
					}
				
				};
				
			})(id, format, fnUpload);
		
		image.setAttribute('crossOrigin','anonymous');
		image.src = src;

		
	},
	
	uploadFile : function(oEvent, src, filename, format) {
		
		var fnUpload = $(oEvent.target).attr("data-call");
		
		var dataParams = {}
		var id = $(oEvent.target).attr("id");
		
		if (($(oEvent.target).data("params") != null) && ($(oEvent.target).data("params") != "undefined")) {
			dataParams = eval("("+$(oEvent.target).data("params")+")");
			console.info("Params = " + dataParams);
		}
		
		dataParams.format = 'document';
		dataParams.filename = filename;
		
		var oRequest= {actions:[{action:fnUpload, content:src, data:dataParams}], jw:App.Core.Security.code};
		$('*').triggerHandler('handle-app', oRequest);
		
	},
	
	loadFile : function(target, file) {
		
		//	Create our FileReader and run the results through the render function.
		
		var uploadType = $(target).attr("data-type");
		
		if ((uploadType == null) || (uploadType == 'undefined')) {
			uploadType = "files";
		}
		
		for (var counter=0; counter < file.length; counter++) {
			
			var fileitem = file[counter];
			var reader = new FileReader();
			var format = fileitem.type.split("/")[1]

			reader.fileName = fileitem.name;
			reader.uid = new String().guid();
			
			reader.onload = function(e) {
				
				switch (uploadType) {
						
					case "files": {
						App.UI.Uploader.uploadFile(target, e.target.result, e.target.fileName, format);
						break;
					}
						
					case "image": {
						if (!file.type.match(/image.*/)){
							console.log("The dropped file is not an image: ", file.type);
							return;
						}
						App.UI.Uploader.uploadImage(target, e.target.result, e.target.fileName, format);
						break;
					}
						
				}
				
				App.UI.Uploader.readers.remove(e.target.uid);
				
			};
			
			App.UI.Uploader.readers.add(reader.uid, reader);
			reader.readAsDataURL(fileitem);

		}
		
	}
	
};

$(document).ready(function() {
				  
				  App.UI.Uploader.__preinit();
				  
				  App.UI.Uploader.refresh();

			  });
