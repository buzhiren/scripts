function login(){
    var u = $('#username').val();
    var p = $('#password').val();
    var data={
        'username':u,
        'password':p
    }
    //console.log(data);
    $.ajax({
        type: 'POST',
        url: 'http://192.168.193.10/v1/user',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var result = eval(data)
            var info = result['user']
            console.log(info)
            var judge = info["judge"]
            var role = info["role"]
            var messg = info["message"]
            console.log(judge)
            if( judge == 'True' && role == 'ordinary'){
                window.location.href = 'http://192.168.193.10/ord_asset.html';
            } else if ( judge == 'True' && role == 'admin' ) {
                window.location.href = 'http://192.168.193.10/asset.html';
            } else if(judge == 'True' && role == 'root'){
                window.location.href = 'http://192.168.193.10/home.html';
            } else if (judge == 'False'){
                 alert(messg);
            };
         }
     })
}
