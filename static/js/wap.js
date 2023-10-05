$(function(){
	$(".g_btn").on('click',function(){
		if($(".footer").hasClass("footer_on")){
			$(".footer").removeClass("footer_on");
			$(".footer").addClass("footer_down");
		}else{
			$(".footer").removeClass("footer_down");
			$(".footer").addClass("footer_on");
		}
	})

	$(".banner_box").on('click',function(){
		if($(this).find(".py_logo").hasClass("py_logo_add")){
			$(".banner_box").find(".mov_con").slideUp();
			$(".banner_box").find(".py_logo").removeClass("py_logo_add")
		}else{
			$(".banner_box").find(".mov_con").slideUp();
			$(".banner_box").find(".py_logo").removeClass("py_logo_add")
			$(this).find(".mov_con").slideDown();
			$(this).find(".py_logo").addClass("py_logo_add");
		}
	})

	if(document.querySelector(".j_footer_fixed")){
	    var myElement1 = document.querySelector(".j_footer_fixed");
	    // 创建 Headroom 对象，将页面元素传递进去
	    var headroom1  = new Headroom(myElement1,{
	      "tolerance": 0,
	      "offset": 0,
	      "classes": {
	        "initial": "animated",
	        "pinned": "footer_on",
	        "unpinned": "footer_down"
	      }
	    });
	    headroom1.init(); 
    }
})