var r=255;var g=255;var b=100;var token=0;var seli=0;var activeteToall=0;var activeMovbar=0;var lazyLoad=1;var lazyLoadC=0;var lastBefore=0;var action=0;var internval=0;var updaters=new Array("t","p","g","l");var upchose=0;jQuery(document).ready(function(){jQuery("#topbr > textarea").bind("click",main.showSalt);jQuery("#topbr > textarea").bind("focus",main.showSalt);jQuery("#topbr > textarea").bind("keydown",main.movText);jQuery(".posts").click(main.hideSalt);jQuery("#movbar").click(main.activeMovbar);jQuery("#to_all").hover(main.toAllHover,main.toAllHover);jQuery("#to_all").click(main.toActive);jQuery("#tolid").click(main.toActive);jQuery("body").click(main.bodyHide);jQuery(".pname").hover(main.mini,main.minihide);jQuery(".pcmmd").click(main.addComment);jQuery(".plike").click(main.sendLike);jQuery(".plike_on").click(main.sendLikeOff);jQuery(".pshare").click(main.share);jQuery("#gomood").click(main.sendMood);jQuery(".moreComment").click(main.moreComment);jQuery(".fallow").click(main.fallow);jQuery(".unfallow").click(main.unfallow);jQuery("#pit").click(main.postit);jQuery(".postit > div > a").click(main.postiter);jQuery(".cpic").click(main.cpic);jQuery(".deletepostit").click(main.postitex);$(".postit").draggable();main.tox();jQuery("img").lazyload({placeholder:"/statics/images/grey.gif"});jQuery(window).scroll(function(){var f=jQuery(window).height();var d=jQuery(document).scroll().height();var a=d-f;var c=jQuery(window).scrollTop();if(a-50<c&&lazyLoadC<3&&lazyLoad==1){lazyLoadC++;lazyLoad=0;main.lazyLoad()}});interval=setInterval(main.update,10000)});var main={moreComment:function(){jQuery(this).parent().find(".comments").css("display","block");jQuery(this).remove()},rebindPosts:function(){jQuery(".pcmmd").unbind("click");jQuery(".pshare").unbind("click");jQuery(".pcmmd").click(main.addComment);jQuery(".pshare").click(main.share);jQuery(".moreComment").click(main.moreComment);main.rebindLike()},sendMood:function(){main.sendPost("/",jQuery("#topbr").serialize(true),function(){main.update()})},rebindLike:function(){jQuery(".plike").unbind("click");jQuery(".plike").click(main.sendLike);jQuery(".plike_on").unbind("click");jQuery(".plike_on").click(main.sendLikeOff)},lazyLoad:function(){var Last=jQuery(".post:last").attr("id");if(action==4){param="livelast="+Last}else{if(action==1){param="userlast="+Last+"&puser="+puser}else{if(action==0){param="userlast="+Last+"&self=1"}else{if(action==2){param="feed="+Last+"&feed="+feed_id}}}}param=param+"&nmode=live";main.sendPost("/",param,function(data){r=null;eval("r="+data);main.createNew(r,0)})},update:function(){e=new Date();t=e.getTime()/1000;csrfmiddlewaretoken=jQuery("#gotToken").find("input").val();upelement=updaters[upchose];var elm;elm=upelement+"="+timex+"&t_time="+t+"&csrfmiddlewaretoken="+csrfmiddlewaretoken;main.sendPost("/",elm,function(data){r=null;eval("r="+data);main.createNew(r.result,1);timex=r.time})},createNew:function(c,d){if(d==null){d=1}for(var a=0;a<c.length;a++){if(jQuery("#p_"+c[a]["id"]).length){elm=jQuery("#p_"+c[a]["id"]);jQuery("#p_"+c[a]["id"]).css("display","none");jQuery("#p_"+c[a]["id"]).remove()}html=jQuery("<div class='post' style='display:none;' id='p_"+c[a]["id"]+"'>"+c[a]["html"]+"</div>");if(d==1){jQuery(".posts").prepend(html)}if(d==0){jQuery(".posts").append(html)}jQuery("#p_"+c[a]["id"]).slideDown("slow")}lazyLoad=1;main.rebindPosts()},toListRemove:function(j){var f=jQuery("#to").val().split(",");var a=j;var d="";for(var c=0;c<f.length;c++){if(f[c]!=a){if(d!=""){d+=","}d+=f[c]}}jQuery("#to").val(d)},toListCheck:function(j){var f=jQuery("#to").val().split(",");var a=j;var d="";no_add=false;for(var c=0;c<f.length;c++){if(f[c]==a){no_add=true}}return no_add},toListAdd:function(a){if(!main.toListCheck(a)){tmp=jQuery("#to").val();if(tmp!=""){tmp+=","}tmp+=a;jQuery("#to").val(tmp)}},tox:function(){jQuery("#tox > a > span").unbind("click");jQuery("#tox > a > span").click(function(){id=jQuery(this).parent().attr("rel");main.toListRemove(id);jQuery(this).parent().hide("slow",function(){jQuery(this).remove();jQuery("#getu").focus()})})},toList:function(data){var d=data;eval(" d="+data+";");count=0;jQuery("#tolist").html("");for(var i=0;i<d.length;i++){if(!main.toListCheck(d[i]["id"])){sel="";count++;if(count==1){sel=" class='selected' "}if(jQuery("#tolist").html().indexOf('rel="'+d[i]["id"]+'"')==-1){jQuery("#tolist").append("<a"+sel+' href="#" rel="'+d[i]["id"]+'">'+d[i]["name"]+"</a>")}}}seli=0;var pos=jQuery("#topbr > textarea").position();jQuery("#tolist").css({top:pos.top+25,left:pos.left});if(jQuery("#tolist").css("display")=="none"&&count>0){jQuery("#tolist").slideDown()}jQuery("#tolist > a").click(function(){to=jQuery(this).attr("rel");name=jQuery(this).text();if(jQuery("#topbr > textarea").val().indexOf("@"+name+" ")==-1){r=jQuery("#topbr > textarea").val().split("@");r=r[r.length-1];val=jQuery("#topbr > textarea").val().replace("@"+r,"@"+name);jQuery("#topbr > textarea").val(val);jQuery("#tolist").slideUp();jQuery("#topbr > textarea").focus()}})},fallow:function(){var a=jQuery(this);main.sendPost("/","fallow="+jQuery(this).attr("rel"),function(){a.removeClass("fallow").addClass("unfallow");a.find("span").html("Unfallow");a.unbind("click");a.bind("click",main.unfallow)})},postit:function(){jQuery(".postit").show("slow")},minihide:function(){var a=jQuery(this);jQuery("#minii").remove()},mini:function(){},postiter:function(){text=jQuery(this).parent().find("textarea").val();jQuery(this).css({background:"url(/statics/images/load-anim-16.gif) no-repeat","text-indent":"22px",display:"block"});jQuery(this).attr("disabled","disabled");pos=jQuery(".postit").position();main.sendPost("/","postit="+text+"&coord="+pos.left+","+pos.top,function(){});jQuery(".postit").hide("slow")},postitex:function(){text=jQuery(this).attr("href").replace("#","");par=jQuery(this).parent().parent();main.sendPost("/","postitdel="+text,function(){});par.hide("slow");par.remove()},unfallow:function(){var a=jQuery(this);main.sendPost("/","fallow="+jQuery(this).attr("rel"),function(){a.removeClass("unfallow").addClass("fallow").find("span").html("Fallow");a.unbind("click");a.bind("click",main.fallow)})},movText:function(d){if(d.keyCode==81){jQuery(this).bind("keyup",main.getuser)}var a=new Array();code=d;var c=new Array();jQuery("#tolist > a").each(function(){a.push(jQuery(this))});if(d.keyCode==32){jQuery(this).unbind("keyup")}if(a.length>0){if(code.keyCode==40){seli++;if(a.length>seli){a[seli-1].removeClass("selected");a[seli].addClass("selected")}else{if(a.length==seli){a[seli-1].removeClass("selected");a[0].addClass("selected");seli=0}}jQuery(this).focus();return false}else{if(code.keyCode==13){jQuery(this).unbind("keyup");to=a[seli].attr("rel");name=a[seli].text();if(!main.toListCheck(to)){main.toListAdd(to);r=jQuery("#topbr > textarea").val().split("@");r=r[r.length-1];val=jQuery("#topbr > textarea").val().replace("@"+r,"@"+name);jQuery("#topbr > textarea").val(val+" ");jQuery("#tolist").slideUp();jQuery("#topbr > textarea").focus();main.tox()}jQuery(this).focus();return false}else{if(code.keyCode==38){if(seli-1>=0){a[seli].removeClass("selected");a[seli-1].addClass("selected");seli--}else{a[0].removeClass("selected");a[a.length-1].addClass("selected");seli=a.length-1}jQuery(this).focus();return false}}}}jQuery(this).css("overflow","hidden");t=jQuery(this).scrollTop();if(jQuery(this).scrollTop()>0){t=jQuery(this).scrollTop()+20}h=(t)+jQuery(this).height();if(h>100){jQuery(this).css("overflow","visible")}else{jQuery(this).css({height:h})}},cpic:function(){csrfmiddlewaretoken=jQuery("#gotToken").find("input").val();main.modal("Change Picture",'<form method="post" action="" id="gopost" enctype="multipart/form-data"><input type="hidden" name="csrfmiddlewaretoken" value="'+csrfmiddlewaretoken+'" /><input type="file" name="file" id="file" /></form>',1,function(){jQuery("#gopost").submit()})},share:function(){val=jQuery(this).attr("rel").split(";");main.modal("PaylaÅŸ",'<p style="text-align:left;"><label>KÄ±sa URL:<br /><input type="text" value="http://frmm.me'+val[0]+'" /><br /></label><label>URL:<br /><input type="text" value="http://www.frimemind.com'+val[1]+'" /></label></p>')},sendLike:function(){jQuery(this).css("background","url(/statics/images/load-anim-16.gif) no-repeat");main.sendPost("/","like="+jQuery(this).parent().parent().parent().attr("id"),function(){main.update();jQuery(this).removeClass("plike").addClass("plike_on")})},sendLikeOff:function(){jQuery(this).css("background","url(/statics/images/load-anim-16.gif) no-repeat");t=jQuery(this);main.sendPost("/","unlike="+jQuery(this).parent().parent().parent().attr("id"),function(){t.css("background","");t.removeClass("plike_on").addClass("plike");t.text("BeÄŸen");main.rebindLike()})},sendKeyList:function(a){},getuser:function(a){if(a.keyCode==38||a.keyCode==40||a.keyCode==13){main.sendKeyList(a.keyCode);return}var c=jQuery(this).val().split("@")[jQuery(this).val().split("@").length-1].split(" ")[0];if(c.length>0&&c!=" "){main.sendPost("/","getU="+c,main.toList)}},bodyHide:function(a){var c=jQuery("#body").position();if(a.pageX<c.left||a.pageX>c.left+jQuery("#body").width()||a.pageY<c.top){main.hideSalt()}},sendPost:function(a,j,i){var d="";var c=null;if(j!=null){d=j}if(i!=null){c=i}jQuery.ajax({type:"POST",url:a,dataType:"html",data:d,success:c,error:function(l,f,k){main.ajaxError()}})},ajaxError:function(){main.modal("Hata!","Sunucu beklenmeyen bir hata oluşturdu. Lütfen tekrar deneyiniz.")},toActive:function(){jQuery("#tos").css("border","1px inset #ccc");jQuery("#tos > input").focus();jQuery("#tolid").css("display","none");activeteToall=1},toAllHover:function(){if(activeteToall==0){if(jQuery("#tolid").css("display")=="none"){var a=jQuery("#tos > input").position();jQuery("#tolid").css({top:a.top,left:a.left,display:"block"})}else{jQuery("#tolid").css("display","none")}}},modal:function(j,c,a,d){$("#dialog-message").attr("title",j);$("#dialog-message").html(c);if(a==null){$("#dialog-message").dialog({modal:true,buttons:{Ok:function(){$(this).dialog("close")}}})}else{$("#dialog-message").dialog({modal:true,buttons:{Ok:d}})}},addComment:function(){var a=jQuery(this).parent().parent().parent().attr("id");jQuery(".cigo").find("textarea").slideUp(500,function(){jQuery(this).parent().find("button").hide("slow",function(){jQuery(this).remove()});jQuery(this).remove()});if(jQuery("#"+a).find("button").text()==""){jQuery("#"+a).find(".cigo").css("display","none");jQuery("#"+a).find(".cigo").append(jQuery('<textarea id="cmd"></textarea><button class="btn">Deneme</button>'));jQuery("#"+a).find(".cigo").slideDown(500);jQuery("#"+a).find(".cigo").find("button").click(function(){text=jQuery(this).parent().find("textarea").val();id=jQuery(this).parent().parent().parent().attr("id");jQuery(this).attr("disabled","disabled");jQuery(this).parent().find("textarea").attr("disabled","disabled");main.sendPost("/","reply="+id+"&text="+text,function(){main.update()})})}},activeMovbar:function(){if(activeMovbar==0){jQuery("#usemood").val("1");jQuery(this).css("background-color","#ffff00");activeMovbar=1;jQuery(this).append(jQuery("<div id='slider'></div>"));$("#slider").slider({value:5,min:0,max:10,step:0.1,slide:function(c,d){$("#mood").val(parseFloat(d.value));$("#inslider").text(parseFloat(d.value));if(d.value<5){var a=5/100;var f=d.value/a;g=parseInt((200/100)*f)}if(d.value>5){var a=5/100;var f=(d.value-5)/a;r=200-parseInt((200/100)*f);if(d.value>7){b=200-r;r=120;g=0}}if(d.value==5){r=200;g=200}jQuery("#movbar").css("background-color","rgb("+r+","+g+","+b+")")}});jQuery(".ui-slider-handle").append(jQuery("<div id='inslider'>5.0</div>"))}},showSalt:function(){activeteToall=0;jQuery("#tos").css("border","none");if(jQuery("#movbar").css("display")=="none"){jQuery("#movbar").slideDown("slow")}if(jQuery("#to_all").css("display")=="none"){jQuery("#to_all").slideDown("slow")}if(jQuery(this).height()<50){jQuery(this).animate({height:"50px"},1000)}jQuery("#to_all").unbind("hover");jQuery("#to_all").hover(main.toAllHover,main.toAllHover);activeMovbar=0},hideSalt:function(){jQuery("#slider").remove();if(jQuery("#movbar").css("display")!="none"){jQuery("#movbar").hide("slow");jQuery("#to_all").hide("slow");jQuery("#movbar").css("background-color","#ccc");activeMovbar=0;jQuery("#usemood").val("0")}if(jQuery("#topbr > textarea").height()>45){jQuery("#topbr > textarea").animate({height:"22px"},1000)}}};