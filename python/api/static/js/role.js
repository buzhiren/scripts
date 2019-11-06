


// 查询
function queryrole() {
        $.ajax({
        type: 'GET',
        url: 'http://192.168.193.10/v1/role/all',
        // data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        async:false,
        dataType: 'json',
        success: function(data) {
            var role_data = eval(data)
            // return ""
            console.log(role_data)
            }
     })
       // return role_data;
}









//修改
function queryrt() {
        $.ajax({
        type: 'GET',
        url: 'http://192.168.193.10/v1/role/all',
        // data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        async:false,
        dataType: 'json',
        success: function(data) {
            role_data = eval(data)
            return ""
            }
     })
        return role_data;
}



function delaction(){
    var u = $('#username').val();
    var o = $("#wrap input[name='grader']:checked").val();
    if(u == ""){
        alert("请输入用户名")
    return false;
    }
    var all_data = queryrt()['data'];
    console.log(all_data)
    var number = all_data.length
    for(var n=0; n <number; n++) {
        if( u == all_data[n]['username'] ){
            var id_info = all_data[n]['id']
            break;
        }
    }
    var data = {
        "newvalue":o,
    }

    $.ajax({
        type: 'POST',
        url: 'http://192.168.193.10/v1/role/'+id_info,
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var info = eval(data)
            var judge = info['data']["judge"]
            var messg = info['data']["messg"]
            if( judge == 'True'){
                alert('修改成功')
                // window.location.href = '/static/html/asset.html';
            } else {
                alert('修改失败'+messg)
            };
         }
     })
}


// 查询单个角色
function querysingle(){
    var u = $("#selename").val();
    var all_data = queryrt()['data'];
    console.log(all_data);
    var number = all_data.length
    for(var n=0; n <number; n++) {
        if( u == all_data[n]['username'] ){
            var id_info = all_data[n]['role']
            break;
        } else if(u != all_data[n]['username']){
            var id_info = "不存在"
        }
    }
    alert(u+"的角色为： "+id_info);
}



function dropsingle() {
    var u = $("#dropname").val();
    var all_data = queryrt()['data'];
    var number = all_data.length
    for(var n=0; n <number; n++) {
        if( u == all_data[n]['username'] ){
            var id_info = all_data[n]['id']
            break;
        } else if(u != all_data[n]['username']){
            var id_info = "不存在"
        }
    }
    $.ajax({
        type: 'DELETE',
        url: 'http://192.168.193.10/v1/role/'+id_info,
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var info = eval(data)
            var judge = info['data']["judge"]
            var messg = info['data']["messg"]
            if( judge == 'True'){
                alert('修改成功')
                // window.location.href = '/static/html/asset.html';
            } else {
                alert('修改失败'+messg)
            };
         }
     })

}



// function exhaction(){
//     var o = $("#arap input[name='exh']:checked").val();
//     var data={
//         "judge":o
//     }
//     console.log(data)
//     $.ajax({
//         type: 'GET',
//         url: '/user/v1/role/showall',
//         data: data,
//         contentType: 'application/json; charset=UTF-8',
//         dataType: 'json',
//         success: function(data){
//             var list = eval(data)
//             var showall = list['showall']
//     console.log(showall);
//     alert(showall);
//         }
//     })
//
// }
