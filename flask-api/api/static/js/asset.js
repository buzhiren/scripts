//全局变量

// asset_data = ""





// 增加资产
function showmodel() {
    document.getElementById('i1').classList.remove('hide')
    document.getElementById('i2').classList.remove('hide')
}
function hidemodel() {
    document.getElementById('i1').classList.add('hide')
    document.getElementById('i2').classList.add('hide')
}

function submitmodel() {
    var assnumber = $('#assnumber').val();
    var type = $('#type').val();
    var brand = $('#model').val();
    var price = $('#price').val();
    var owner = $('#owner').val();
    var pur_time = $('#pur_time').val();
    var begin_time = $('#begin_time').val();
    var end_time = $('#exp_time').val();
    var state = $('#state').val();

    var ins_data = {
        'g_number': assnumber,
        'g_type': type,
        'g_brand':brand,
        'g_price':price,
        'g_owner':owner,
        'pur_time':pur_time,
        'begin_time':begin_time,
        'end_time':end_time,
        'g_state':state,
    }
    console.log(ins_data)
    $.ajax({
        type: 'POST',
        url: 'http://192.168.193.10/v1/asset/',
        data: JSON.stringify(ins_data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var info = eval(data)
	    console.log(info)
            var judge = info["judge"]
            var messg = info["messg"]
            if( judge == 'True'){
                alert('添加成功')
                window.location.href = 'http://192.168.193.10/asset.html';
            } else {
                alert('添加失败'+messg)
            };
         }
     })
}


// 查看资产
function querymodel() {
        $.ajax({
        type: 'GET',
        url: 'http://192.168.193.10/v1/asset/all',
        // data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var asset_data = eval(data)
            console.log(asset_data)
	    alert(asset_data)
            }
     })

}




// 修改资产
function modify() {
    document.getElementById('x1').classList.remove('hide')
    document.getElementById('x2').classList.remove('hide')
}

function modifymodel(){
    document.getElementById('x1').classList.add('hide')
    document.getElementById('x2').classList.add('hide')
}


function queryt() {
        $.ajax({
        type: 'GET',
        url: '/v1/asset/all',
        // data: JSON.stringify(data),
        async:false,
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            asset_data = eval(data)
            return ""
            // console.log(asset_data)
            }
     })
        return asset_data;
}


function change() {
    var asnum = $('#asnum').val();
    var pject = $('#project').val();
    var cont = $('#content').val();
    var all_data = queryt();
    //var res_info = all_data['data']
    var number = all_data.length
    for(var n=0; n <number; n++) {
        if( asnum == all_data[n]['g_number'] ){
            var id_info = all_data[n]['id']
            break;
        }
    }
    var  data = {
        "field": pject,
        "newvalue": cont,
        "id":id_info,

    }
    $.ajax({
        type: 'PUT',
        url: '/v1/asset/'+id_info,
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var info = eval(data)
            var judge = info["judge"]
            var messg = info["messg"]
            if( judge == 'True'){
                alert('修改成功')
                // window.location.href = '/static/html/asset.html';
            } else {
                alert('修改失败'+messg)
            };
        }
     })

}




// 删除资产
function delect() {
    document.getElementById('s1').classList.remove('hide')
    document.getElementById('s2').classList.remove('hide')
}

function delectmodel(){
    document.getElementById('s1').classList.add('hide')
    document.getElementById('s2').classList.add('hide')
}


function delectaction() {
    var g_number = $('#numt').val();
    var data = {
        "g_number":g_number
    }

    var all_data = queryt();
    var number = all_data.length
    for(var n=0; n <number; n++) {
        if( g_number == all_data[n]['g_number'] ){
            var id_info = all_data[n]['id']
            break;
        }
    }
    $.ajax({
        type: 'DELETE',
        url: '/v1/asset/'+id_info,
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var info = eval(data)
            var judge = info["judge"]
            var messg = info["messg"]
            if( judge == 'True'){
                alert('删除成功')
                // window.location.href = '/static/html/asset.html';
            } else {
                alert('删除失败'+messg)
            };
        }
     })


}
