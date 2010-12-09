var r = 255;
var g = 255;
var b = 100;
var token = 0;
var seli = 0;
var activeteToall = 0;
var activeMovbar=0;
jQuery(document).ready(function() {
	jQuery("#topbr > textarea").bind("click",main.showSalt);
	jQuery("#topbr > textarea").bind("focus",main.showSalt);
	jQuery("#topbr > textarea").bind("keyup",main.movText);
	jQuery("#topbr > textarea").bind("keypress",main.movText);
	jQuery("#topbr > textarea").bind("keydown",main.movText);
	jQuery(".posts").click(main.hideSalt);
	jQuery("#movbar").click(main.activeMovbar);
	jQuery("#to_all").hover(main.toAllHover,main.toAllHover);
	jQuery("#to_all").click(main.toActive);
	jQuery("#tolid").click(main.toActive);
	jQuery("body").click(main.bodyHide);
	jQuery(".pcmmd").click(main.addComment);
	jQuery(".plike").click(main.sendLike);
	jQuery(".pshare").click(main.share);
	jQuery("#gomood").click(main.sendMood);
        jQuery("#getu").bind("keyup",main.getuser);
        main.tox();
        jQuery("img").lazyload({
             placeholder : "/statics/images/grey.gif"
         });
});

var main = {
        sendMood:function() {
          main.sendPost("/",jQuery("#topbr").serialize(true));
        },
	rebindLike:function() {
		jQuery(".plike").unbind("click");
		jQuery(".plike").click(main.sendLike);
		jQuery(".plike_on").unbind("click");
		jQuery(".plike_on").click(main.sendLikeOff);
	},

        toListRemove:function(id) {
            var all = jQuery("#to").val().split(",");
            var st = id;
            var tmp = "";
            for(var i=0;i<all.length;i++) {
                if(all[i] != st) {
                    if (tmp != "") tmp +=",";
                    tmp += all[i];
                }

            }
            jQuery("#to").val(tmp);
        },
        toListCheck:function(to) {
            var all = jQuery("#to").val().split(",");
            var st = to;
            var tmp = "";
            no_add = false;
            for(var i=0;i<all.length;i++) {
                if(all[i] == st) {
                   
                    no_add = true;
                }

            }
            return no_add;
        },
        toListAdd:function(to) {
            if(!main.toListCheck(to)) {
                tmp = jQuery("#to").val();
                if(tmp != "") tmp +=",";
                tmp += to;
                jQuery("#to").val(tmp);
            }
        },
        tox:function() {
            jQuery("#tox > a > span").unbind("click");
            jQuery("#tox > a > span").click(function() {
                id = jQuery(this).parent().attr("rel");
                main.toListRemove(id);
                jQuery(this).parent().hide("slow",function() {
                    jQuery(this).remove();
                    jQuery("#getu").focus();
                });
            });

        }
        ,
        toList:function(data) {
            var d;
            jQuery("#tolist > a").unbind("click");
            jQuery("#tolist").html("");
            eval("d="+data);
            count = 0;
            for(var i=0;i<d.length;i++) {
                if(!main.toListCheck(d[i]['id'])) {
                    sel = "";
                     if(count==0)sel=" class='selected' "
                     jQuery("#tolist").append('<a'+sel+' href="#" rel="'+d[i]['id']+'">'+d[i]['name']+'</a>');
                     count++;
                }
            }
            seli = 0;
            var pos = jQuery("#getu").position();

            jQuery("#tolist").css({top:pos.top+25,left:pos.left});
             if(jQuery("#tolist").css("display") == "none" && count > 0) jQuery("#tolist").slideDown();
             jQuery("#tolist > a").click(function(){
                 to = jQuery(this).attr("rel");
                 name = jQuery(this).text();
                 if(!main.toListCheck(to)) {
                  main.toListAdd(to);
                  jQuery("#tox").append('<a rel="'+to+'" style="margin-left:3px;">'+name+'<span>x</span></a>');
                  jQuery("#tolist").slideUp();
                  jQuery("#getu").val("");
                   jQuery("#getu").focus();
                  main.tox();
                 }
             });
            
        },
	movText:function() {
		jQuery(this).css("overflow","hidden");
		t= jQuery(this).scrollTop();
		if(jQuery(this).scrollTop() > 0) {
			t = jQuery(this).scrollTop()+20;
		}
		h = (t)+jQuery(this).height();
		if(h > 100) {
			jQuery(this).css("overflow","visible");
		} else {
			jQuery(this).css({height:h});
		}
	},

	share:function() {
		val = jQuery(this).attr("rel").split(";")
		main.modal("Paylaş",'<p style="text-align:left;"><label>Kısa URL:<br /><input type="text" value="'+val[0]+'" /><br /></label><label>URL:<br /><input type="text" value="'+val[1]+'" /></label></p>');
	},

	sendLike:function() {
		jQuery(this).removeClass("plike").addClass("plike_on");
		jQuery(this).text("Beğeniyi kaldır");
		main.rebindLike();
                main.sendPost("/root");
	},
	sendLikeOff:function() {

		jQuery(this).removeClass("plike_on").addClass("plike");
		jQuery(this).text("Beğen");
		main.rebindLike();

	},

        sendKeyList:function(code) {


           var liste = new Array();
           
           jQuery("#tolist > a").each(function() {

               liste.push(jQuery(this));
           });
           if(liste.length > 0) {
               if(code == 40) {
                   seli++;
                   if(liste.length > seli) {
                       liste[seli-1].removeClass("selected");
                       liste[seli].addClass("selected");
                   } else if(liste.length == seli) {
                       liste[seli-1].removeClass("selected");
                       liste[0].addClass("selected");
                       seli = 0;
                   }
               }else if(code == 13) {
                   to = liste[seli].attr("rel");
                   name=liste[seli].text();
                   if(!main.toListCheck(to)) {
                      main.toListAdd(to);
                      jQuery("#tox").append('<a rel="'+to+'" style="margin-left:3px;">'+name+'<span>x</span></a>');
                      jQuery("#tolist").slideUp();
                      jQuery("#getu").val("");
                       jQuery("#getu").focus();
                      main.tox();
                     }
               }else if(code == 38) {
                   
                   if(seli - 1 >= 0) {
                       liste[seli].removeClass("selected");
                       liste[seli - 1].addClass("selected");
                       seli--;
                   } else {
                       liste[0].removeClass("selected");
                       liste[liste.length - 1].addClass("selected");
                       seli=liste.length - 1;
                   }
               }
           }
        },

        getuser:function(e) {
            if(e.keyCode == 38 || e.keyCode == 40 || e.keyCode == 13) {
                main.sendKeyList(e.keyCode);
                return;
            }
            var val=jQuery("#getu").val();
            main.sendPost("/","getU="+val,main.toList);
        }
        ,

	bodyHide:function(e) {

		var pos = jQuery("#body").position();
		if(e.pageX < pos.left || e.pageX > pos.left + jQuery("#body").width() || e.pageY < pos.top) {
			main.hideSalt();

		}
	}
	,
	sendPost:function(url,param,fu) {
		var p = "";
		var f = null;
                //alert(param);
		if(param != null)p = param;
                
                
		if(fu != null) f = fu;
		jQuery.ajax({
                type: "POST",
                url: url,
                dataType:"html",
                data:p,
                success:f,
                error:function (xhr, ajaxOptions, thrownError){
                    main.ajaxError();
                }
            });
	},
	ajaxError:function() {
		main.modal("Hata!","Sunucu beklenmeyen bir hata olu�turdu. L�tfen tekrar deneyiniz.")
	},
	toActive:function() {
		jQuery("#tos").css("border","1px inset #ccc");
		jQuery("#tos > input").focus();
		jQuery("#tolid").css("display","none");
		activeteToall = 1;
	},
	toAllHover:function() {
		if(activeteToall == 0) {
			if(jQuery("#tolid").css("display") == "none") {

				var pos = jQuery("#tos > input").position();
				jQuery("#tolid").css({top:pos.top,left:pos.left,display:'block'});

			} else {
				jQuery("#tolid").css("display","none");
			}
		}
	},

	modal:function(title,message) {
	$( "#dialog-message" ).attr("title",title);
	$( "#dialog-message" ).html(message);

	$( "#dialog-message" ).dialog({
			modal: true,
			buttons: {
				Ok: function() {
					$( this ).dialog( "close" );
				}
			}
		});


	},

	
	addComment:function() {
		var parent = jQuery(this).parent().parent().parent().attr("id");
		jQuery(".cigo").find("textarea").slideUp(500,function() {
			jQuery(this).parent().find("button").hide("slow",function() {jQuery(this).remove()});
			jQuery(this).remove();

		});
		if(jQuery('#'+parent).find("button").text() == '') {
			jQuery("#"+parent).find(".cigo").css("display","none");
			jQuery("#"+parent).find(".cigo").append(jQuery('<textarea id="cmd"></textarea><button class="btn">Deneme</button>'));
			jQuery("#"+parent).find(".cigo").slideDown(500);
                        jQuery("#"+parent).find(".cigo").find("button").click(function() {
                            text = jQuery(this).parent().find("textarea").val();
                            id = jQuery(this).parent().parent().parent().attr("id");
                            main.sendPost("/","reply="+id+"&text="+text);
                        });
		}
	},
	activeMovbar:function() {
		if(activeMovbar == 0) {
			jQuery(this).css("background-color","#ffff00");
			activeMovbar = 1;
			jQuery(this).append(jQuery("<div id='slider'></div>"));
			$( "#slider" ).slider({
				value:5.0,
				min: 0.0,
				max: 10.0,
				step: 0.1,
				slide: function( event, ui ) {
				$( "#mood" ).val( parseFloat(ui.value) );
				$( "#inslider" ).text( parseFloat(ui.value) );

				if(ui.value < 5) {
					var u = 5/100;
					var p = ui.value / u;
					g = parseInt((200/100) * p);
				}

				if(ui.value > 5) {
					var u = 5/100;
					var p = (ui.value - 5) / u;
					r = 200 - parseInt((200/100) * p);
					if(ui.value > 7) {
						b = 200 - r;
						r = 120;
						g =0;
					}

				}
				if(ui.value == 5) {
					r = 200;
					g =200;
				}
				jQuery("#movbar").css("background-color","rgb("+r+","+g+","+b+")")
			}
			});
			jQuery(".ui-slider-handle").append(jQuery("<div id='inslider'>5.0</div>"));
		}
	},

	showSalt:function() {
		activeteToall = 0;
		jQuery("#tos").css("border","none");
		if(jQuery("#movbar").css("display") == "none") jQuery("#movbar").slideDown("slow");
		if(jQuery("#to_all").css("display") == "none") jQuery("#to_all").slideDown("slow");
		if(jQuery(this).height() < 50) jQuery(this).animate({height:"50px"},1000);
		jQuery("#to_all").unbind("hover");
		jQuery("#to_all").hover(main.toAllHover,main.toAllHover);
		activeMovbar = 0;

	},
	hideSalt:function() {
		jQuery("#slider").remove();
		if(jQuery("#movbar").css("display") != "none") {
			jQuery("#movbar").hide("slow");
			jQuery("#to_all").hide("slow");
			jQuery("#movbar").css("background-color","#ccc");
			activeMovbar = 0;
		}
		if(jQuery("#topbr > textarea").height() > 45) jQuery("#topbr > textarea").animate({height:"22px"},1000);
	}
}




/* var timex;
var updaters = new Array("t","p","g","l");
var upchose = 0;
var updateStart = 1;
var r = 255;
var g = 255;
var b = 0;
jQuery(document).ready(function() {
    main.fbinit();
	$( "#slider" ).slider({
		value:5.0,
		min: 0.0,
		max: 10.0,
		step: 0.1,
		slide: function( event, ui ) {
			$( "#mood" ).val( parseFloat(ui.value) );
			$( "#inslider" ).text( parseFloat(ui.value) );
			
			if(ui.value < 5) {
				var u = 5/100;
				var p = ui.value / u;
				g = parseInt((255/100) * p);
			}
			
			if(ui.value > 5) {
				var u = 5/100;
				var p = (ui.value - 5) / u;
				r = 255 - parseInt((255/100) * p);
			}
			if(ui.value == 5) {
				r = 255;
				g = 255;
			}
			jQuery("#slider_top").css("background-color","rgb("+r+","+g+","+b+")")
		}
	});
	var d = new Date();
	var hash=jQuery("#hash").val()+d.getTime();
	jQuery("#hash").val(hash);
	var csrfmiddlewaretoken = jQuery("#gotToken").find("input").val();

	$('#file_upload').uploadify({
	    'uploader'  : '/statics/swf/uploadify.swf',
		'script'    : '/upload',
	    'width'		: "87px",
	    'height'	: "20px",
	    "method"	: "get",
		'scriptData': {"hash":hash,"csrfmiddlewaretoken":csrfmiddlewaretoken},
	    'buttonImg'	: '/statics/images/file_up.png',
	    //'cancelImg' : '/uploadify/cancel.png',
	    'auto'      : true,
	    'onOpen'      : function(event,ID,fileObj) {
	        $('#file_t').text(fileObj.name);
	        $('.perc').width("1%");
                $('.uploadifyQueue').css("display","none");
	        $("#uploadprogress").show();
	      },
	      'onComplete' : function(event, ID, fileObj, response, data) {
	    	  //alert(fileObj.type);
	    	  if (fileObj.type==".jpg" || fileObj.type==".png" || fileObj.type==".gif" || fileObj.type==".bmp") {
	    		  var o = fileObj;
	    		  jQuery("#files").append(jQuery("<a href='' class='file_"+fileObj.type.replace(".","")+"'><img src='/statics/users/"+fileObj.name+"' width='120'/></a>"));
	    		  $("#uploadprogress").hide();
	    		  
	    	  } else if(fileObj.type==".mp3" || fileObj.type==".pdf"  || fileObj.type==".doc" || fileObj.type=="docx" || fileObj.type=="pdf" || fileObj.type=="xls" || fileObj.type=="xlsx" || fileObj.type=="pps" || fileObj.type=="ppsx" || fileObj.type=="swf"  || fileObj.type==".mov" || fileObj.type==".avi" || fileObj.type==".mp4"){
	    		  jQuery("#files").append(jQuery("<a href='' class='file_"+fileObj.type.replace(".","")+"'>"+fileObj.name+"</a>"));
	    		  $("#uploadprogress").hide();
	    	  } else {
	    		  $("#uploadprogress").hide();
	    	  }
	    	
	    	
	      }
	      ,
	      
	      'onProgress'  : function(event,ID,fileObj,data) {
	          
	          $('.perc').width(data.percentage+"%");
	          return false;
	        }
	  });
	$('#file_upload2').uploadify({
		'uploader'  : '/statics/swf/uploadify.swf',
		'script'    : '/upload?hash='+hash+"&csrfmiddlewaretoken="+csrfmiddlewaretoken,
		'width'		: "87px",
		'height'	: "20px",
		'buttonImg'	: '/statics/images/file_up2.png',
		"fileExt"	:'*.mp3;*.avi;*.mp4;*.m4a;*.3gp;*.flv',
		"fileDesc"	: "Dosya",
		//'cancelImg' : '/uploadify/cancel.png',
		'auto'      : true,
		'onError'     : function (event,ID,fileObj,errorObj) {
		      alert(errorObj.type + ' Error: ' + errorObj.info);
		    }
	});
	jQuery("#totext").bind("keyup",function() {
		
		if(jQuery("#totext").val().length > 0) {
			var pos = jQuery("#totext").position();
			csrfmiddlewaretoken = jQuery("#gotToken").find("input").val();
			jQuery.post("/",{'getU':jQuery("#totext").val(),"csrfmiddlewaretoken":csrfmiddlewaretoken},function(data){
				jQuery("#listto").css({top:pos.top+22,left:pos.left});
				
				var all;
				eval("all="+data+";")
                                main.hadlex();

				all = main.compareUser(all,"id");
				
				//alert(all);
				for(var i=0;i<all.length;i++) {
					jQuery("#listto").html(" ");
					obj = jQuery('<a href="javascript:;"></a>');
					
					obj.click(function() {
						allx = new Array();
						eval("allx="+jQuery("#tousers").val()+";");
						id = jQuery(this).find("span").attr("rel");
						text = jQuery(this).find("span").text();
						ek = 0;
						for(var i=0;i<allx.length;i++) {
							if (allx[i] == id) ek = 1; 
						}
						
						
						if(ek==0)allx.push(jQuery(this).find("span").attr("rel"));
						tmp = "";
						for(var i=0;i<allx.length;i++) {
							if (tmp!='') tmp +=",";
							tmp += "'"+allx[i]+"'";
						}
						tmp = "["+tmp+"]";
						jQuery("#tousers").val(tmp);
						jQuery(this).remove();
						jQuery(".sender").append(jQuery('<a href="javascript:;">'+text+' <span rel="'+id+'">x</span></a>'))
						main.sederEvent();
						jQuery("#listto").hide("slow");
						jQuery("#totext").val("");
					});
					obj.append(jQuery('<span rel="'+all[i]['id']+'">'+all[i]['name']+'</span>'))
					jQuery("#listto").html(obj);
				}
				
				if(jQuery("#listto").css("display") == "none" && all.length > 0) jQuery("#listto").show("slow");
				if(jQuery("#listto").css("display") != "none" && all.length == 0)jQuery("#listto").hide("slow");
			});
			//alert(jQuery("#listto").css("display"));
			
		} else {
			jQuery("#listto").hide("slow");
		}
		//alert(jQuery("#listto").css("display"));
	});
	
	
	main.sederEvent();
	jQuery("#slider_top").css("background-color","rgb("+r+","+g+","+b+")")

	jQuery(".ui-slider-handle").append(jQuery("<div id='inslider'>5.0</div>"));
	
	jQuery("#postform").bind("submit",function() {
            if( jQuery("#msg").val().length < 2) {
                alert("birseyler yazmalisin");
                return false;
            }
            d = jQuery("#postform").serialize(true) ;
            jQuery("#postform").find("button").attr("disabled","disabled");
            jQuery("#postform").find("textarea").val("");
            //button
            d += "&token="+token;
		jQuery.post("/",d,function(data) {
                       var e;
                       jQuery("#postform").find("button").attr("disabled","");
                        eval("e="+data+";");
                        //token = e['token'];
                        main.hadlex();
                        if(e['response'] == "err") alert('Sistem hatasi');
			main.Update();
			
		});	
		return false;
	});
	$( "#mood" ).val($( "#slider" ).slider( "value" ) );
	main.bind();
        
	if (updateStart)main.UpdateTimer();
});
var wait_update = 0;
var animate_scroll = 0;
main = {

                
                handleSessionResponse:function(response) {
                     // if we dont have a session, just hide the user info
                    if (!response.session) {
                      clearDisplay();
                      return;
                    }

                    // if we have a session, query for the user's profile picture and name
                    if (response.perms) {
                        var perms;
                        eval("perms = "+response.perms);
                        perms_req = "read_stream,email,publish_stream,offline_access,photo_upload,video_upload".split(",");
                        
                        nonex = 0
                        allperms = perms['extended']+perms['user'];
                       
                        for(i=0;i<perms_req.length;i++) {
                            if (allperms.indexOf(perms_req[i]) == -1) {
                               alert(perms_req[i]);
                               nonex = 1
                            }
                        }
                        
                       
                        if (nonex == 1) {
                            FB.login(main.handleSessionResponse,{perms:'read_stream,user_birthday,email,publish_stream,offline_access,photo_upload,video_upload'});
                            return;
                        }
                        
                       if(!loggedUSER)document.location = '/loginfacebook';
                    } else {
                        FB.login(main.handleSessionResponse,{perms:'read_stream,user_birthday,email,publish_stream,offline_access,photo_upload,video_upload'});
                        return;
                    }
                },
                fbinit:function() {
                  $('#login_fb').bind('click', function() {
                    FB.login(main.handleSessionResponse,{perms:'read_stream,user_birthday,email,publish_stream,offline_access,photo_upload,video_upload'});
                   });
                  FB.init({apiKey: '535c96a06491b8e94bd16eafc32cf3b2' ,
                     status : true, // check login status
                     cookie : true, // enable cookies to allow the server to access the session
                     xfbml  : true  // parse XFBML
                     //
                     });

                    // fetch the status on load
                   FB.getLoginStatus(main.handleSessionResponse);
                },


		hadlex:function() {
                  token = main.readCookie('token');
                  main.eraseCookie('token');
                },

                createCookie:function (name,value,days) {
                        if (days) {
                                var date = new Date();
                                date.setTime(date.getTime()+(days*24*60*60*1000));
                                var expires = "; expires="+date.toGMTString();
                        }
                        else var expires = "";
                        document.cookie = name+"="+value+expires+"; path=/";
                },

                readCookie:function (name) {
                        var nameEQ = name + "=";
                        var ca = document.cookie.split(';');
                        for(var i=0;i < ca.length;i++) {
                                var c = ca[i];
                                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
                        }
                        return null;
                },

                eraseCookie:function (name) {
                        main.createCookie(name,"",-1);
                },


		sederEvent:function(){
	
			jQuery(".sender > a").unbind("click");
			jQuery(".sender > a").click(function() {
				all = new Array();
				eval("all="+jQuery("#tousers").val()+";");
				
				id = jQuery(this).find("span").attr("rel");
				tmp = "";
				for(var i=0;i<all.length;i++) {
					if (tmp!='') tmp +=",";
					if(id != all[i]) tmp += "'"+all[i]+"'";
				}
				tmp = "["+tmp+"]";
				jQuery("#tousers").val(tmp);
				jQuery(this).remove();
				
				
			});
	
		},
		postloader:function(url,postdata,endfunc) {
                    jQuery.post(url,postdata,function(data) {
                        csrfmiddlewaretoken = data['csrfmiddlewaretoken'];
                        data2 = data;
                        eval('endfunc('+data2+');');
                    });
                },
		isHave:function(elm) {
			if(jQuery(elm).html() != null) return true;
			return false;
		},
		UpdateTimer:function() {
			main.Update();
			setTimeout("main.UpdateTimer();",5000);
		}
		,
		compareUser:function(arr,key) {
			all = new Array();
			eval("all="+jQuery("#tousers").val()+";");
			tmp = new Array();
			
			for(var k=0;k<arr.length;k++) {
				var b =0;
				for(var i=0;i<all.length;i++) {
				
					elm = arr[k];
					if(key != '') elm = elm[key];
					
					if(all[i] == elm) b = 1;
				}
				if (b==0) tmp.push(arr[k]);
			}
			return tmp;
		}
		,
                maketoken:function() {

                },
		Update:function() {
			e = new Date();
			t = e.getTime() / 1000;
			csrfmiddlewaretoken = jQuery("#gotToken").find("input").val();
			upelement = updaters[upchose];
			var elm;
			eval("elm = {'token':'"+token+"','"+upelement+"':'"+timex+"',\"t_time\":'"+t+"',\"csrfmiddlewaretoken\":'"+csrfmiddlewaretoken+"'};");
		//	alert(elm);

			jQuery.post("/",elm,function(data) {
				var d = null;
				eval("d ="+data);

                                main.hadlex();
				//alert(d);
				//alert(d['time']);
				
				if (d['result'] != null && d['result'] != "err") {
					if (d['result'].length > 0) {
						timex = d['time'];
						//alert(d['result'].length );
						for(var i=0;i<d['result'].length;i++) {
							//alert(d['result'][i]['id']);
							if(main.isHave("#"+d['result'][i]['id'])) {
								main.upgrade(d['result'][i]['html'],d['result'][i]);
							} else {
								main.create(d['result'][i]);
							}
						}
					}
				} else if (d['result'] == "err") {
                                    alert("Sistem Hatasi");
                                }
			});
			
		},
		upgrade:function(html,data) {
			datax = jQuery("#"+data['id']);
			datax.html(html);
			jQuery("#"+data['id']).hide("slow",function() {
				jQuery(this).remove();
				datax.css("visiblity","hidden");
				datax.append('<br class="clr" />');
				jQuery("#allpost").prepend(datax);
				jQuery("#"+data['id']).show("slow");
				main.bind();
				if (animate_scroll) {
					$('html, body').animate({
						scrollTop: $("#"+data['id']).offset().top
						}, 2000);
					animate_scroll = 0;
				}
			});
			
		},
		bind:function() {
			jQuery(".commentSend").unbind("click");
			jQuery(".discomment").unbind("click");
			jQuery(".like").unbind("click");
			jQuery(".commentSend").click(function(){
				//alert(jQuery(this).parent().find(".send").html());
				if(jQuery(this).parent().find(".send").html() == null) {
					jQuery(this).parent().append(jQuery('<div class="send" style="display:none;"><textarea rows="" cols=""></textarea><button class="rtl">Send</button></div>'));
					jQuery(this).parent().find(".send").find("button").click(function() {
						id = jQuery(this).parent().parent().parent().parent().attr("id");
						csrfmiddlewaretoken = jQuery("#gotToken").find("input").val();
						parent = jQuery(this).parent()
						text = jQuery(this).parent().find("textarea").val()
						jQuery.post("/",{"token":token,"reply":id,"text":text,"csrfmiddlewaretoken":csrfmiddlewaretoken},function(data) {
							//alert(data);
                                                        eval("all="+data+";")
                                                        main.hadlex();
							parent.remove();
							animate_scroll = 1;
							main.Update();
						});
					});
					jQuery(this).parent().find(".send").show("slow");
				}
			});
			
			jQuery(".discomment").click(function() {
				id = jQuery(this).parent().attr("id");
				pr =  jQuery(this).parent();
				csrfmiddlewaretoken = jQuery("#gotToken").find("input").val();
				jQuery.post("/",{'csrfmiddlewaretoken':csrfmiddlewaretoken,'comment':id}, function(data) {
					
                                        eval("all="+data+";")
                                        //token = all['token'];
                                        main.hadlex();
                                        if (all['response'] =="ok") {
						pr.hide("slow",function() {jQuery(this).remove();});
						alert("Yorumun Silindi");
						main.Update();
						$('html, body').animate({
							scrollTop: $("#"+id).offset().top
							}, 2000);
					} else {
						alert("Beklenmedik Bir Hata OluÅŸtu");
					}
				});
			});
			
			jQuery(".like").click(function() {
				
				
				id = jQuery(this).parent().parent().attr("id");
				csrfmiddlewaretoken = jQuery("#gotToken").find("input").val();
				parent = jQuery(this).parent();
				jQuery.post("/",{"like":id,"csrfmiddlewaretoken":csrfmiddlewaretoken},function(data) {
					
                                        eval("all="+data+";")
                                        //token = all['token'];
                                        main.hadlex();
                                        if (all['response'] == "err") {
						alert("Daha Ã¶nce beyenmiÅŸsin.");
					} else {
						parent.find(".like").remove();
						animate_scroll = 1;
						main.Update();
						
					}
				});
			});
		},
		create:function(html) {
			ht = jQuery('<div id="'+html['id']+'" class="post" style="display:none;">'+html['html']+'</div><br class="clr" />');
			jQuery("#allpost").prepend(ht);
			jQuery("#"+html['id']).fadeIn("slow");
			main.bind();
			if (animate_scroll) {
				$('html, body').animate({
					scrollTop: $("#"+html['id']).offset().top
					}, 2000);
				animate_scroll = 0;
			}
		}
}
*/