        document.getElementById("category").style.height = document.body.scrollHeight + "px";
        document.getElementById("wrapper").style.height = document.body.scrollHeight + "px";
        var scroller1, scroller2;
        function loaded() {
            scroller1 = new iScroll('category');
            scroller2 = new iScroll('wrapper');
        }

        document.addEventListener('touchmove', function(e){
            e.preventDefault();
        }, false);
        
        /* * * * * * * *
         *
         * Use this for high compatibility (iDevice + Android)
         *
         */
        document.addEventListener('DOMContentLoaded', function(){
            setTimeout(loaded, 200);
        }, false);
