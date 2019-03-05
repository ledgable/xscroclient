
/*
 * Copyright (C) 2016-2018 Ledgable BV
 * All Rights Reserved
 * No copying, duplication or replication of code permitted without
 * express permission of Ledgable BV
 */

DataComponent = function(id) { return this.init(id); };

$.extend(DataComponent.prototype, {
	id: null,
		 
	templates : null,
	datastore : null, // for later !!
		 
	type : function() { return $('#'+this.id).attr('data-component'); },
		 
	init : function(id) {
		this.id = id;
		this.__setup(); // get templates etc...
	},
	
	verify : function() {
		var htmlTemplates = $('#'+this.id + ' > .template');;
		if (htmlTemplates.length > 0) {
			// we have templates - something seems different - reload them asap !!
			this.__loadTemplates(htmlTemplates, true);			
		}
	},
	
	__setup : function() {
		 
		var targetId = this.id;
		var type = $('#'+this.id).attr('data-component');
		 
		if (type == "repeater" || type == "list" || type == "gmaps") {
			if ((targetId==null) || (targetId=='undefined') || (targetId=='')) return;
			var htmlTemplates = $('#'+targetId + ' > .template');
			this.__loadTemplates(htmlTemplates, false);
		 }
		 
	},
	
	__loadTemplates : function(htmlTemplates, reset) {
		 
		if ((this.templates==null) || reset) {
			this.templates = new Hashtable();
		} else {
			if (htmlTemplates.length > 0) {
				for (var counter=0; counter< htmlTemplates.length; counter++) {
					$(htmlTemplates[counter]).remove();
				}
			}
			return;
		}
		 
		if (htmlTemplates.length > 0) {
			for (var counter=0; counter< htmlTemplates.length; counter++) {

				if ($(htmlTemplates[counter]).parents('.template').length == 0) {
		 
					var classid = $(htmlTemplates[counter]).attr('class');
					var classes = classid.split(' ');
					var out = '';				
					
					for (var xcount=0; xcount<classes.length; xcount++) {
						if (classes[xcount]!='template') out += '.'+classes[xcount];					
					}				
					
					if (this.templates.indexof(out)==-1) {
						var content = $(htmlTemplates[counter]).html();
						var attributesraw = $(htmlTemplates[counter])[0].attributes;
						var attrs = {};
						for (var acount=0; acount<attributesraw.length; acount++) {
							attrs[attributesraw[acount].name] = attributesraw[acount].value;
						}
												
						this.templates.add(out, {'html':content, 'attr':attrs});
						$(htmlTemplates[counter]).remove();
					}
					
				} else {
					// template is nested....
				}
			}
		}
	}
	
});

App.UI = {};

App.UI.Core = {

	hasInit : false,
	componentsRegisterd : new Hashtable(),
	inprogress : false,

	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		$('*').bind('page-refresh data-refresh window-refresh', function(object, data) {
			if (App.UI.Core.inprogress) {
				console.info('refresh in progress - aborting');
			}
			App.UI.Core.inprogress = true;
			App.UI.Core.refresh(data);
			App.UI.Core.inprogress = false;
		});				
	},
	
	attr : function(id, template, attribute) {
		if (id==null) return null;
		var dataComp = App.UI.Core.componentsRegisterd.get(id);
		if (dataComp != null) {
			if (dataComp.templates.indexof(template) != -1 ) {
				if (dataComp.templates.get(template).attr[attribute] != null) {
					return dataComp.templates.get(template).attr[attribute];		
				}
			}
		}
		return null;		
	},
	
	get : function(id, template) {
		if (id==null) return null;
		var dataComp = App.UI.Core.componentsRegisterd.get(id);
		if (dataComp != null) {
			if (dataComp.templates.indexof(template) != -1 ) {
				return dataComp.templates.get(template).html;		
			}
		}
		return null;
	},
	
	refresh : function(target) {
		if ((target == null) || (typeof(target) == 'object')) {
			$('body').find('[data-component]').each(function() { 
				App.UI.Core.__processComponent(this); 
			});										
		} else {
			if (($(target).attr('data-component') != null) && ($(target).attr('data-component') != 'undefined')) {
				App.UI.Core.__processComponent($(target)); 			
			} else {
				$(target).find('[data-component]').each(function() { 
					App.UI.Core.__processComponent(this); 
				});			
			}
		}
	},			
	
	__processComponent : function(target) {
		
		if ((target==null) || (target=='undefined')) return;
		
		var objectid = $(target).attr('id');
	
		if ((objectid == null) || (objectid == 'undefined')) {
			
			var dataid = $(target).attr('data-actualid');
			
			if ((dataid != null) && (dataid != 'undefined')) {
				$(target).attr('id', dataid);
			} else {
				objectid = new String().guid();
				$(target).attr('id', objectid);
			}
			
		}
		
		var datacomp = null;
		
		if (App.UI.Core.componentsRegisterd.indexof(objectid) == -1) {
			// not in cache - prob havent seen it before .....
			datacomp = new DataComponent(objectid);
			App.UI.Core.componentsRegisterd.add(objectid, datacomp);
		} else {
			datacomp = App.UI.Core.componentsRegisterd.get(objectid);
			datacomp.verify();
		}
		
		if (datacomp != null) {
			App.UI.Core.componentsRegisterd.add(objectid, datacomp);
		}
		
	},
	
	checkRepeats : function(line) {
		
		var r=/(<repeat[^>]*>)([\u0000-\uffff]+)/i;
		var q = /eval\=\"[^"]+\"/;
		var m = null;
		
		while((m=r.exec(line))!=null&&m.length>1&&m[1]!='') {
			
			var sequence = m[0].substring(0, m[0].indexOf('</repeat>')+9);
			
			var toreplace= sequence;
			var evalsequence = false;
			var oHtml = '';
			
			if ((n=q.exec(m[1]))!=null) {
				
				var evaluate = n[0].substr(6, n[0].length-7);
				var startpos = n.index+n[0].length+1;
				var repeatSequence = jQuery.trim(sequence.substring(startpos, sequence.length-9));

				evaluate = evaluate.replace('&amp;&amp;', '&&');
				evaluate = evaluate.replace('&amp;', '&');
				evaluate = evaluate.replace('&lt;', '<');
				evaluate = evaluate.replace('&gt;', '>');
				
				if ((evaluate!='') && (evaluate != null) && (evaluate != 'undefined')) {
					if ((evaluate.indexOf('=')!=-1) || (evaluate.indexOf('>')!=-1) || (evaluate.indexOf('<')!=-1) || (evaluate.indexOf('+')!=-1) || (evaluate.indexOf('-')!=-1)) {
						evalsequence = eval(evaluate);
					} else {
						evalsequence = evaluate;
					}
				} else {
					evalsequence = 'null';
				}
			} else {
				evalsequence = 'null';
			}
			
			try {
				if (evalsequence != 'null') {
					
					var count = parseInt(evalsequence);
					
					if (count > 0) {
						for (var counter=0; counter < count; counter++) {
							oHtml += repeatSequence;
						}						
					}
			
				}
			}
			
			catch (err) {
				console.info('error = '+err);
			}
			
			line = line.replace(toreplace, oHtml);
			
		}
		
		return line;
		
	},
			
	checkConditions : function(line) {
		
		var r=/(<condition[^>]*>)([\u0000-\uffff]+)/i;
		var q = /eval\=\"[^"]+\"/;
		var s=/(<result (eval|is|check)="[^result>]*)([\u0000-\uffff]+)/i;
		var m = null;
		
		while((m=r.exec(line))!=null&&m.length>1&&m[1]!='') {				
						
			var sequence = m[0].substring(0, m[0].indexOf('</condition>')+12);
			
			var toreplace= sequence;
			var evalsequence = false;			
			var oHtml = '';			
			
			if ((n=q.exec(m[1]))!=null) {				
				var evaluate = n[0].substr(6, n[0].length-7);

				evaluate = evaluate.replace('&amp;&amp;', '&&');
				evaluate = evaluate.replace('&amp;', '&');
				evaluate = evaluate.replace('&perc;', '%');
				evaluate = evaluate.replace('&lt;', '<');
				evaluate = evaluate.replace('&gt;', '>');
				
				if ((evaluate!='') && (evaluate != null) && (evaluate != 'undefined')) {
				
					try {
						if ((evaluate.indexOf('==')!=-1) || (evaluate.indexOf('<=')!=-1) || (evaluate.indexOf('>=')!=-1) || (evaluate.indexOf('>')!=-1) || (evaluate.indexOf('<')!=-1) || (evaluate.indexOf('+')!=-1) || (evaluate.indexOf('-')!=-1)) {
							evalsequence = eval(evaluate);
						} else {
							evalsequence = evaluate;
						}
					}
				
					catch (err) {
						evalsequence = evaluate;
					}
				
				} else {
					evalsequence = 'null';
				}
				
			} else {
				evalsequence = 'null';				
			}
			
			var o = null;
			
			try {
				
				while((o=s.exec(sequence))!=null&&o.length>1&&o[1]!='') {
					
					var resultentry = o[0].substring(0, o[0].indexOf('</result>')+9);
					
					if (resultentry.indexOf('is="') != -1) {

						var offset = resultentry.indexOf('is="')+4;
						var resulteval = resultentry.substring(offset);
						var testthis = resulteval.substring(0, resulteval.indexOf('">'));
						var textout = jQuery.trim((o[0].substring(offset+testthis.length+2, o[0].indexOf('</result>'))));
				
						var exit = false;
						var eresult = evalsequence.toString();
				
						switch (testthis) {
				
							case "default": {
								oHtml += textout;
								exit = true;
								break;
							}
				
							case "null": {
								if ((eresult == null) || (eresult == 'null') || (eresult == 'undefined') || (eresult == "''") || (eresult == "")) {
									oHtml += textout;
									exit = true;
								}
								break;
							}
				
							default: {
								if (testthis == eresult) {
									oHtml += textout;
									exit = true;
								}
								break;
							}
				
						}
				
						if (exit) {
							break;
						}
										
					} else if (resultentry.indexOf('eval="') != -1) {
					
						var offset = resultentry.indexOf('eval="')+6;
						var resulteval = resultentry.substring(offset);
						var testthis = resulteval.substring(0, resulteval.indexOf('">'));
						var textout = jQuery.trim((o[0].substring(offset+testthis.length+2, o[0].indexOf('</result>'))));
						var sequencecheck = evalsequence.toString() + testthis;

						sequencecheck = sequencecheck.replace('&amp;&amp;', '&&');
						sequencecheck = sequencecheck.replace('&amp;', '&');
						sequencecheck = sequencecheck.replace('&perc;', '%');
						sequencecheck = sequencecheck.replace('&lt;', '<');
						sequencecheck = sequencecheck.replace('&gt;', '>');
				
						if (eval(sequencecheck) == true) {
							oHtml += textout;
							break;
						}
							
					} else if (resultentry.indexOf('check="') != -1) {
				
						var offset = resultentry.indexOf('check="')+7;
						var resulteval = resultentry.substring(offset);
						var testthis = resulteval.substring(0, resulteval.indexOf('">'));
						var textout = jQuery.trim((o[0].substring(offset+testthis.length+2, o[0].indexOf('</result>'))));
						var sequencecheck = testthis;
								
						sequencecheck = sequencecheck.replace('&amp;&amp;', '&&');
						sequencecheck = sequencecheck.replace('&amp;', '&');
						sequencecheck = sequencecheck.replace('&perc;', '%');
						sequencecheck = sequencecheck.replace('&lt;', '<');
						sequencecheck = sequencecheck.replace('&gt;', '>');
						
						if (eval(sequencecheck) == true) {
							oHtml += textout;
							break;
						}
				
				}
				
					sequence = sequence.replace(resultentry, '');

				}
			}
				
			catch (err) {
				console.info('error = '+err+' in ' + sequence);
			}
			
			line = line.replace(toreplace, oHtml);
			
		}
		
		return line;
		
	},
	
	doReplaceDir : function(line, prefix) {
		
		if ((prefix==null)  || (prefix=='undefined')) prefix = '';
		var rep = new RegExp('(replace\=\"'+prefix+'[^"]+\")');
		//var rep=/(replace\=\"[^"]+\")/;		
		var sequence = '';
		var m;
		
		// check for replace directive....		
		while((m=rep.exec(line))!=null&&m.length>1&&m[1]!=''){
			sequence=m[1].substr(9, m[1].length-10);
			line = line.replace(m[1], sequence);
		}
		
		return line;
	},
	
	doVarSubstitution : function(data, line) {
		
		if ((line=='') || (line==null) || (line=='undefined') || (data==null)) return line;
		
		line = this.doReplaceDir(line);
		
		var r=/(%[^%]+%)/;
		var sequence = '';
		var m;
		var dataItem = null;
				
		while((m=r.exec(line))!=null&&m.length>1&&m[1]!=''){
			
			sequence=m[1].substr(1, m[1].length-2);
			
			var defaultvalue = '';
			var lookup = null;
			var keyword = '';
			var isarray = false;
			var done = false;
			var arraycontent = null;
			var formatting = null;
			var datatype = null;
			
			// check for default....
			
			var posrepl = sequence.indexOf('$');
			if ( posrepl != -1) { // sequence start..
				isarray = true;
				keyword = sequence.substring(0,posrepl);
				arraycontent = sequence.substring(posrepl+1);
				done = true;
			}
			
			var posdef = sequence.indexOf('|');
			if ((!done) && (posdef != -1)) {
				// is there is a default value to show.....
				defaultvalue = sequence.substring(posdef+1);
				keyword = sequence.substring(0,posdef);
				done = true;
			}
			
			var poscol = sequence.indexOf(':');
			if ((!done) && (poscol != -1)) {
				// is there is a default value to show.....				
				var rightbit = sequence.substring(poscol+1);
				var dtype = rightbit.indexOf(':');
				if (dtype != -1) {
					datatype = rightbit.substring(0, dtype);
					formatting = rightbit.substring(dtype+1);
				} else {
					datatype = 'date';
					formatting = rightbit;
				}		
				keyword = sequence.substring(0,poscol);
				done = true;				
			}			
			
			var possub = sequence.indexOf('#');
			if ((!done) && (possub != -1)) {
				var options =  sequence.substring(possub+1).split(',');
				if (options.length > 0) {
					lookup = new Array();
					for (var ocounter=0; ocounter<options.length; ocounter++) {
						var ioption = options[ocounter].split('=');
						lookup['o'+ioption[0].toString()] = ioption[1];
					}
				}
				keyword = sequence.substring(0, possub);
				done = true;				
			}
			
			if (keyword == '') keyword = sequence;			
			dataItem = null;
			
			try {
				
				if (keyword.indexOf('.') != -1) {
					
					var splitUp = keyword.split('.');
					var counter = 0;
					var dpointer = data;
					
					while ((counter < splitUp.length) && (dpointer != null)) {
						if (dpointer[splitUp[counter]] != null) {
							if (splitUp[counter] != "length") {
								if (dpointer[splitUp[counter]] != null) {
									dpointer = dpointer[splitUp[counter]];
								} else {
									dpointer = null;
									break;
								}
							}
						} else {
							dpointer = null;
							break;
						}
						counter++;
					}
				
					if (splitUp[(splitUp.length-1)] == "length") {
						var object = (lookup != null) ? lookup['o'+dpointer.toString()] : dpointer;
						if (object != null) {
							dataItem = object.length
						} else {
							dataItem = "0"
						}
					} else {
						dataItem = (lookup != null) ? lookup['o'+dpointer.toString()] : dpointer;
					}
				
				} else {
						
					if ((keyword!=null) && (data != null)) {
						if (data[keyword] != null) {
							var dataItem = null;
							if (lookup != null) {
								if (lookup['o'+data[keyword].toString()] != null) {
									var rawDataitem = lookup['o'+data[keyword]];
									dataItem = rawDataitem.toString();
								} else {
									dataItem = (lookup['odef'] != null) ? lookup['odef'] : data[keyword];  									
								}
							} else {
								dataItem = data[keyword];
							}
						} else {
							dataItem = (lookup && (lookup['odef'] != null)) ? lookup['odef'] : null;  
						}
					} else {
						dataItem = null;
					}
				}
				
			} catch (err) {
				console.info(err);
				dataItem = null;
			}
			
			if (!isarray) {			
				
				if (formatting != null) {
					
					switch (datatype) {
						
						case 'eval': {
							try {
								formatting = formatting.replace(/&amp;37;/gi,'%');
								formatting = formatting.replace(/&amp;7c;/gi,'|');
								var question = this.doVarSubstitution(data, formatting);
								dataItem = eval(question);
							}
							catch (err) {
								//console.info('An error occurred in the eval');
								console.info('error in line = '+line);	
							}
							break;
						}
								
						case 'fn': {
				
							switch (formatting) {
				
								case "remaining": {
				
									var _now = Math.round((new Date()).getTime() / 1000);
				
									if (dataItem <= 0) {
										dataItem = "";
									} else {
										var _datediff = dataItem - _now;
										if (_datediff <= 0) {
											dataItem = "Expired";
										} else {
											var _months = _datediff / 2592000;
											if (_months > 0) {
												dataItem = ""+_months+"m";
											} else {
												var _weeks = _datediff / 604800;
												if (_weeks > 0) {
													dataItem = ""+_weeks+"w";
												} else {
													var _days = _datediff / 86400;
													if (_days > 0) {
														dataItem = ""+_days+"d";
													} else {
														var _hours = _datediff / 3600;
														if (_hours > 0) {
															dataItem = ""+_hours+"h";
														} else {
															dataItem = ">1h";
														}
													}
												}
											}
										}
									}
				
									break;
								}
				
								case "upper": dataItem = dataItem.toUpperCase(); break;
								case "absnumber": dataItem = Number(Math.abs(dataItem)).toLocaleString('en'); break;								
								case "number": dataItem = Number(dataItem).toLocaleString('en'); break;
								case "percent": {
									var value = Number(dataItem);
									if (value < 1.0) value = value * 100;
									dataItem = String(value.toLocaleString('en'));
									break;
								}
								case "currency": {
									var i = parseFloat(dataItem);
									if (isNaN(i)) {
										i = 0.00;
									}
									var showComma = true;
									var minus = (i < 0) ? '' : '';
									i = Math.abs(i);
									i = parseInt((i + .005) * 100);
									i = i / 100;
									var s = showComma ? Number(dataItem).toLocaleString('en') : new String(i);
									if (s.indexOf('.') < 0) { s += '.00'; }
									if (s.indexOf('.') == (s.length - 2)) { s += '0'; }
									s = minus + s;
									dataItem = s;
									break;
								}
								case "currency3": {
									var i = parseFloat(dataItem);
									if (isNaN(i)) {
									i = 0.000;
									}
									var showComma = true;
									var minus = (i < 0) ? '' : '';
									i = Math.abs(i);
									i = parseInt((i + .0005) * 1000);
									i = i / 1000;
									var s = showComma ? Number(dataItem).toLocaleString('en') : new String(i);
									if (s.indexOf('.') < 0) { s += '.000'; }
									if (s.indexOf('.') == (s.length - 2)) { s += '00'; }
									if (s.indexOf('.') == (s.length - 3)) { s += '0'; }
									s = minus + s;
									dataItem = s;
									break;
								}
				
							}
		
							break;
						}
				
						case 'concat':
						case 'string': {
							if ((dataItem=='undefined') || (dataItem==null)) {
								dataItem = '';
							} else {
								if (dataItem.length > formatting) {
									dataItem = dataItem.substring(0, formatting) + '...';
								}
							}
							break;
						}
				
						case 'epoch': {
							if ((dataItem == null) || (dataItem=='undefined')) {
								dataItem = '';
							} else {
								var d = new Date(0); // The 0 there is the key, which sets the date to the epoch
								d.setUTCSeconds(dataItem);
								dataItem = d.format(formatting);
							}
							break;
						}
				
						case 'date': {
							try {
								if ((dataItem == null) || (dataItem=='undefined')) {
									dataItem = '';
								} else {									
									date = Date.frommysql(dataItem);
									dataItem = date.format(formatting);
								}
							}
							catch (err) {
								console.info('error in line = '+line);								
							}
							break;
						}
										
					}
										
				}
				
				line = ((dataItem != null) && (dataItem !='undefined') && (dataItem != '')) ?
						line.replace(m[1], dataItem) : line.replace(m[1], defaultvalue);
				
			} else {
				
				var oHtml = '<ul class="children clear">';
				
				if ((dataItem != null) && (dataItem.length>0)) {

					arraycontent = arraycontent.replace(/&amp;37;/gi,'%');
					arraycontent = arraycontent.replace(/&amp;35;/gi,'#');
					arraycontent = arraycontent.replace(/&amp;92;/gi,'\'');
					arraycontent = arraycontent.replace(/&amp;47;/gi,'/');
					arraycontent = arraycontent.replace(/&amp;61;/gi,'=');
					arraycontent = arraycontent.replace(/&amp;7c;/gi,'|');
					arraycontent = arraycontent.replace(/&amp;gt/gi,'>');
				
					for (var counter = 0; counter< dataItem.length; counter++) {
				
						var subst = this.doVarSubstitution(dataItem[counter], arraycontent);
				
						if ((dataItem[counter] != null) && (dataItem[counter].id != 'undefined') && (dataItem[counter].id != null)) {
							oHtml += '<li data-id="' + dataItem[counter].id + '"' + subst + '</li>';							
						} else {
							oHtml += '<li ' + subst + '</li>';
						}
				
					}
				
				}
				
				oHtml += '</ul>';
				
				line = line.replace(m[1], oHtml);
			}
						
		}
		
		line = this.checkRepeats(line);
				
		var out = this.checkConditions(line);
			
		//out = out.replace(/__percent__/gi,'%');

		return out;
		
	},		

	sortOn : function(arr) {
		if (arr && arr.length > 0) {
			return function(a,b) {
				var asub, bsub, prop, direction;
				for (var i=0; i<arr.length; i++) {
					prop = arr[i];
					if (prop[0]=='!') {
						direction = -1;
						prop = prop.substring(1);
					} else {
						direction = 1;
					}
				
					var v1 = Object.byString(a, prop);
					var v2 = Object.byString(b, prop);
				
					asub = (v1 != null) ? v1 : '';
					bsub = (v2 != null) ? v2 : '';
				
					if (asub < bsub) return (direction*-1);
					if (asub > bsub) return (direction*1);
				}
				return 0;
			};
		} else {
			return function(a,b) { return a<=b; };
		}
	}
	
};

App.UI.DataServices = {

	dataStore : new Hashtable(),
	oldData : new Hashtable(),
	curPtrs : new Hashtable(),
	dataitems : new Hashtable(), //persistent datastorage
	
	hasInit : false,

	__preinit : function() {
	
		if (this.hasInit) return;
		this.hasInit = true;
	
		$('*').bind('page-refresh page-changed window-refresh', function(object, data) {
			if (data == 'undefined') data = null;
			if (object.type == 'page-changed') {
				while (App.UI.DataServices.curPtrs.count() > 0) {
					var pointer = App.UI.DataServices.curPtrs.pop();		
					if (pointer != null) pointer.abort();				
				}
				App.UI.DataServices.refresh();
			}
		});
	},
	
	getDataItem : function(spacename, data) {
		if (data=='undefined') data = null;
		if ((spacename==null) || (spacename=='undefined')) return null;
		
		if (!App.UI.DataServices.dataitems.exists(spacename)) {
			if (data!=null) {
				App.UI.DataServices.dataitems.add(spacename, data);				
			} else {
				App.UI.DataServices.dataitems.add(spacename, new Array());
			}
			console.info('created dynamic memory space '+spacename);
		} else {
			if (data != null) {
				App.UI.DataServices.dataitems.add(spacename, data);
			}
		}
		return App.UI.DataServices.dataitems.get(spacename);
	},
	
	getData : function(url, target, callback, usecache) {
		
		if (callback==null) return;
				
		if ((usecache == null) || (usecache == 'undefined')) {
			usecache = true;
		}
		
		if (usecache && (App.UI.DataServices.oldData.indexof(url) != -1)) {
			callback(App.UI.DataServices.oldData.get(url), target);
			return;
		}
				
		var pointer = $.ajax({
			type: "get",
			async: true,
			timeout: 5000,
			dataType: "text",										// we get this as text as otherwise cant do comparison
			error: function(data) {
				App.UI.DataServices.__recoverFailed(data, target);
				callback(null, target);
			},
			fail: function(data) {
				console.info(data);
				App.UI.DataServices.__recoverFailed(data, target);
				callback(null, target);
			},
			success: function(data) {
				App.UI.DataServices.oldData.add(url, data);
				App.UI.DataServices.curPtrs.remove(url);
				callback(data, target);
			},
			headers: {
				"session_id":App.Core.Security.sessionId
			},
			url: url, 
			data:{}
		});		
		
		App.UI.DataServices.curPtrs.add(url, pointer);
		
	},
		
	__recoverFailed : function(data, target) {
		$(target).attr('data-callinpro', false);
	},
	
	clear : function() {
		// console.info('info / Dataservices clear of all data');
		App.UI.DataServices.oldData.clear();
		App.UI.DataServices.dataStore.clear();		
	},
	
	refresh : function() {
		// clear the data !!
		App.UI.DataServices.clear();
	}	
	
};


App.UI.DataSelect = {

				hasInit : false,
				
				
				__preinit : function() {
				
					if (this.hasInit) return;
					this.hasInit = true;
				
					$('*').bind('page-refresh window-refresh', function(object, data) {
								App.UI.DataSelect.refresh(data);
							});
				
					$('*').bind('data-refresh', function(object, data) {
							if (data != null) {
								var componenttype = $(data).attr("data-component");
								if (componenttype == "repeater") {
									App.UI.DataSelect.__createList($(data));
								}
							}
						});
				
					$(document).delegate('select[data-datasource]', 'change', function(oEvent) {
										 App.UI.DataSelect.__createList(oEvent.currentTarget);
									 });
				
				},
				
				refresh : function(target) {
				
					if ((target=='undefined') || (target==null)) target = null;
				
					if ((target==null) || (typeof(target) == 'object')) {
						$('body').find('select[data-datasource]').each(function() {
															   App.UI.DataSelect.__createList(this);
														   });
					} else {
						$(target).find('select[data-datasource]').each(function() {
																   App.UI.DataSelect.__createList(this);
															   });
					}
				},
				
				__createList : function(target) {
				
					if (target==null) return;
				
					var datasource = $(target).attr('data-datasource');
					if ((datasource=='undefined') || (datasource==null)) datasource = null;
			
					var isnew = $(target).attr('data-ready');
					if ((isnew=='undefined') || (isnew==null)) {
						isnew = true;
					} else {
						isnew = isnew.toString().bool();
					}
					$(target).attr('data-ready', isnew);
			
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
							App.UI.DataServices.getData(datasource, target, App.UI.DataSelect.__processJsonData);
						}
			
					}
			
				},

				__processJsonData : function(datain, target) {
				
					if ((datain == null) || (target == null)) return;
				
					$(target).attr('data-callinpro', false);
				
					var dataselected = $(target).attr("data-selected");
					var data = jQuery.parseJSON(datain);
								
					var options = $("option:not(:disabled)", target);
				
					if (options.length > 0) {
						$(options).remove();
					}
				
					for (var counter=0; counter< data.length; counter++) {
						var dataitem = data[counter];
						if ((dataselected != "-1") && (dataselected == dataitem.uid)) {
							$(target).append("<option selected='selected' value='" + dataitem.uid + "'>" + dataitem.display + "</option>");
						} else {
							$(target).append("<option value='" + dataitem.uid + "'>" + dataitem.display + "</option>");
						}
					}
				
					if (dataselected == "-1") {
						$(target).attr('selectedIndex', '-1');
					}
				
				}
				
};

App.UI.Select = {
				
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		$('*').bind('data-refresh', function(object, data) { App.UI.Select.__refreshReceived(data); });	
				
	},

	__refreshReceived : function(data) {

		$('body').find('select[data-max]').each(function() {
			App.UI.Select.__setupSelector(this);
		});
				
		$('body').find('select[data-value]').each(function() {						
			App.UI.Select.__updateSelector(this); 			
		});
				
		$('body').find('[data-value].radio.group').each(function() {
			App.UI.Select.__updateRadios(this);
		});
				
	},

	refresh : function() {
		this.__refreshReceived(null);
	},
	
	__setupSelector : function(target) {
		if (target==null) return;
		if ($(target).parents('.template').length != 0) return;
		var max = $(target).attr('data-max');
		$('option[value]', $(target)).remove();
		for (var counter=0; counter <= max; counter++) {
			$(target).append("<option value='"+counter+"'>"+counter+"</option>");
		}
	},
				
	__updateSelector : function(target) {
		if (target==null) return;
		if ($(target).parents('.template').length != 0) return;
		var optionValue = $(target).attr('data-value');
		$(target).val(optionValue);
		$(target).trigger("change");
		//$('option[value='+ optionValue +']', $(target)).attr('selected', 'selected');
		//$('option[value='+ optionValue +']', $(target)).change();
	},
				
	__updateRadios : function(target) {
		if (target==null) return;
				
		var groupname = $(target).attr("data-group");
		var radios = $(target).find("input:radio");
		var optionValue = $(target).attr('data-value');
				
		if ((optionValue == null) || (optionValue == 'undefined') || (optionValue == '')) {
			optionValue = 0;
		}
				
		if (radios != null) {
				
		var fn = function(option, optionValue) {
					var tagname = $(option).attr('name')
					if (tagname == groupname) {
						var sInputValue = $(option).val();
						if (sInputValue == optionValue) {
							if ($(option).is(':checked') === false) {
								$(option).prop('checked', true);
							}
						}
					}
				};
				
			for (var counter=0; counter < radios.length; counter++) {
				fn(radios[counter], optionValue);
			}

		}
				
//		if ($(target).parents('.template').length != 0) return;
//		var optionValue = $(target).attr('data-value');
//		$('option[value='+ optionValue +']', $(target)).attr('selected', 'selected');
	}
		
};
				
App.UI.UpdatingInput = {
				
			hasInit : false,
				
			__preinit : function() {
				
				if (this.hasInit) return;
				this.hasInit = true;
				
				$('*').bind('page-refresh window-refresh', function(object, data) { App.UI.SmartInput.refresh(null); });
				
				$(document).delegate('[data-component="updatinginput"]', 'change keyup onload', function(oEvent) {
									 App.UI.UpdatingInput.__trigger(oEvent.currentTarget);
									 });
				
			},
				
			refresh : function(target) {
				
				if ((target=='undefined') || (target==null)) target = null;
				
				if (target==null) {
					$('body').find('[data-component="updatinginput"]').each(function() {
																App.UI.UpdatingInput.setup(this);
															});
				} else {
					App.UI.UpdatingInput.setup(target);
				}
				
			},
				
			setup : function(target) {
				
				if (target == null) return;
				
				App.UI.UpdatingInput.__trigger(target);
				
			},
				
			__trigger : function(target) {
				
				var _event = $(target).data("event");
				if (_event != null && _event != 'undefined') {
					App.Core.Application.__handleEvent({'currentTarget':target}, 'event');
				}
				
			}
				
};
				
App.UI.SmartInput = {
	
	hasInit : false,
		
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;

		$('*').bind('page-refresh window-refresh', function(object, data) { App.UI.SmartInput.refresh(null); });
		
		$(document).delegate('[data-component="smart"]', 'change keyup', function(oEvent) {
			App.UI.SmartInput.setup(oEvent.currentTarget); 
		});				
	
	},
	
	refresh : function(target) {
		if ((target=='undefined') || (target==null)) target = null;		
		
		if (target==null) {
			$('body').find('[data-component="smart"]').each(function() { 
				App.UI.SmartInput.setup(this); 
			});			
		} else {
			App.UI.SmartInput.setup(target); 
		}
		
	},
	
	setup : function(target) {
				
		if ((target=='undefined') || (target==null)) return;
		
		var datatarget = $(target).attr('data-target');
		if ((datatarget=='undefined') || (datatarget=='')) datatarget = null;
		
		var dataprefix = $(target).attr('data-prefix');
		if ((dataprefix=='undefined') || (dataprefix==null)) dataprefix = '';
				
		var datavar = $(target).attr('data-var');
		if ((datavar=='undefined') || (datavar=='')) datavar = null;
		
		if ((datavar==null) || (datatarget==null)) return;		
		
		var currentvalue = null;
				
		switch (target.tagName)
		{
			case 'SELECT': {
				currentvalue = dataprefix + $(':selected', target).attr('data-value');	
				break;
			}
			case 'INPUT': {
				var value_ = $(target).val();
				var default_ = $(target).attr("data-default");
				if (value_ != default_) {
					currentvalue = dataprefix + $.URLEncode(value_);
				}
				break;
			}
			default: {
				console.info('object is unsupport at the moment / type ' + target.tagName);				
			}
		}
		
		var targetvalue = $('#'+datatarget).attr(datavar);
				
		if ((currentvalue != null) && (targetvalue != currentvalue)) {
				
			$('#'+datatarget).attr(datavar, currentvalue);
				
			var oData = {'object': target.id};
				
			if ($('#'+datatarget).attr('data-callinpro') == 'true') {
				$('#'+datatarget).attr('data-callinpro', 'false');
			}
				
			$('*').triggerHandler('data-refresh', ('#'+datatarget)); // inform everyone that the grid dynamics just changed !!
		}
		
	}
		
};


App.UI.DropDown = {
	
	hasInit : false,

	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		$('*').bind('data-refresh page-refresh', function(object, data) { App.UI.DropDown.refresh(null); });	
		
	},

	refresh : function(target) {

		if ((target=='undefined') || (target==null)) target = null;		
		
		if (target==null) {
			$('body').find('[data-component="dropdown"]').each(function() { 
				App.UI.DropDown.__getData(this); 
			});			
		} else {
			App.UI.DropDown.__getData(target); 
		}
		
	},

	__getData : function(target) {
		
		if (target==null) return;

		var datasource = $(this).attr('data-source');
		if ((datasource == 'undefined') || (datasource == null)) datasource = null;

		$.ajax({
			type: "get",
			dataType: "text",										// we get this as text as otherwise cant do comparison
			error: function(data) {
				// do nothing...
			},
			success: function(data) {

				var data = jQuery.parseJSON(datain);
				if (data == null) return;

				var propname = $(target).attr('data-propname');
				if ((propname == 'undefined') || (propname == null)) propname = 'display';
												
				var oHtml = '';
				if (data.length >0) {
					for (var counter=0; counter< data.length; counter++) {
						oHtml += '<option value="'+ data[counter].id +'">'+ data[counter][propname] +'</option>';												
					}
				}
				
				$('#'+ target).html(oHtml);
				$('#'+ target).change();
								
			},
			headers: {
				"session_id":App.Core.Security.sessionId
			},
			url:datasource, 
			data:{}
		});
		
	}
	
};

App.UI.Pager = {
	
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		$('*').bind('data-refresh', function(object, data) { App.UI.Pager.__refreshReceived(data); });	
		
		$(document).delegate('[data-component="pager"] .pager_info li', 'click', function(oEvent) {
			App.UI.Pager.mouseControl_page(oEvent);
		});
		
	},
	
	mouseControl_page : function(oEvent) {

		if (oEvent == null) return;
		
		// get the parent and then the data source as we are completely async..
		
		var parent = $(oEvent.currentTarget).parents('[data-component="pager"]');
		var datasource = $(parent).attr('data-source');
		
		if ((datasource == 'undefined') || (datasource == null)) datasource = null;		
		if (datasource==null) return;

		var source = $('#'+datasource);
		if (source==null) return;
		
		var sourcetype = $(source).attr('data-component');
		var pageInfo = null;

		switch (sourcetype) {
			case 'list': {
				pageInfo = App.UI.List.getPageInfo(source);				
				break;
			}
			case 'repeater': {
				pageInfo = App.UI.Repeater.getPageInfo(source);				
				break;
			}
			default: {
				break;
			}
		}
		
		switch (oEvent.type) {
		
			case 'click': {			
				var pageno = -1;
				if ($(oEvent.currentTarget).hasClass('pageno')) {
					if ($(oEvent.currentTarget).hasClass('selected')) return;
					pageno = parseInt($(oEvent.currentTarget).attr('data-pageno'));
				}
				if ($(oEvent.currentTarget).hasClass('last')) {
					pageno = (pageInfo.pagemax-1);
				}
				if ($(oEvent.currentTarget).hasClass('start')) {
					pageno = 0;
				}
				if ($(oEvent.currentTarget).hasClass('next')) {
					if (pageInfo.pageno < (pageInfo.pagemax-1)) {
						pageno = pageInfo.pageno+1;
					}
				}				
				if ($(oEvent.currentTarget).hasClass('prev')) {
					if (pageInfo.pageno > 0) {
						pageno = pageInfo.pageno-1;
					}
				}
				if (pageno != -1) {
					$('li.selected', $(oEvent.currentTarget).parent()).removeClass('selected');
					switch (sourcetype) {
						case 'list': {
							App.UI.List.changePage(source, pageno);											
							break;
						} 
						case 'repeater': {
							App.UI.Repeater.changePage(source, pageno);				
							break;
						}
					}
					//$('li.pageno[data-pageno|="'+ pageno +'"]', $(oEvent.currentTarget).parent()).addClass('selected');
					this.__createPager(parent, false);
				}
				break;
			}
		
		}
		
	},
	
	__refreshReceived : function(data) {
	
		if (data==null) return;
		
		$('body').find('[data-component="pager"]').each(function() {			
			
			var datasource = $(this).attr('data-source');
			if ((datasource == 'undefined') || (datasource == null)) datasource = null;
			
			var notificationsource = $(data.object).attr('id');
			if ((notificationsource == 'undefined') || (notificationsource == null)) notificationsource = null;
			
			if ((notificationsource != null) && (notificationsource == datasource)) {
				App.UI.Pager.__createPager(this, data.datachanged); 
			}
			
		});		
		
	},
	
	__createPager : function(target, datachanged) {
		
		if (target==null) return;	
		// when we get here we are inside the pager...
		
		var datasource = $(target).attr('data-source');
		if ((datasource == 'undefined') || (datasource == null)) datasource = null;		
		if (datasource==null) return;
		
		var source = $('#'+datasource);
		if (source==null) return;
		
		var sourcetype = $(source).attr('data-component');
		var pageInfo = null;

		switch (sourcetype) {
			case 'list': {
				pageInfo = App.UI.List.getPageInfo(source);				
				break;
			}
			case 'repeater': {
				pageInfo = App.UI.Repeater.getPageInfo(source);				
				break;
			}
			default: {
				break;
			}
		}
		
		if (pageInfo==null) return;

		var pagefrom = pageInfo.pageno - 1;
		var pageto = pageInfo.pageno + 3;
		
		if (pagefrom < 1) pagefrom = 1;
		if (pageto > pageInfo.pagemax) pageto = pageInfo.pagemax;

		if (datachanged) {
		
			oHtml = '<ul class="pager_info">';
			
			oHtml += '<li class="start"><span>«</span></li>';
			oHtml += '<li class="prev"><span>‹</span></li>';
				
			for (var pageno=1; pageno<=pageInfo.pagemax; pageno++) {		
				if ((pageno>=pagefrom) && (pageno<=pageto)) {
					oHtml += '<li class="pageno' + (((pageno-1)==pageInfo.pageno)?' selected':'') +'" data-pageno="'+ (pageno-1) + '"><span>'+ pageno + '</span></li>';				
				} else {
					oHtml += '<li class="pageno' + (((pageno-1)==pageInfo.pageno)?' selected':'') +'" style="display: none;" data-pageno="'+ (pageno-1) + '"><span>'+ pageno + '</span></li>';
				}
			}
			
			oHtml += '<li class="next"><span>›</span></li>';
			oHtml += '<li class="last"><span>»</span></li>';
			
			oHtml += '</ul>';
			
			$(target).html(oHtml);
		
		} else {

			var lis = $('li.pageno', $(target));
			$(lis).removeClass('selected');
			for (var pageno=1; pageno<= lis.length; pageno++) {
				if ((pageno-1)==pageInfo.pageno) {
					$(lis[pageno-1]).addClass('selected');
				}
				$(lis[pageno-1]).css({'display':( ((pageno>=pagefrom) && (pageno<=pageto)) ? 'inline-block':'none' )});
			}
			
		}
		
	}
	
};


App.UI.List = {
	
	hasInit : false,
	
	__preinit : function() {
		
		if (this.hasInit) return;
		this.hasInit = true;
		
		$('*').bind('page-refresh window-refresh', function(object, data) {
			App.UI.List.refresh(data);
		});
		
//		$(document).delegate('[data-component="list"] dt.row', 'click', function(oEvent) {
//			App.UI.List.mouseControl_row(oEvent);
//		});
		
		$(document).delegate('[data-component="list"] dt.titlebar .sortable', 'click', function(oEvent) {
			App.UI.List.mouseControl_sort(oEvent);
		});
				
		$('*').bind('data-refresh', function(object, data) {
			if (data != null) {
				var componenttype = $(data).attr("data-component");
				if (componenttype == "list") {
					App.UI.List.__createList($(data));
				}
			}
		});
		
	},
				
	refresh : function(target) {
				
		if ((target=='undefined') || (target==null)) target = null;
				
		if ((target==null) || (typeof(target) == 'object')) {
				$('body').find('[data-component="list"]').each(function() {
				   var listento = $(this).attr('data-listento');
				   if ((listento == 'undefined')||(listento == null)) {
						App.UI.List.__createList(this);
					} else {
					   var listenarray = listento.split(',');
					   if (listenarray.indexOf(listento)!=-1) {
						   App.UI.List.__createList(this);
				   }
				   }
			   });
		} else {
			if ($(target).attr('data-component') != null) {
				App.UI.List.__createList($(target));
			} else {
				$(target).find('[data-component="list"]').each(function() {
																   App.UI.List.__createList(this);
																   });
			}
				
		}
				
	},
	
	mouseControl_sort : function(oEvent) {
		
		switch (oEvent.type) {
			
			case 'click': {
				
				var sortField = $(oEvent.currentTarget).attr('data-sort');
				if ((sortField=='undefined') || (sortField==null)) sortField = '';
				
				var parent = $(oEvent.currentTarget).parents('[data-component="list"]');	
				if (!$(oEvent.currentTarget).hasClass('sort')) {
					$('dt.titlebar .sortable.sort', parent).removeClass('sort');
				}
				$('dt.titlebar .sortable.desc', parent).removeClass('desc');
				
				var currentSearch = $(parent).attr('data-sorton');
				if ((currentSearch == 'undefined') || (currentSearch == null)) currentSearch = '';
				
				if (currentSearch != '') {
					if (currentSearch[0]!='!') {
						if (currentSearch==sortField) {
							// invert the search...
							sortField = '!' + sortField;
							$(oEvent.currentTarget).addClass('desc');
						}
					} 
				}				
				
				$(parent).attr('data-sorton', sortField);
				
				if (!$(oEvent.currentTarget).hasClass('sort')) {
					$(oEvent.currentTarget).addClass('sort');
				}
				
				if (sortField[0] == '!') {
					$(oEvent.currentTarget).addClass('desc');
				}

				// refreshes the data
				this.__processJsonData(null, parent, true);	
				
				break;
			}
			
		}
		
	},
	
	mouseControl_row : function(oEvent) {

		if (($(oEvent.target).hasClass('pagenav')==true) || ($(oEvent.target).attr('data-event')!=null) || ($(oEvent.target).attr('data-url')!=null)) {
			oEvent.preventDefault();
			return;
		}
		
		switch (oEvent.type) {
					
			case 'click': {

				var parent = $(oEvent.currentTarget).parents('[data-component="list"]');
				
				var mode = $(parent).attr('data-mode');				
				if ((mode == 'undefined') || (mode == null)) mode = null;					
																				
				if (mode != null) {
					
					switch (mode) {
					
						case 'true': 
						case 'multi': {
							if ($(oEvent.currentTarget).hasClass('selected')) {
								$(oEvent.currentTarget).removeClass('selected');				
							} else {
								$(oEvent.currentTarget).addClass('selected');											
							}							
							break;
						}
						
						case '2state': {
							if ($(oEvent.currentTarget).hasClass('selected')) {
								$(oEvent.currentTarget).removeClass('selected');				
							} else {
								$('dt.selected', $(oEvent.currentTarget).parents('dl')).removeClass('selected'); // clear anything already selected...
								$(oEvent.currentTarget).addClass('selected');											
							}								
							break;
						}
					
					}
					
				} else {
					
					if ($(oEvent.currentTarget).hasClass('selected')) return; // dont do anything as its already selected									
					$('dt.selected', $(oEvent.currentTarget).parents('dl')).removeClass('selected'); // clear anything already selected...
					$(oEvent.currentTarget).addClass('selected');
					
				}
				
				var selection = this.getSelected(parent);				
				
				/* if there are no items selected, we still raise an event */
				var oData = {'object': parent, 'selected':selection};				
				$('*').triggerHandler('row-selected', oData);

				break;
				
			}
		
		}		
		
	},

	/* allow direct access just in case */
	getSelected : function(target) {

		var selection = new Array();
		if (target==null) return selection;

		var items = $('dl', target).find('dt.row.selected');
		
		if (items.length > 0) {
			selection = new Array();
			for (var counter=0; counter<items.length; counter++) {
				selection.push($(items[counter]).attr('data-id'));
			}
		}
		
		return selection;
		
	},

	reload : function(target) {
		
		this.__createList(target);
		
	},
	
	changePage : function(target, pageNo) {

		if (target==null) return;		
		pageNo = ((pageNo == 'undefined') || (pageNo == null)) ? 0 : parseInt(pageNo);
		
		var pageInfo = this.getPageInfo(target);
		if ((pageNo >= 0) && (pageInfo.pageno != pageNo) && (pageNo < pageInfo.pagemax)) {
			// change the page number...
			$(target).attr('data-page', pageNo);			
			//refresh the page
			this.__processJsonData(null, target, true);	
		}
		
	},
	
	__createList : function(target) {

		if (target==null) return;
		
		var datasource = $(target).attr('data-datasource');
		if ((datasource=='undefined') || (datasource==null)) datasource = null; 
		
		var isnew = $(target).attr('data-ready');
		if ((isnew=='undefined') || (isnew==null)) {
			isnew = true; 
		} else {
			isnew = isnew.toString().bool();
		}
		$(target).attr('data-ready', isnew);
		
		if (isnew) {
			$(target).parents('.i_panel.hidden').css({'display':'none'});
		}
		
		var callinpro = $(target).attr('data-callinpro');
		if ((callinpro=='undefined') || (callinpro==null)) { 
			callinpro = false;		
		} else {
			callinpro = callinpro.toString().bool();
		}
				
		if ($('dl.row_column', target).length>0) {
			// already has a ul specification
		} else {
			$(target).append('<dl class="row_column"></dl>');
		}
		
		if ((datasource != null) && (datasource != '')) {

			if (callinpro) return;
			$(target).attr('data-callinpro', true);
			
			if (datasource.startsWith('arr:')) {			
				var space = datasource.substring(4);
				var memData = App.UI.DataServices.getDataItem(space);
				this.__processJsonData(memData, target, false);
			} else {
				App.UI.DataServices.getData(datasource, target, App.UI.List.__processJsonData);				
			}
			
		}
				
	},
	
	getPageInfo : function(target) {
		
		var pageno = $(target).attr('data-page');
		pageno = ((pageno == 'undefined') || (pageno == null)) ? 0 : parseInt(pageno);

		var pagesize = $(target).attr('data-pagesize');
		pagesize = ((pagesize == 'undefined') || (pagesize == null)) ? 0 : parseInt(pagesize);

		var pagemax = $(target).attr('data-pagemax');
		pagemax = ((pagemax == 'undefined') || (pagemax == null)) ? 0 : parseInt(pagemax);
		
		var offset = pageno*pagesize; // calculate the offset of the data

		return {'pageno': pageno, 'pagesize': pagesize, 'pagemax': pagemax, 'offset': offset};
		
	},

	filter : function(target, filter) {
		if (target==null) return;
		if ((filter=='undefined') || (filter==null)) filter = '';
		$(target).attr('data-filter', filter);
		this.__processJsonData(null, target, true);
	},
	
	__processJsonData : function(datain, target, dataonly) {
		
		if (datain != null) {
			$(target).attr('data-callinpro', false);
		}

		var isnew = $(target).attr('data-ready');
		isnew = isnew.toString().bool();
		
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

		var oHtml = '';								
		var datachanged = (datain!=null);
		var max = 0;
		var maxpages = 0;
		
		var storeId = $(target).attr('id');
		if ((storeId == 'undefined') || (storeId==null)) storeId = null;

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
		
		// set up the templates - all should be display:none to be sure no ui glitch...
		var template_header = App.UI.Core.get(storeId, '.row');
		var template_data = App.UI.Core.get(storeId, '.data'); 
		var template_title = App.UI.Core.get(storeId, '.header');
		var template_footer = App.UI.Core.get(storeId, '.footer');
		var template_noresults = App.UI.Core.get(storeId, '.noresults');
				
		// reset the template if it doesnt exist...
		if ((template_header == 'undefined') || (template_header == null)) template_header = '';		
		if ((template_data == 'undefined') || (template_data == null)) template_data = '';

		if ((!dataonly) && (template_title != 'undefined') && (template_title != null)) {
			oHtml += '<dt class="header">' + template_title + '</dt>';
		}
		
		var pageInfo = App.UI.List.getPageInfo(target);
		var _rowClass = '';
		var _rowdataClass = '';
		var _eventInfo = null;
		var _eventUrl = null;
		var id = null;
		var filter = null;
		
		if ((data != null) && (data.length>0)) {
		
			// do sorting !!
			var sorton = $(target).attr('data-sorton');
			sorton = ((sorton == 'undefined') || (sorton == null)) ? null : sorton.split(',');		
			
			if ((sorton != null) && (sorton != '')) data.sort(App.UI.Core.sortOn(sorton));

			var filteron = $(target).attr('data-filteron');
			filteron = ((filteron == 'undefined') || (filteron == '')) ? null : filteron;		
	
			filter = $(target).attr('data-filter');
			filter = ((filter == null) || (filter == 'undefined') || (filter == '')) ? null : filter;
					
			if ((filteron != null) && (filter != null)) {
				var filteredData = new Array();
				$.each(data, function(i, item) {
					if (item != null) {
					   var check = Object.byString(item, filteron);
					   if (check != null) {
						   if (check.toLowerCase().indexOf(filter) != -1) {
							   filteredData.push(item);
						   }
					   }
					}
				});
				data = filteredData;
			}

			_eventInfo = App.UI.Core.attr(storeId, '.row', 'data-event');
			if ((_eventInfo == 'undefined') || (_eventInfo == null)) _eventInfo = null;

			_rowClass = App.UI.Core.attr(storeId, '.row', 'data-rowclass'); 
			if ((_rowClass == 'undefined') || (_rowClass == null)) _rowClass = '';

			_eventUrl = App.UI.Core.attr(storeId, '.row', 'data-url');
			if ((_eventUrl == 'undefined') || (_eventUrl == null)) _eventUrl = null;
				
			_rowdataClass = App.UI.Core.attr(storeId, '.data', 'data-rowclass');
			if ((_rowdataClass == 'undefined') || (_rowdataClass == null)) _rowdataClass = '';

			id = $(target).attr('data-id');
			if ((id == 'undefined') || (id == null)) id = '';
			
			// get paging information		
			
			if ((data != null) && (data.length > 0) && (pageInfo.pagesize > 0)) {
				max = ((pageInfo.offset+pageInfo.pagesize)>data.length) ? data.length : (pageInfo.offset+pageInfo.pagesize);
				maxpages = parseInt(data.length / pageInfo.pagesize) + (((data.length % pageInfo.pagesize) != 0) ? 1 : 0 ); 			
			} else {
				if ((data == null) || (data.length == 0)) {
					max = 0;
				} else {
					if (pageInfo.pagesize==0) {
						max = data.length;
					}
				}
			}		
			
			$(target).attr('data-pagemax', maxpages);
			if ((pageInfo.pageno< 0) || (pageInfo.pageno>maxpages)) pageInfo.pageno = 0; // move to the front again as the data isnt there...
			$(target).attr('data-page', pageInfo.pageno); // write the page number back to the service as required
			
		} else {
			
			$(target).attr('data-pagemax', 0);
			$(target).attr('data-page', 0);
		
		}
				
		// present data
		
		if ((data != null) && (data.length > 0)) {
			
			if ($(target).hasClass("noresults")) {
				$(target).removeClass("noresults");
			}
				
			if ($('.noresults', target)) $('.noresults', target).hide();
			if ($('.results.static', target)) $('.results.static', target).show();
									
			var row_counter=0;
			
			// oHtml += '<dt class="spacer"></dt>';
				
			for (var counter=pageInfo.offset; counter < max; counter++) {
								
				var rowClass = ''; //((counter-pageInfo.offset) % 2)==0?'even':'odd';
				var rowdataClass = '';
				
				if (_rowClass != '') rowClass += (' ' + App.UI.Core.doVarSubstitution(data[counter], _rowClass));
				if (_rowdataClass != '') rowdataClass += (' ' + App.UI.Core.doVarSubstitution(data[counter], _rowdataClass));
				
				// make variable substitution here....
				var output_header = App.UI.Core.doVarSubstitution(data[counter], template_header);
				var output_data = App.UI.Core.doVarSubstitution(data[counter], template_data);
				
				var eventInfo = (_eventInfo != null) ? App.UI.Core.doVarSubstitution(data[counter], _eventInfo) : null;
				var eventUrl =  (_eventUrl  != null) ? App.UI.Core.doVarSubstitution(data[counter], _eventUrl)  : null;
				
				oHtml += '<dt class="row odd '+rowClass+'" data-rowindex="'+ row_counter+'" data-id="';				
				oHtml += ((data[counter] != null) && (id != '') && (data[counter][id] != null)) ? data[counter][id] : counter;  
				oHtml += '"';
				
				oHtml += (eventInfo != null) ? (' data-event="'+ eventInfo +'"') : "";
				oHtml += (_eventUrl != null) ? (' data-url="'+ eventUrl + '"') : "";
				
				oHtml += '>'+ output_header + '</dt>';

				if (output_data != '') oHtml += '<dd class="data '+rowdataClass+'">'+ output_data +'</dd>';				
				
				row_counter++;
				
			}
			
			var currentdata = {'rows_total':data.length, 'rows_shown': row_counter};
			
			var output_footer = App.UI.Core.doVarSubstitution(currentdata, template_footer);			
			if ((template_footer != 'undefined') && (template_footer != null) && (template_footer != '')) oHtml += '<dt class="footer">'+ output_footer +'</dt>';
			
		} else {

			if (!$(target).hasClass("noresults")) {
				$(target).addClass("noresults");
			}

			var output_footer = App.UI.Core.doVarSubstitution(currentdata, template_noresults);
			if ((template_noresults != 'undefined') && (template_noresults != null) && (template_noresults != '')) oHtml += '<dt class="noresults">'+ output_footer +'</dt>';

			if ($('.noresults.static', target)) $('.noresults.static', target).show();
			if ($('.results.static', target)) $('.results.static', target).hide();								
				
		}
		
		if (!dataonly) {
			$('dl.row_column', target).html(oHtml);
		} else {
			$('dl.row_column dt.row, dl.row_column dt.spacer, dl.row_column dd, dl.row_column dt.footer', target).remove();
			$('dl.row_column', target).append(oHtml);
		}
		
		if (isnew) {
			$(target).parents('.i_panel.hidden').fadeIn();
			$(target).attr('data-ready', 'false');
		}
		
		var oData = { 'object': target, 'pageno': pageInfo.pageno, 'datachanged': (datachanged || (filter != null)) }; 		
		
		$('*').triggerHandler('html-changed', target);
		$('*').triggerHandler('data-refresh', oData); // inform everyone that the grid dynamics just changed !!

	},
		
	__recoverFailed : function(datain, target) {
		/* data not received */
		$(target).attr('data-callinpro', false);
	}
		
};
				

App.UI.Filter = {
				
	hasInit : false,
				
	__preinit : function() {
				
		if (this.hasInit) return;
		this.hasInit = true;
				
		$('*').bind('page-refresh', function(object, data) { App.UI.Filter.refresh(); });
		$(document).delegate('[data-component="filter"] input[type=text]', 'keyup', function(oEvent){ App.UI.Filter.content_Changed(oEvent); });
				
	},
				
	content_Changed : function(oEvent) {
				
		var currentText = '';
				
		if (oEvent == null) return;
				
		switch (oEvent.type) {
				
			case 'keyup':{
				currentText = $(oEvent.currentTarget).attr('value');
				break;
			}
				
		}
				
		// get the parent and then the data source as we are completely async..
				
		var parent = $(oEvent.currentTarget).parents('[data-component="filter"]');
		var datasource = $(parent).attr('data-source');
				
		if ((datasource == 'undefined') || (datasource == null)) datasource = null;
		if (datasource==null) return;
				
		var source = $('#'+datasource);
		if (source==null) return;
				
		var sourcetype = $(source).attr('data-component');
				
		switch (sourcetype) {
				
			case 'list': {
				App.UI.List.filter(source, currentText);
				break;
			}
				
			case 'repeater': {
				App.UI.Repeater.filter(source, currentText);
				break;
			}
				
			default: {
				break;
			}
				
		}
				
	},
				
	refresh : function() {
		$('body').find('[data-component="filter"]').each(function() {
														 App.UI.Filter.__setupFilter(this);
													 });
	},
				
	__setupFilter : function(target) {
				
	}
				
};
				
				
App.UI.SortOn = {
				
				hasInit : false,
				
				__preinit : function() {
				
					if (this.hasInit) return;
					this.hasInit = true;
					
					$('*').bind('page-refresh', function(object, data) { App.UI.SortOn.refresh(); });
				
					$(document).delegate('[data-component="sorter"]', 'click', function(oEvent){ App.UI.SortOn.__clicked(oEvent); });
				
				},
				
				__clicked : function(oEvent) {
				
					var target = oEvent.currentTarget;
					var filter = $(target).attr("data-sorton");
					var parent = $(target).parents("[data-component='repeater'],[data-component='list']");
				
					var direction = "";
				
					if ($(target).hasClass('up')) {
						$(parent).find('[data-sorton]').each(function() {
														 $(this).removeClass('up');
														 $(this).removeClass('down');
														 if (!$(this).hasClass('none')) {
															$(this).addClass('none');
														 }
													 });
						$(target).addClass('down');
					} else {
						$(parent).find('[data-sorton]').each(function() {
														 $(this).removeClass('up');
														 $(this).removeClass('down');
														 if (!$(this).hasClass('none')) {
															 $(this).addClass('none');
														 }
													 });
						$(target).addClass('up');
						direction = "!";
					}
			
					var sourcetype = $(parent).attr("data-component");
					var actualfilter = direction + filter;
				
					switch (sourcetype) {
				
						case 'list': {
//							App.UI.List.filter(parent, currentText);
							break;
						}
				
						case 'repeater': {
							$(parent).attr("data-sorton", actualfilter);
							var storeId = $(parent).attr('id');
							App.UI.Repeater.__processJsonData(null, "#"+storeId, true);
							break;
						}
				
						default: {
							break;
						}
					}
				
				},
				
				refresh : function() {
				
					$('body').find('[data-component="filter"]').each(function() {
																 App.UI.SortOn.__setupFilter(this);
																 });
				
				},
				
				__setupFilter : function(target) {
				
				}

				
				
	};
				
App.UI.AutoWidth = {

				hasInit : false,
				
				__preinit : function() {
				
					if (this.hasInit) return;
					this.hasInit = true;
				
					$('*').bind('page-refresh tab-changed html-changed window-refresh', function(object, data) {
							App.UI.AutoWidth.refresh(data);
						});
				
					$(window).resize(function() {
								 App.UI.AutoWidth.refresh(null);
								 return true;
								 });
				
				},
				
				refresh : function(target) {
				
					if ((target=='undefined') || (target==null)) target = null;
				
					if ((target==null) || (typeof(target) == 'object')) {
				
						$('body').find('.column.wauto').each(function() {
																	   App.UI.AutoWidth.__resolve(this);
																   });
					} else {
						$(target).find('.column.wauto').each(function() {
																		   App.UI.AutoWidth.__resolve(this);
																	   });
					}
				
				},
				
				__resolve : function(target) {
				
					if (target==null) return;

					var header = $(target).parents(".header");
				
					if ((header != null) && (header != 'undefined')) {

						var parent = $(header).parent();
						var allItems = $(header).find('.column');
						var fixedItems = $(header).find('.column:not(.wauto)');
						var totalWidth = $(header).width();
				
						var index = allItems.index(target);
				
						var width = 0;
				
						for (var counter=0; counter < fixedItems.length; counter++) {
							var fixedWidth = $(fixedItems[counter]).outerWidth(true);
							width += fixedWidth;
						}
				
						var difference = $(target).outerWidth(true) - $(target).width();
						var remainder = (totalWidth - (width + difference));
						var updatables = $(parent).find('.resizing');
				
						if (updatables.length > 0) {
							for (var counter=0; counter < updatables.length; counter++) {
								$(updatables[counter]).width(remainder);
							}
						}
				
						$(target).width(remainder);
				
					}
				
				}
				
			};


App.UI.Repeater = {
		
	hasInit : false,
	dataStore : null,
	
	__preinit : function() {

		if (this.hasInit) return;
		this.hasInit = true;

		$('*').bind('page-refresh window-refresh', function(object, data) {
			App.UI.Repeater.refresh(data); 
		});

		$('*').bind('data-refresh', function(object, data) {
			if (data != null) {
				var componenttype = $(data).attr("data-component");
				if (componenttype == "repeater") {
					App.UI.Repeater.__createList($(data));
				}
			}
		});

		$(document).delegate('[data-component="repeater"] ul > li.header .column', 'mouseover mouseout mouseleave', function(oEvent) { App.UI.Repeater.highlightColumn(oEvent); });

		App.UI.Repeater.dataStore = new Hashtable();

	},

	refresh : function(target) {
				
		if ((target=='undefined') || (target==null)) target = null;		
				
		if ((target==null) || (typeof(target) == 'object')) {
			$('body').find('[data-component="repeater"]').each(function() { 				
				var listento = $(this).attr('data-listento');
				if ((listento == 'undefined')||(listento == null)) {
					App.UI.Repeater.__createList(this); 					
				} else {
					var listenarray = listento.split(',');
					if (listenarray.indexOf(listento)!=-1) {
						App.UI.Repeater.__createList(this); 				
					}
				}				
			});			
		} else {
			if ($(target).attr('data-component') != null) {
				App.UI.Repeater.__createList($(target));				
			} else {
				$(target).find('[data-component="repeater"]').each(function() { 
					App.UI.Repeater.__createList(this);
				});
			}
			
			//$(target).find('[data-component="repeater"]').each(function() { 
			//	App.UI.Repeater.__createList(this); 
			//});			
		}
				
	},	
	
	__createList : function(target) {
		
		if (target==null) return;
		
		var datasource = $(target).attr('data-datasource');
		if ((datasource=='undefined') || (datasource==null)) datasource = null; 
		
		var callinpro = $(target).attr('data-callinpro');
		if ((callinpro=='undefined') || (callinpro==null)) { 
			callinpro = false;		
		} else {
			callinpro = callinpro.toString().bool();
		}
				
		if ($('ul.list', target).length>0) {
			// already has a ul specification
		} else {
			$(target).append('<ul class="list clear"></ul>');
		}
		
		var usecache = $(target).attr('data-cache');
		if ((usecache == null) || (usecache == 'undefined')) {
			usecache = true;
		} else {
			usecache = parseInt(usecache) == 1;
		}
				
		if ((datasource != null) && (datasource != '')) {

			if (callinpro) return;
			$(target).attr('data-callinpro', true);

			if (datasource.startsWith('arr:')) {			
				var space = datasource.substring(4);
				var memData = App.UI.DataServices.getDataItem(space);
				this.__processJsonData(memData, target, false);
			} else {
				App.UI.DataServices.getData(datasource, target, App.UI.Repeater.__processJsonData, usecache);
			}
			
		}
		
	},
				
	highlightColumn : function(oEvent) {
	
		var target = $(oEvent.currentTarget);
		var parent = $(oEvent.currentTarget).parents("li");

		var collection = $(parent).find(".column");
		var index = $(collection).index(target);
				
		switch (oEvent.type) {
				
			case 'mouseover': {
				
				break;
			}
				
			case 'mouseleave' : {
				
				break;
			}
				
			case 'mouseout': {
				
				break;
			}
				
		}
				
	},

	getPageInfo : function(target) {
		
		var pageno = $(target).attr('data-page');
		pageno = ((pageno == 'undefined') || (pageno == null)) ? 0 : parseInt(pageno);

		var pagesize = $(target).attr('data-pagesize');
		pagesize = ((pagesize == 'undefined') || (pagesize == null)) ? 0 : parseInt(pagesize);

		var pagemax = $(target).attr('data-pagemax');
		pagemax = ((pagemax == 'undefined') || (pagemax == null)) ? 0 : parseInt(pagemax);
				
		var pageoffset = $(target).attr('data-offset');
		pageoffset = ((pageoffset == 'undefined') || (pageoffset == null)) ? 0 : parseInt(pageoffset);
		
		var offset = pageoffset + (pageno*pagesize); // calculate the offset of the data

		return {'pageno': pageno, 'pagesize': pagesize, 'pagemax': pagemax, 'offset': offset};
		
	},

	changePage : function(target, pageNo) {

		if (target==null) return;		
		pageNo = ((pageNo == 'undefined') || (pageNo == null)) ? 0 : parseInt(pageNo);
		
		var pageInfo = this.getPageInfo(target);
		if ((pageNo >= 0) && (pageInfo.pageno != pageNo) && (pageNo < pageInfo.pagemax)) {
			// change the page number...
			$(target).attr('data-page', pageNo);			
			//refresh the page
			this.__processJsonData(null, target, true);	
		}
		
	},
	
	filter : function(target, filter) {
		if (target==null) return;
		if ((filter=='undefined') || (filter==null)) filter = '';
		$(target).attr('data-filter', filter);
		this.__processJsonData(null, target, true);
	},
				
	styleElement : function(storeId, elementId, tag) {

		var oHtml = "<" + tag;
				
		var template = App.UI.Core.get(storeId, elementId);
				
		if (elementId != null) {
				
			var _event = App.UI.Core.attr(storeId, elementId, 'data-event');
			if ((_event == 'undefined') || (_event == null)) _event = null;
				
			var _url = App.UI.Core.attr(storeId, elementId, 'data-url');
			if ((_url == 'undefined') || (_url == null)) _url = null;
				
			var _class = App.UI.Core.attr(storeId, elementId, 'data-itemclass');
			if ((_class == 'undefined') || (_class == null)) _class = null;
				
			var _style = App.UI.Core.attr(storeId, elementId, 'data-style');
			if ((_style == 'undefined') || (_style == null)) _style = null;

			oHtml += (_event != null) ? (' data-event="'+ _event +'"') : "";
			oHtml += (_url != null) ? (' data-url="'+ _url + '"') : "";
			oHtml += (_class != null) ? (' class="'+ _class +'"') : "";
			oHtml += (_style != null) ? (' style="'+ _style +'"') : "";

		}

		oHtml += ">";

		return oHtml;
				
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

		var oHtml = '';								
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
		
		var variable = $(target).attr('data-enumerate');
		if (variable != null && variable != 'undefined') {
			data = Object.byString(data, variable);
		}
				
		// set up the templates - all should be display:none to be sure no ui glitch...
		
		var template_item = App.UI.Core.get(storeId, '.item');
		var template_header = App.UI.Core.get(storeId, '.header');
		var template_staticbefore = App.UI.Core.get(storeId, '.static_before');
		var template_staticafter = App.UI.Core.get(storeId, '.static_after');

		// do sorting !!
		var sorton = $(target).attr('data-sorton');
		sorton = ((sorton == 'undefined') || (sorton == null)) ? null : sorton.split(',');		
		
		if ((sorton != null) && (sorton != '') && (data!=null) && (data.length>0)) {
			var sorting = App.UI.Core.sortOn(sorton);
			data.sort(sorting);
		}
		
		var filteron = $(target).attr('data-filteron');
		filteron = ((filteron == 'undefined') || (filteron == '')) ? null : filteron;		

		var filter = $(target).attr('data-filter');
		filter = ((filter == null) || (filter == 'undefined') || (filter == '')) ? null : filter;
				
		if ((filter != null) && (filteron != null) && (data != null) && (data.length > 0)) {
			var filteredData = new Array();
			filter = filter.toLowerCase();
			$.each(data, function(i, item) { 
				if (item != null) {
				    var check = Object.byString(item, filteron);
					if (check != null) {
						if (check.toLowerCase().indexOf(filter) != -1) {
							filteredData.push(item);
						}
				    }
				}
			});
			data = filteredData;
		} else {
			
		}
		
		// reset the template if it doesnt exist...
		if ((template_item == 'undefined') || (template_item == null)) { 
			template_item = '';		
		}
				
		var _selectedid = $(target).attr('data-selected');
				
		var _styleInfo = App.UI.Core.attr(storeId, '.item', 'data-style');
		if ((_styleInfo == 'undefined') || (_styleInfo == null)) _styleInfo = null;
				
		var _eventInfo = App.UI.Core.attr(storeId, '.item', 'data-event');
		if ((_eventInfo == 'undefined') || (_eventInfo == null)) _eventInfo = null;

		var _eventUrl = App.UI.Core.attr(storeId, '.item', 'data-url');
		if ((_eventUrl == 'undefined') || (_eventUrl == null)) _eventUrl = null;

		var _rowClass = App.UI.Core.attr(storeId, '.item', 'data-itemclass');
		if ((_rowClass == 'undefined') || (_rowClass == null)) _rowClass = null;
				
		var id = $(target).attr('data-id');
		if ((id == 'undefined') || (id == null)) id = '';
		
		// get paging information		
		var pageInfo = App.UI.Repeater.getPageInfo(target);
		var max = 0;
		var maxpages = 0;
		
		if ((data != null) && (data.length > 0) && (pageInfo.pagesize > 0)) {
			max = ((pageInfo.offset+pageInfo.pagesize)>data.length) ? data.length : (pageInfo.offset+pageInfo.pagesize);
			maxpages = parseInt(data.length / pageInfo.pagesize) + (((data.length % pageInfo.pagesize) != 0) ? 1 : 0 ); 			
		} else {
			if ((data == null) || (data.length == 0)) {
				max = 0;
			} else {
				if (pageInfo.pagesize==0) {
					max = data.length;
				}
			}
		}
					
		if ((pageInfo.pageno< 0) || (pageInfo.pageno>maxpages)) pageInfo.pageno = 0; // move to the front again as the data isnt there...
		$(target).attr({'data-pagemax':maxpages, 'data-page':pageInfo.pageno}); // write the page number back to the service as required		
		
		// present data
		
		if ((template_header != null) && (template_header != "undefined")) {
				
			var output_item = App.UI.Core.doVarSubstitution(null, template_header);
			var headerfound = $('ul.list li.item.header', target);
				
			if (((headerfound == null) && dataonly) || (!dataonly)) {
				oHtml += '<li class="item header">'+ output_item + '</li>';
			}
				
		}
				
		if ((data != null) && (data.length > 0)) {

			if ($(target).hasClass("noresults")) {
				$(target).removeClass("noresults");
			}
				
			if ($('.noresults.static', target)) $('.noresults.static', target).hide();
			
			for (var counter=pageInfo.offset; counter < max; counter++) {
								
				var rowClass = (_rowClass != null) ? ' ' + _rowClass : '';
				
				// make variable substitution here....
				if (rowClass != '') rowClass = App.UI.Core.doVarSubstitution(data[counter], rowClass);				
				var output_item = App.UI.Core.doVarSubstitution(data[counter], template_item);
				
				var _currentid = ((data[counter] != null) && (id != '') && (data[counter][id] != null)) ? data[counter][id] : counter;
				
				var styleInfo = (_styleInfo != null) ? App.UI.Core.doVarSubstitution(data[counter], _styleInfo) : null;
				var eventInfo = (_eventInfo != null) ? App.UI.Core.doVarSubstitution(data[counter], _eventInfo) : null;
				var eventUrl =  (_eventUrl  != null) ? App.UI.Core.doVarSubstitution(data[counter], _eventUrl)  : null;
				
				if (_selectedid != null && _selectedid != 'undefined' && _currentid == _selectedid) {
					rowClass = rowClass + ((_rowClass != '') ? ' ' : '') + "selected";
				}
				
				if ((counter % 2) == 0) {
					oHtml += '<li class="item'+rowClass+'" data-id="';
				} else {
					oHtml += '<li class="item odd'+rowClass+'" data-id="';
				}
				
				oHtml += _currentid + '"';
				
				oHtml += (styleInfo != null) ? (' style="'+ styleInfo +'"') : "";
				oHtml += (eventInfo != null) ? (' data-event="'+ eventInfo +'"') : "";
				oHtml += (_eventUrl != null) ? (' data-url="'+ eventUrl + '"') : "";
				
				oHtml += '>'+ output_item + '</li>';
				
			}
			
		} else {
			
			if (!$(target).hasClass("noresults")) {
				$(target).addClass("noresults");
			}
				
			if ($('.noresults.static', target)) $('.noresults.static', target).show();
			
		}
				
		if (template_staticbefore != null) {
			var _beforeTag = App.UI.Repeater.styleElement(storeId, ".static_before", "li");
			_beforeTag += template_staticbefore+"</li>";
			oHtml = _beforeTag + oHtml;
		}

		if (template_staticafter != null) {
			oHtml += App.UI.Repeater.styleElement(storeId, ".static_after", "li");
			oHtml += template_staticafter+"</li>";
		}
				
		oHtml = oHtml.replace(/__percent__/gi,'%');
								
		if (!dataonly) {
			$('ul.list', target).html(oHtml);
		} else {
			$('ul.list li.item:not(.header)', target).remove();
			$('ul.list', target).append(oHtml);
		}
		
		var oData = { 'object': target, 'pageno': pageInfo.pageno, 'datachanged': (datachanged || (filter != null)) };
				
		$('*').triggerHandler('html-changed', target);
		$('*').triggerHandler('data-refresh', oData); // inform everyone that the grid dynamics just changed !!
		
	},

	
	__recoverFailed : function(datain, target) {
		/* data not received */
		$(target).attr('data-callinpro', false);
	}	
				
};

				
App.UI.SelectableUL = {

				hasInit : false,
				
				__preinit : function() {
				
					if (this.hasInit) return;
					this.hasInit = true;
					
					$('*').bind('page-refresh window-refresh', function(object, data) {
								App.UI.SelectableUL.refresh(data);
							});
				
				$(document).delegate('ul.selectable > li:not(.header):not(.unselectable):not(.bottom)', 'click', function(oEvent) {
							 App.UI.SelectableUL.itemClicked(oEvent);
						 });
				
				$(document).delegate('dl.selectable > dt:not(.header):not(.unselectable):not(.bottom)', 'click', function(oEvent) {
									 App.UI.SelectableUL.itemClicked(oEvent);
									 });
				
				},
				
				refresh : function(target) {
				
					if ((target=='undefined') || (target==null)) target = null;
					
					if ((target==null) || (typeof(target) == 'object')) {
						$('body').find('ul.selectable').each(function() {
																		App.UI.SelectableUL.setup(this);
																	});
						$('body').find('dl.selectable').each(function() {
																		 App.UI.SelectableUL.setup(this);
																	 });
					} else {
						$(target).find('ul.selectable').each(function() {
																		App.UI.SelectableUL.setup(this);
																	});
				
						$(target).find('dl.selectable').each(function() {
																		 App.UI.SelectableUL.setup(this);
														 });

					}

				},
				
				setup : function(target) {
				
					if (target == null) return;
				
				
				},
				
				itemClicked : function(event) {
				
					var target = event.currentTarget;
				
					if ($(target).hasClass('selected')) {
				
					} else {
						var parent = $(target).parent();
						$('> *.selected', parent).removeClass('selected');
						$(target).addClass('selected');
						$('> span > input:radio', target).prop('checked',true);
						var _parentComponent = $(parent).parent();
						var _currentid = $(target).attr("data-id");
						if (_currentid != null && _currentid != "undefined") {
							_parentComponent.attr("data-selected", _currentid);
						}
					}
				
					$('*').triggerHandler('tab-changed', target);
				
				}
				
};




				

$(document).ready(function() {
	
	App.UI.DataServices.__preinit();
	App.UI.Core.__preinit();
	App.UI.AutoWidth.__preinit();
				  
	App.UI.List.__preinit();
	App.UI.Repeater.__preinit();
	App.UI.SelectableUL.__preinit();
	App.UI.Pager.__preinit();
	App.UI.Filter.__preinit();
	App.UI.SortOn.__preinit();
	App.UI.Select.__preinit();
	App.UI.DataSelect.__preinit();
				  
	App.UI.SmartInput.__preinit();
	App.UI.UpdatingInput.__preinit();

	/* Now check if i need to see something... */

	App.UI.Core.refresh();
	App.UI.AutoWidth.refresh();

	App.UI.List.refresh();
	App.UI.Repeater.refresh();
	App.UI.SelectableUL.refresh();
	App.UI.Filter.refresh();
	App.UI.SortOn.refresh();
	App.UI.Select.refresh();
	App.UI.DataSelect.refresh();
				  
	App.UI.SmartInput.refresh();
	App.UI.UpdatingInput.__preinit();
	
});
