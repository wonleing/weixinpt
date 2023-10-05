$(document).ready(function(){

    $(document).bind('touchstart', function(){
    });
    var titleSwipe = $(".titleSwipe");
    window.categorySwipe = Swipe(document.getElementById('categorySwipe'), {
        startSlide: 0,
        continuous: true,
        disableScroll: false,
        // stopPropagation: true,
        callback: function(index, element){
        },
        transitionEnd: function(index, element){
        }
    });
    window.movieSwipe = Swipe(document.getElementById('movieSwipe'), {
        startSlide: 0,
        continuous: true,
        disableScroll: false,
        // stopPropagation: true,
        callback: function(index, element){
            categorySwipe.slide(parseInt(index / 3));
            titleSwipe.find(".swipe_category").removeClass("pressed");
            titleSwipe.find('div[id=' + index + ']').addClass("pressed");
        },
        transitionEnd: function(index, element){
        }
    });
    
    
    titleSwipe.find(".swipe_category").click(function(){
        titleSwipe.find(".swipe_category").removeClass("pressed");
        $(this).addClass("pressed");
        movieSwipe.slide($(this).attr("id"));
    });
    
    
    $(".more_free").click(function(){
        var thisElement = $(this);
        if (thisElement.hasClass("loading")) {
            return;
        }
        var categoryId = thisElement.attr("categoryId");
        var pageNum = thisElement.attr("pageNum");
        thisElement.html("正在加载中...").addClass("loading");
        
		var parentElement=$(this).parent();
		var id=parentElement.attr("id");
		var pagenum=parentElement.attr("swipe_pagenum");
        $.ajax({
            url: "/lxtj/getmore/free/"+id+"/"+pagenum+"/",
            type: 'GET',
            dataType: 'json',
            timeout: 3e4,
            success: function(json){
                console.log(json);
                if (typeof json == "undefined") {
                    console.log("empty data.");
                }
                
                var list = json.result.pageContent;
                var listObj = thisElement.prev();
                for (var i in list) {
                    listObj.append(renderFreeMovie(list[i]));
                }
                
                thisElement.removeClass("loading");
                thisElement.html("加载更多");
				
				parentElement.attr("swipe_pagenum",parseInt(pagenum)+1);
            },
            error: function(){
				thisElement.hide();
            }
        });
    });
    
    $(".more_charge").click(function(){
        var thisElement = $(this);
        if (thisElement.hasClass("loading")) {
            return;
        }
        var categoryId = thisElement.attr("categoryId");
        var pageNum = thisElement.attr("pageNum");
        thisElement.html("正在加载中...").addClass("loading");

                var parentElement=$(this).parent();
                var id=parentElement.attr("id");
                var pagenum=parentElement.attr("swipe_pagenum");
        $.ajax({
            url: "/lxtj/getmore/charge/"+id+"/"+pagenum+"/",
            type: 'GET',
            dataType: 'json',
            timeout: 3e4,
            success: function(json){
                console.log(json);
                if (typeof json == "undefined") {
                    console.log("empty data.");
                }

                var list = json.data.result.pageContent;
                var listObj = thisElement.prev();
                for (var i in list) {
                    listObj.append(renderChargeMovie(id, list[i]));
                }

                thisElement.removeClass("loading");
                thisElement.html("加载更多");

                                parentElement.attr("swipe_pagenum",parseInt(pagenum)+1);
            },
            error: function(){
                                thisElement.hide();
            }
        });
    });
    
    function renderFreeMovie(data){
        if (data.videoset_type == 1 || data.videoset_type == 2 || data.videoset_type == 4 ||  data.videoset_type == 6){
            var img = data.videoset_tv_img;
        } else {
            var img = data.videoset_img;
        }
        return '<div class="swipe_image">' +
        '<a href="../../../lxtj/detail/' + data.videoset_type + '/' + data.videoset_id + '?wxid=' + wxid + '" >' +
        '<img src="' +
        img +
        '">' +
        '</img></a>' +
        '<div class="name">' +
        data.videoset_name +
        ' </div>' +
        '</div>';
    }
    
    function renderChargeMovie(opid, data){
        return '<div class="swipe_image">' +
        '<a href="../../../lxtj/payarea/?vid=' + data.contentId + '&opid=' + opid + '&wxid=' + wxid + '" >' +
        '<img src="' +
        data.contentPosters +
        '">' +
        '</img></a>' +
        '<div class="name">' +
        data.contentName +
        ' </div>' +
        '</div>';
    }
    
    renderCurrentCategory();
    function renderCurrentCategory(){
        var categoryNum = parseInt($("#categorySwipe").find(".pressed").parent().parent().attr("swipe_pagenum"));
        var movieNum = parseInt($("#categorySwipe").find(".pressed").attr("swipe_pagenum"));
        categorySwipe.slide(categoryNum);
        movieSwipe.slide(movieNum);
    }
});
