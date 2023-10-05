/** 
 * JQ评分效果 
 */  
 function Score(options) {  
    this.config = {  
        selector                  :   '.star',     // 评分容器  
        renderCallback            :   null,        // 渲染页面后回调  
        callback                  :   null         // 点击评分回调                           
    };  
  
    this.cache = {  
        aMsg : [  
                "很不满意|一星",  
                "不满意|二星",  
                "一般|三星",  
                "满意|四星",  
                "非常满意|五星"  
                ],  
        iStar  : 0,  
        iScore : 0  
    };  
  
    this.init(options);  
 }  
  
 Score.prototype = {  
  
    constructor: Score,  
  
    init: function(options){  
        this.config = $.extend(this.config,options || {});  
        var self = this,  
            _config = self.config,  
            _cache = self.cache;  
  
        self._renderHTML();  
    },  
    _renderHTML: function(){  
        var self = this,  
            _config = self.config;  
        var html = '<span class="desc"></span>' +   
                   '<p class="star-p hidden"></p>';  
        $(_config.selector).each(function(index,item){  
            $(item).append(html);  
            $(item).wrap($('<div class="parentCls" style="position:relative"></div>'));  
            var parentCls = $(item).closest('.parentCls');  
            self._bindEnv(parentCls);  
            _config.renderCallback && $.isFunction(_config.renderCallback) && _config.renderCallback();  
        });  
  
    },  
    _bindEnv: function(parentCls){  
        var self = this,  
            _config = self.config,  
            _cache = self.cache;  
  
        $(_config.selector + ' li',parentCls).each(function(index,item){  
              
            // 鼠标移上  
            $(item).mouseover(function(e){  
                var offsetLeft = $('ul',parentCls)[0].offsetLeft;  
                ismax(index + 1);  
                //$('p',parentCls).hasClass('hidden') && $('p',parentCls).removeClass('hidden');  
                //$('p',parentCls).css({'left':index*$(this).width() + 12 + 'px'});  
                var html = '<em>' + _cache.aMsg[index].split('|')[0]+'' +   
                           '</em>' + _cache.aMsg[index].split('|')[1];  
                $('.desc',parentCls).html(html);
                $('#status').val(index+1);
                //$('p',parentCls).html(html);  
            });  
  
            // 鼠标移出  
            $(item).mouseout(function(){  
                ismax(index+1);  
                !$('p',parentCls).hasClass('hidden') && $('p',parentCls).addClass('hidden');  
            });  
        });  
  
        function ismax(iArg) {  
            _cache.iScore = iArg || _cache.iStar;  
            var lis = $(_config.selector + ' li',parentCls);  
              
            for(var i = 0; i < lis.length; i++) {  
                lis[i].className = i < _cache.iScore ? "on" : "";  
            }  
        }  
    }  
 };
