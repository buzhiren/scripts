function  TipsInfo(){

     var md5_v=$("#md5sum").val();
     var file_v=$("#exampleInputFile").val();
     
     console.log(file_v)
     if(md5_v === ""){
         alert("请输入MD5.")
         event.preventDefault();
         return 
     }else if(file_v === ""){
         alert("请选择文件.")
         event.preventDefault();
         return
     };

    $('#progress_one').css('display', 'block');
    
    //获取上传的文件
    var uploadFile = $('#exampleInputFile').get(0).files[0];
    var formdata = new FormData();

    formdata.append('file', uploadFile);
    formdata.append('md5sum', md5_v);

    $.ajax({
        url: '/upload',
        type: 'post',
        data: formdata,
        dataType: "json",
        processData: false,
        contentType: false,
        xhr: function() {
            var xhr = new XMLHttpRequest();
            //使用XMLHttpRequest.upload监听上传过程，注册progress事件，打印回调函数中的event事件
            xhr.upload.addEventListener('progress', function (e) {
                //console.log(e);
                //loaded代表上传了多少
                //total代表总数为多少
                var num = Math.floor((e.loaded / e.total) * 100);
                var progressRate = num + '%'
                //通过设置进度条的宽度达到效果
                $('#p_cont').html("正在上传中[" + progressRate + "]")
                $('.progress-bar').css({"width": progressRate})
                if( progressRate === "100%"){
                    $('#p_cont').html("上传完成[100%]")
                };
            
            });
                  return xhr;
        }    
    });
};



function jump(){
    window.location.href='jenkins_upload';
}

