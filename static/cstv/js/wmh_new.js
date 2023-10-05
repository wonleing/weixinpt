// JavaScript Document
//获取地址栏参数
function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     return r!=null?unescape(r[2]):null;
}

function ScrollLoad(options)
{
    if(options.scroll_percent==undefined)
    {
        options.scroll_percent=95;
    }   
    if(options.loading==undefined)
    {
        options.loading="";
    }
    this.options=options;
    if(this.options.success==undefined)
    {
        this.options.success=function(){};
    }
    this.ajax_handle=null;
    var this_obj=this;
    this.loadPage=function(is_abort){//加载页，如果在前端有其它操作要清空然后重新载入，可调用该函数
        if(is_abort==undefined)
        {
            is_abort=false;
        }
        
        if(!is_abort&&this_obj.ajax_handle!=null&&this_obj.ajax_handle.readyState!=4)//上一次的ajax还没有完成
        {
            return ;
        }
        else if(is_abort&&this_obj.ajax_handle!=null)
        {
            this_obj.ajax_handle.abort();
            this_obj.ajax_handle=null;
        }
        if($(this_obj.options.next_a).size()<1)//最后一页，没有下一页了
        {
            return ;
        }
        $(this_obj.loading).css("display","");
        var url=$(this_obj.options.next_a).attr("href");
        if(url.length<1)
        {
            return ;
        }
        if(url.indexOf("?")<0)
        {
            url+="?";
        }
        else
        {
            url+="&";
        }
        url+="offset="+$(">*",$(this_obj.options.container)).size();
        this_obj.ajax_handle=$.getJSON(url,function(html){
                $(this_obj.loading).css("display","none");
                this_obj.options.success(html);
            }
        );
    }
    
    
    $(options.container).closest(".touch_scroll_bar").scroll(function(){
        var total_height=$(this_obj.options.container).outerHeight(true);
        var window_height=$(this).height();
        var y=$(this).scrollTop();
        if((y+window_height)/total_height>this_obj.options.scroll_percent/100)
        {
            this_obj.loadPage();
        }
    }); 
}

/**
 *微信分享
 * @param _o:{imgurl,title,desc,content} 

function wx_share(_o)
{
    document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {
        var appId = '',
            imgUrl = _o.imgUrl,
            link = window.location.href,
            title = _o.title,
            desc = _o.desc,
            content = _o.content;
        
        // 发送给好友
        WeixinJSBridge.on('menu:share:appmessage', function(argv){
            WeixinJSBridge.invoke('sendAppMessage',{
                                  "appid":appId,
                                  "img_url":imgUrl,
                                  "img_width":"640",
                                  "img_height":"640",
                                  "link":link,
                                  "desc":desc,
                                  "title":title
                                  }, function(res) {})
        });
        // 分享到朋友圈
        WeixinJSBridge.on('menu:share:timeline', function(argv){
            WeixinJSBridge.invoke('shareTimeline',{
                                  "img_url":imgUrl,
                                  "img_width":"640",
                                  "img_height":"640",
                                  "link":link,
                                  "desc": desc,
                                  "title":title
                                  }, function(res) {
                                  });
        });

        // 分享到微博
        var weiboContent = '';
        WeixinJSBridge.on('menu:share:weibo', function(argv){
            WeixinJSBridge.invoke('shareWeibo',{
                                  "content":content,
                                  "url":link,
                                  }, function(res) {
                                  });
        });
        // 隐藏右上角的选项菜单入口
        //WeixinJSBridge.call('hideOptionMenu');
    }, false);
}
 */
/**
 * 微信处理 
 
document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {
    WeixinJSBridge.call('hideToolbar');
});

$(function(){
    $(".nav_bottom .refresh").live("click",function(){
        window.location.reload();
    });
    $(".nav_bottom .choose").live("click",function(){
        window.location.href="/wmhnew";
    });
    
    $(".nav_bottom .return").live("click",function(){
        window.history.back();
    });
    wx_share({imgUrl:"http://itv.tv.tvmining.com/images/wmh_logo.jpg",title:"微电视",desc:$("head title").text(),content:$("head title").text()});
    

});
*/