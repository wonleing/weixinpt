        $(document).bind('touchstart', function(){
        });
        var nav = $(".nav");
        var bottom = $(".bottom_info");
        nav.delegate(".nav_style", "click", (function(){
            nav.find(".nav_style").removeClass("pressed");
            $(this).addClass("pressed");
            bottom.find(".info").hide();
               if($(this).attr("tag")=="series"){
                   if(type==2){
                       bottom.find(".comment").show();
                   }else{
                       bottom.find(".series").show();
                   }
               }else{
                   bottom.find("." + $(this).attr("tag") + "").show();
               }
        }));
        var seriesDiv = nav.find(".series");
        var commentDiv = bottom.find(".comment");
        if (type == 1) {
            seriesDiv.hide();
            commentDiv.hide();
            nav.find(".profile").addClass("pressed");
            bottom.find(".profile").show();
        }
        else
            if (type == 2) {
                seriesDiv.show();
                commentDiv.show();
            }
            else {
                seriesDiv.show();
                bottom.find(".series").show();
            }
