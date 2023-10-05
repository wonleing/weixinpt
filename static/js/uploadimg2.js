$(document).ready(function () {
    $('#resetupload1').hide().on('click', function () {
        //$('#droppedimage').empty();
        $('#dropbox1').show();
        $('#resetupload1').hide();
    });
    $('#resetupload2').hide().on('click', function () {
        //$('#droppedimage2').empty();
        $('#dropbox2').show();
        $('#resetupload2').hide();
    });
    //商户大图
    var settings1 = $(".media-drop1").html5Uploader({
        postUrl: '../../uploadimg/?type=big&ext='+$('#fname1').val(),
        imageUrl: '',
        /**
         * File dropped / selected.
         */
        onDropped: function (success) {
            if (!success) {
                $('.errormessages').text('请上传jpg');
            } else {
                $('.errormessages').empty();
                $('.media-drop-placeholder > *').hide();
                $('.media-drop-placeholder').toggleClass('busyloading', true).css('cursor', 'progress');
            }
        },
        /**
         * Image cropped and scaled.
         */
        onProcessed: function (canvas) {
            if (canvas) {
                // Remove possible previously loaded image.
                var url = canvas.toDataURL();
                //var newImg = document.createElement("img");
                var newImg = document.getElementById('bigbanner');
                newImg.src = url;
                // Show new image.
                $('#droppedimage1').empty().append(newImg);
                // Hide dropbox.
                $('#dropbox1').hide();
                // Button to reset upload box.
                $('#resetupload1').show();
                // Reset dropbox for reuse.
                $('.errormessages').empty();
                $('.media-drop-placeholder > *').show();
                $('.media-drop-placeholder').toggleClass('busyloading', false).css('cursor', 'auto');
            } else {
                window.alert("不支持html5")
            }
        },
        /** Image uploaded.
         * @param success boolean True indicates success
         * @param responseText String Raw server response
         */
        onUploaded: function (success, responseText) {
            if (success) {
                $('#filename1').val("http://123.206.26.34/html/upload/"+responseText);
                window.alert(responseText+'上传成功');
            } else {
                $('#filename1').val("error");
                window.alert('上传失败'+responseText);
            }
        },
        /** Progress during upload.
         * @param progress Number Progress percentage
         */
        onUploadProgress: function (progress) {
            window.console && console.log('Upload progress: ' + progress);
        }
    });
    settings1.cropRatio = 16/9;
    settings1.maxLength = 640;

    //LOGO与头像
    var settings2 = $(".media-drop2").html5Uploader({
        postUrl: '../../uploadimg/?type=small&ext='+$('#fname2').val(),
        imageUrl: '',
        /**
         * File dropped / selected.
         */
        onDropped: function (success) {
            if (!success) {
                $('.errormessages').text('请上传jpg');
            } else {
                $('.errormessages').empty();
                $('.media-drop-placeholder > *').hide();
                $('.media-drop-placeholder').toggleClass('busyloading', true).css('cursor', 'progress');
            }
        },
        /**
         * Image cropped and scaled.
         */
        onProcessed: function (canvas) {
            if (canvas) {
                // Remove possible previously loaded image.
                var url = canvas.toDataURL();
                //var newImg = document.createElement("img");
                var newImg = document.getElementById('userlogo');
                newImg.src = url;
                // Show new image.
                $('#droppedimage2').empty().append(newImg);
                // Hide dropbox.
                $('#dropbox2').hide();
                // Button to reset upload box.
                $('#resetupload2').show();
                // Reset dropbox for reuse.
                $('.errormessages').empty();
                $('.media-drop-placeholder > *').show();
                $('.media-drop-placeholder').toggleClass('busyloading', false).css('cursor', 'auto');
            } else {
                window.alert("不支持html5")
            }
        },
        /** Image uploaded.
         * @param success boolean True indicates success
         * @param responseText String Raw server response
         */
        onUploaded: function (success, responseText) {
            if (success) {
                $('#filename2').val("http://123.206.26.34/html/upload/"+responseText);
                window.alert(responseText+'上传成功');
            } else {
                $('#filename2').val("error");
                window.alert('上传失败'+responseText);
            }
        },
        /** Progress during upload.
         * @param progress Number Progress percentage
         */
        onUploadProgress: function (progress) {
            window.console && console.log('Upload progress: ' + progress);
        }
    });
    settings2.cropRatio = 1;
    settings2.maxLength = 150;
});
