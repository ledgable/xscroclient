
App.UI.Stats = {
	
	hasInit : false,
	
	__preinit : function() {
		if (this.hasInit) return;
		this.hasInit = true;
	},
	
};


App.UI.Stats.Plot = {
	
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		$('*').bind('page-refresh window-refresh', function(object, data) {
						App.UI.Stats.Plot.refresh(data);
					});
		
		$(document).delegate('[data-component="statplot"]', 'data-attribute-changed', function() {
							 App.UI.Stats.Plot.__createStat(this);
							 });
		
		$(document).delegate('[data-component="statplot"]', 'click', function() {
							 App.UI.Stats.Plot.__reset(this);
							 });
		
	},

	refresh : function(target) {
		
		if ((target==null) || (typeof(target) == 'object')) {
			$('body').find('[data-component="statplot"]').each(function() {
																 App.UI.Stats.Plot.__createStat(this);
																 });
		} else {
			$(target).find('[data-component="statplot"]').each(function() {
																 App.UI.Stats.Plot.__createStat(this);
																 });
		}
		
	},
	
	__createStat : function(target) {
		
		if ((target != null) && (target != "undefined")) {
			
			var datasource = $(target).attr('data-datasource');
			if ((datasource=='undefined') || (datasource==null)) datasource = null;
			
			var callinpro = $(target).attr('data-callinpro');
			if ((callinpro=='undefined') || (callinpro==null)) {
				callinpro = false;
			} else {
				callinpro = callinpro.toString().bool();
			}
			
			if ((datasource != null) && (datasource != '')) {
				
				if (callinpro) return;
				$(target).attr('data-callinpro', true);
				
				if (datasource.startsWith('arr:')) {
					var space = datasource.substring(4);
					var memData = App.UI.DataServices.getDataItem(space);
					this.__processJsonData(memData, target, false);
				} else {
					App.UI.DataServices.getData(datasource, target, App.UI.Stats.Plot.__processJsonData, 0);
				}
				
			} else {
				
				App.UI.Stats.Plot.__updateDisplay(target);
				
			}
			
		}
		
	},
	
	__processJsonData : function(datain, target, dataonly) {
		
		if (datain != null) {
			$(target).attr('data-callinpro', false);
		}
		
		var callinpro = $(target).attr('data-callinpro');
		if ((callinpro=='undefined') || (callinpro==null)) {
			callinpro = false;
		} else {
			callinpro = callinpro.toString().bool();
		}
		
		// the data is being refreshed - avoid this process....
		if (callinpro && dataonly) return;
		
		if ((dataonly=='undefined') || (dataonly==null)) dataonly = false;
		if (target==null) return;
		
		var datachanged = (datain!=null);
		var storeId = $(target).attr('id');
		
		if (storeId != null) {
			if (datain==null) {
				datain = App.UI.DataServices.dataStore.get(storeId);
			} else {
				App.UI.DataServices.dataStore.add(storeId, datain); // will overwrite if necessary !!
			}
		}
		
		var data = null;
		if (typeof datain == 'string') {
			data = jQuery.parseJSON(datain);
		} else {
			data = datain;
		}
		
		App.UI.Stats.Plot.__updateDisplay(target, data);
		
	},
	
	__normalizeData : function(datain, offset, interval) {
		
		var entry = null;
		var data = null;

		var length = datain.length;
		var outdata = [];
		var timestamp = 0;
		var volume, price = 0.0;
		
		var currentidx = -1;
		var currentidx, idx = 0;
		
		var minvolume, maxvolume, volume = 0.0;
		var minprice, maxprice, price = 0.0;
		
		for (var counter=0; counter<length; counter++) {
			
			entry = datain[counter];
			timestamp = entry.time;
			
			if (timestamp >= offset) {
			
				volume = entry.volume;
				price = entry.price;
				
				idx = Math.floor((timestamp - offset) / interval);
				
				if (idx == currentidx) {
					
					if (volume < data.volume.min) data.volume.min = volume;
					if (volume > data.volume.max) data.volume.max = volume;
					if (price < data.price.min) data.price.min = price;
					if (price > data.price.max) data.price.max = price;
					
					data.price.datapoints.push(price);
					
					data.volume.total += volume;
					data.volume.datapoints.push(volume);
					
				} else {
					
					if (data != null) {
						outdata.push(data);
					}
					
					currentidx = idx;
					minprice = maxprice = price;
					minvolume = maxvolume = volume;
					data = {'idx':idx, 'timestamp':timestamp, 'volume':{'min':volume, 'max':volume, 'total':volume, 'datapoints':[volume]}, 'price':{'min':price, 'max':price, 'datapoints':[price]}};
					
				}
				
			}
			
		}
				
		if (data != null) {
			outdata.push(data);
		}
		
		return outdata;
		
	},
	
	__updateDisplay : function(target, data) {
		
		if (data == null || data == 'undefined') {
			data = {};
		}
		
		var ctx = target.getContext("2d");
		
		target.style.width ='100%';
		target.style.height='100%';
		// ...then set the internal size to match
		target.width  = target.offsetWidth;
		target.height = target.offsetHeight;
		
		var devicePixelRatio = window.devicePixelRatio || 1,
		backingStoreRatio = ctx.webkitBackingStorePixelRatio ||
		ctx.mozBackingStorePixelRatio ||
		ctx.msBackingStorePixelRatio ||
		ctx.oBackingStorePixelRatio ||
		ctx.backingStorePixelRatio || 1,
		ratio = devicePixelRatio / backingStoreRatio;
				
		var width = target.scrollWidth;
		var height = target.scrollHeight;
		
		var plotheight = ((height / 3.0) * 2);
		var volumeheight = (height - plotheight);

		ctx.clearRect(0, 0, width, height);
		
		// draw lines etc here
		
		ctx.beginPath();
		ctx.strokeStyle = "#ddd";
		ctx.moveTo(10,(height - (volumeheight + 10)));
		ctx.lineTo((width-10),(height - (volumeheight + 10)));
		ctx.stroke();
		
		ctx.beginPath();
		ctx.strokeStyle = "#ddd";
		ctx.moveTo(10,(height - 10));
		ctx.lineTo((width-10),(height - 10));
		ctx.stroke();
		
		// then draw plot data
		
		var offset = 0;
		var interval = 1;
		var showintervals = 31;
		
		if (data != null && data != 'undefined') {
		
			var outdata = this.__normalizeData(data, offset, interval);
			
			var entry = null;
			var timestamp = 0;
			var volume = price = 0.0;
			
			// calculate spread
			
			var maxidx, minidx;
			var maxvolume = 0.0;
			var maxprice = minprice = pricespread = 0.0;

			if (outdata.length > 0) {
				
				for (var counter=0; counter < outdata.length; counter++) {
					
					data = outdata[counter];
					
					if (counter == 0) {
						
						minidx = maxidx = data.idx;
						maxprice = data.price.max;
						maxvolume = data.volume.total;
						
					} else {
						
						if (maxvolume < data.volume.total) maxvolume = data.volume.total;
						if (maxprice < data.price.max) maxprice = data.price.max;
						
						maxidx = data.idx;
						
					}
					
				}
				
			}
			
			volumespread = maxvolume;
			pricespread = maxprice - minprice;
			
			// plot volume info

			var xstep = (width / showintervals) / devicePixelRatio;
			
			var normalizedprice, normalizedvolume;
			var xpos = ypos = volheight = priceHeight = 0.0;
			var x1 = y1 = x2 = y2 = 0.0;
			
			for (var counter=0; counter<outdata.length; counter++) {
				
				entry = outdata[counter];
				normalizedprice = normalizedvolume = 0.0;

				timestamp = entry.timestamp;
				xpos = 10 + (counter * xstep);
				
				x1 = x2; y1 = y2;
				x2 = xpos;

				// plot volume

				volume = entry.volume.total;
				
				if (volumespread != 0.0) {
					normalizedvolume = volume / volumespread;
				}

				ctx.beginPath();
				ctx.fillStyle = "#3980A8";
				
				volheight = ((volumeheight - 20) * normalizedvolume);
				ypos = height - 10 - volheight;
				
				ctx.fillRect(x2 - (2.0 / devicePixelRatio), height - (10 + volheight), (4.0 / devicePixelRatio), volheight);
				ctx.fill();
				
			}
			
			// plot pricing
			
			var plotprice = 0.0;
			xpos = ypos = volheight = priceHeight = 0.0;
			x1 = y1 = x2 = y2 = 0.0;
			
			// plot the line
			// do a fill
			
			ctx.beginPath();
			var grd=ctx.createLinearGradient(0,10,0,plotheight);
			grd.addColorStop(0, '#3980A8');
			grd.addColorStop(1, 'rgba(255,255,255,255)');
			ctx.fillStyle=grd;
			
			for (var counter=0; counter<outdata.length; counter++) {
				
				entry = outdata[counter];
				normalizedprice = normalizedvolume = 0.0;
				
				timestamp = entry.timestamp;
				xpos = 10 + (counter * xstep);
				
				x1 = x2; y1 = y2;
				x2 = xpos;

				// plot data
				
				plotprice = 0.0;
				
				if (pricespread > 0) {
					
					if (entry.price.min == entry.price.max) {
						
						plotprice = entry.price.min;
						
					} else {
						
						// calculate average price
						
						var totalprice = 0.0;
						
						for (var intcounter=0; intcounter < entry.price.datapoints.length; intcounter++) {
							totalprice += entry.price.datapoints[intcounter];
						}
						
						plotprice = totalprice / entry.price.datapoints.length;
						
					}
					
					normalizedprice = (plotprice - minprice) / pricespread;
					priceHeight = (plotheight - 20) * normalizedprice;
					
					y2 = (height - volumeheight) - (10 + priceHeight);
					
					if (counter == offset) {
						ctx.moveTo(x2, (plotheight-10));
						ctx.lineTo(x2, y2);
					} else {
						ctx.lineTo(x2, y2);
					}
					
				}
				
			}
			
			ctx.lineTo(x2, (plotheight-10));
			ctx.lineTo(10, (plotheight-10));

			ctx.fill();
			ctx.closePath();
			
		}
		
		// do ranges
		xpos = ypos = volheight = priceHeight = 0.0;
		x1 = y1 = x2 = y2 = 0.0;
		
		for (var counter=0; counter<outdata.length; counter++) {
			
			entry = outdata[counter];
			normalizedprice = normalizedvolume = 0.0;
			
			timestamp = entry.timestamp;
			xpos = 10 + (counter * xstep);
			
			x1 = x2; y1 = y2;
			x2 = xpos;
			
			if (pricespread > 0) {
				
				if (entry.price.datapoints.length > 1) {
					
					// show low and high...
					
					var lowprice = (entry.price.min - minprice) / pricespread;
					var ylow = (height - volumeheight) - (10 + ((plotheight - 20) * lowprice));
					
					var highprice = (entry.price.max - minprice) / pricespread;
					var yhigh = (height - volumeheight) - (10 + ((plotheight - 20) * highprice));
					
					var xint = x2 - 1.5;
					
					ctx.beginPath();
					ctx.strokeStyle = "#666";
					ctx.moveTo(xint,ylow);
					ctx.lineTo(xint+3,ylow);
					ctx.moveTo(xint,yhigh);
					ctx.lineTo(xint+3,yhigh);
					ctx.moveTo(x2,yhigh);
					ctx.lineTo(x2,ylow);
					ctx.stroke();
					
				}
				
			}
			
		}
		
		// do the line
		
		ctx.beginPath();
		ctx.strokeStyle = "#000";
		
		for (var counter=0; counter<outdata.length; counter++) {
			
			entry = outdata[counter];
			normalizedprice = normalizedvolume = 0.0;
			
			timestamp = entry.timestamp;
			xpos = 10 + (counter * xstep);
			
			x1 = x2; y1 = y2;
			x2 = xpos;
			
			// plot data
			
			plotprice = 0.0;
			
			if (pricespread > 0) {
				
				if (entry.price.min == entry.price.max) {
					
					plotprice = entry.price.min;
					
				} else {
					
					// calculate average price
					
					var totalprice = 0.0;
					
					for (var intcounter=0; intcounter < entry.price.datapoints.length; intcounter++) {
						totalprice += entry.price.datapoints[intcounter];
					}
					
					plotprice = totalprice / entry.price.datapoints.length;
					
				}
				
				normalizedprice = (plotprice - minprice) / pricespread;
				priceHeight = (plotheight - 20) * normalizedprice;
				
				y2 = (height - volumeheight) - (10 + priceHeight);
				
				if (counter == offset) {
					ctx.moveTo(x2, y2);
				} else {
					ctx.lineTo(x2, y2);
				}
				
			}
			
		}
		
		ctx.stroke();
		
	},
	
	__reset : function(target) {
		
	},
	
};

App.UI.Stats.Circle = {
	
	/*
	 MODE 0 - Percentage
	 MODE 1 - Circles with shadow
	 MODE 2 - Circles without shadows
	 */
	
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		$('*').bind('page-refresh window-refresh', function(object, data) {
					App.UI.Stats.Circle.refresh(data);
					});
		
		$(document).delegate('[data-component="statcircle"]', 'data-attribute-changed', function() {
							 App.UI.Stats.Circle.__updateDisplay(this);
							 });
		
		$(document).delegate('[data-component="statcircle"]', 'click', function() {
							 App.UI.Stats.Circle.__reset(this);
							 });
		
	},
	
	refresh : function(target) {
		
		if ((target==null) || (typeof(target) == 'object')) {
			$('body').find('[data-component="statcircle"]').each(function() {
																 App.UI.Stats.Circle.__createStat(this);
																 });
		} else {
			$(target).find('[data-component="statcircle"]').each(function() {
																 App.UI.Stats.Circle.__createStat(this);
																 });
		}
		
	},
	
	__reset : function(target) {
		
		if (($(target).attr("data-counter") != null) && ($(target).attr("data-counter") != "undefined")) {
			_currentCounter = $(target).removeAttr("data-counter");
			App.UI.Stats.Circle.__setTimer(target);
		}
		
	},
	
	__setTimer : function(target) {
		
		$.doTimeout(5, function(targetin) {
					
					var _currentCounter = 0;
					var _continue = true;
					
					if (($(targetin).attr("data-counter") != null) && ($(targetin).attr("data-counter") != "undefined")) {
					_currentCounter = parseInt($(targetin).attr("data-counter"));
					}
					
					if (_currentCounter == 0) {
					
					if (($(targetin).attr("data-vals") != null) && ($(targetin).attr("data-vals") != "undefined")) {
					
					var _percentsTo = eval("("+ $(targetin).attr("data-vals") + ")");
					var _destinationArray = new Array();
					var _deltas = new Array();
					
					for (var _counter = 0; _counter < _percentsTo.length; _counter++) {
						_destinationArray.push(0.0);
						_deltas.push(_percentsTo[_counter]/50.0);
					}
					
					_currentCounter ++;
					
					$(targetin).attr({"data-valscurrent":_destinationArray, "data-valsdelta":_deltas, "data-counter":_currentCounter});
					$(targetin).trigger('data-attribute-changed');
					
					}
					
					} else if (_currentCounter <= 50) {
					
					var _currentVals = eval("(["+$(targetin).attr("data-valscurrent")+"])");
					var _deltas = eval("(["+$(targetin).attr("data-valsdelta")+"])");
					
					for (var _counter = 0; _counter < _currentVals.length; _counter++) {
					_currentVals[_counter] += _deltas[_counter];
					}
					
					$(targetin).attr("data-valscurrent", _currentVals);
					
					_currentCounter ++;
					$(targetin).attr("data-counter", _currentCounter);
					
					App.UI.Stats.Circle.__updateDisplay(targetin);
					
					} else {
					
					_continue = false;
					
					}
					
					return _continue;
					
					}, target);
		
	},
	
	__createStat : function(target) {
		
		if ((target != null) && (target != "undefined")) {
			
			var datasource = $(target).attr('data-datasource');
			if ((datasource=='undefined') || (datasource==null)) datasource = null;
			
			var callinpro = $(target).attr('data-callinpro');
			if ((callinpro=='undefined') || (callinpro==null)) {
				callinpro = false;
			} else {
				callinpro = callinpro.toString().bool();
			}
			
			if ((datasource != null) && (datasource != '')) {
				
				if (callinpro) return;
				$(target).attr('data-callinpro', true);
				
				if (datasource.startsWith('arr:')) {
					var space = datasource.substring(4);
					var memData = App.UI.DataServices.getDataItem(space);
					this.__processJsonData(memData, target, false);
				} else {
					App.UI.DataServices.getData(datasource, target, App.UI.Stats.Circle.__processJsonData, 0);
				}
				
			} else {
				
				App.UI.Stats.Circle.__updateDisplay(target);
				
			}
			
		}
		
	},
	
	__processJsonData : function(datain, target, dataonly) {
		
		if (datain != null) {
			$(target).attr('data-callinpro', false);
		}
		
		var callinpro = $(target).attr('data-callinpro');
		if ((callinpro=='undefined') || (callinpro==null)) {
			callinpro = false;
		} else {
			callinpro = callinpro.toString().bool();
		}
		
		// the data is being refreshed - avoid this process....
		if (callinpro && dataonly) return;
		
		if ((dataonly=='undefined') || (dataonly==null)) dataonly = false;
		if (target==null) return;
		
		var datachanged = (datain!=null);
		var storeId = $(target).attr('id');
		
		if (storeId != null) {
			if (datain==null) {
				datain = App.UI.DataServices.dataStore.get(storeId);
			} else {
				App.UI.DataServices.dataStore.add(storeId, datain); // will overwrite if necessary !!
			}
		}
		
		var data = null;
		if (typeof datain == 'string') {
			data = jQuery.parseJSON(datain);
		} else {
			data = datain;
		}
		
		// prepare data structures....
		
		var percentages = [];
		var colors = [];
		
		if ((data != null) && (data != 'undefined')) {
			
			for (var counter=0; counter < data.length; counter++) {
				
				var color = data[counter]["color"]
				var percentage = parseFloat(data[counter]["percentage"]);
				
				percentages.push(percentage);
				colors.push(color);
				
			}
			
		}
		
		var colorStr = '\'' + colors.join('\',\'') + '\'';
		
		$(target).attr("data-vals", (percentages + ""));
		$(target).attr("data-colors", colorStr);
		
		App.UI.Stats.Circle.__updateDisplay(target);
		
	},
	
	__updateDisplay : function(target) {
		
		if (($(target).attr("data-counter") == null) || ($(target).attr("data-counter") == "undefined")) {
			this.__setTimer(target);
		}
		
		var ctx = target.getContext("2d");
		
		var devicePixelRatio = window.devicePixelRatio || 1,
		backingStoreRatio = ctx.webkitBackingStorePixelRatio ||
		ctx.mozBackingStorePixelRatio ||
		ctx.msBackingStorePixelRatio ||
		ctx.oBackingStorePixelRatio ||
		ctx.backingStorePixelRatio || 1,
		ratio = devicePixelRatio / backingStoreRatio;
		
		var mode = 0
		var width = target.width;
		var height = target.height;
		var _width = 5;
		
		ctx.clearRect(0, 0, width, height);
		
		if (($(target).attr("data-mode") != null) && ($(target).attr("data-mode") != "undefined")) {
			mode = parseInt($(target).attr("data-mode"));
		}
		
		if (($(target).attr("data-width") != null) && ($(target).attr("data-width") != "undefined")) {
			_width = parseInt($(target).attr("data-width"));
		}
		
		var _gap = _width / 2;
		
		if (($(target).attr("data-gap") != null) && ($(target).attr("data-gap") != "undefined")) {
			_gap = parseInt($(target).attr("data-gap"));
		}
		
		if (mode == 0) {
			
			ctx.beginPath();
			ctx.arc(width / 2, height / 2, (width / 2)-10, 0, (2*Math.PI));
			ctx.arc(width / 2, height / 2, (width / 2)-(10+_width), (2*Math.PI), 0, 1);
			
			ctx.fillStyle = "#ddd";
			ctx.globalAlpha = 0.15;
			ctx.fill();
			
		}
		
		if (($(target).attr("data-valscurrent") != null) && ($(target).attr("data-valscurrent") != "undefined")) {
			
			var _percents = eval("(["+ $(target).attr("data-valscurrent") + "])");
			var _colors = new Array("#f00", "#0f0", "#00F", "#ff0", "#f0f");
			
			if (($(target).attr("data-colors") != null) && ($(target).attr("data-colors") != "undefined")) {
				_colors = eval("("+ $(target).attr("data-colors") + ")");
			}
			
			if (_colors.length >= _percents.length) {
				
				var _angleFrom = 0.0 - (Math.PI / 2);
				
				if (_angleFrom < 0.0) {
					_angleFrom = (2*Math.PI) + _angleFrom;
				}
				
				for (var _counter=0; _counter < _percents.length; _counter++) {
					
					var _percent = _percents[_counter];
					
					if (_angleFrom > (2*Math.PI)) {
						_angleFrom = _angleFrom - (2*Math.PI);
					}
					
					var _angleTo = _angleFrom + (_percent * (2*Math.PI));
					if (_angleTo > (2*Math.PI)) {
						_angleTo = _angleTo - (2*Math.PI);
					}
					
					if (mode == 1) {
						
						ctx.beginPath();
						ctx.arc(width / 2, height / 2, (width / 2)-(10+(_counter * (_width+_gap))), 0, (2*Math.PI));
						ctx.arc(width / 2, height / 2, (width / 2)-(10+_width+(_counter * (_width+_gap))), (2*Math.PI), 0, 1);
						
						ctx.fillStyle = "#ddd"; //_colors[_counter];
						ctx.globalAlpha = 0.15;
						ctx.fill();
						
					}
					
					ctx.beginPath();
					
					switch (mode) {
							
						case 0: {
							ctx.arc(width / 2, height / 2, (width / 2)-10, _angleFrom, _angleTo);
							ctx.arc(width / 2, height / 2, (width / 2)-(10+_width), _angleTo, _angleFrom, 1);
							break;
						}
							
						case 2:
						case 1: {
							ctx.arc(width / 2, height / 2, (width / 2)-(10+(_counter * (_width+_gap))), _angleFrom, _angleTo);
							ctx.arc(width / 2, height / 2, (width / 2)-(10+_width+(_counter * (_width+_gap))), _angleTo, _angleFrom, 1);
							break;
						}
							
					}
					
					ctx.fillStyle = ("#"+_colors[_counter]);
					ctx.globalAlpha = 1.0;
					ctx.fill();
					
					if (mode == 0) {
						_angleFrom = _angleTo;
					}
					
				}
				
			}
			
		}
		
		if (mode == 0) {
			
			ctx.beginPath();
			ctx.arc(width / 2, height / 2, (width / 2)-10, 0, (2*Math.PI));
			ctx.arc(width / 2, height / 2, (width / 2)-(10+(_width/2)), (2*Math.PI), 0, 1);
			
			ctx.fillStyle = "rgba(255,255,255,0.4)";
			ctx.fill();
			
		}
		
	}
	
};


$(document).ready(function() {
				  
				  App.UI.Stats.__preinit();
				  
				  App.UI.Stats.Plot.__preinit();
				  App.UI.Stats.Circle.__preinit();

				  /* Now check if i need to see something... */
				  
				  App.UI.Stats.Plot.refresh();
				  App.UI.Stats.Circle.refresh();

			  });

