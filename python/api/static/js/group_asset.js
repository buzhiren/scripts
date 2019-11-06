

// 创建资产组
function showmodel() {
    document.getElementById('i1').classList.remove('hide')
    document.getElementById('i2').classList.remove('hide')
}
function hidemodel() {
    document.getElementById('i1').classList.add('hide')
    document.getElementById('i2').classList.add('hide')
}




function submitmodel() {
    var group_asset = $('#grup_asset').val();

    console.log(group_asset)

    var data = {
        "group_name":group_asset
    }

    $.ajax({
        type: 'POST',
        url: 'http://192.168.193.10/v1/group_asset/',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        async:false,
        success: function(data) {
            var info = eval(data)
            console.log(info)
            var judge = info['data']["judge"]
            var messg = info['data']["messg"]
            if( judge == 'True'){
                alert('添加成功')
                window.location.href = 'http://192.168.193.10/group_asset.html';
            } else {
                alert('添加失败'+messg)
            };
         }
     })

}

//  查看资产
function query() {
        $.ajax({
        type: 'GET',
        url: 'http://192.168.193.10/v1/group_asset/all',
        // data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var asset_data = eval(data)
            console.log(asset_data['data'])
            }
     })

}





//  关联资产组

function setmodel() {
    document.getElementById('x1').classList.remove('hide')
    document.getElementById('x2').classList.remove('hide')
}
function setasset() {
    document.getElementById('x1').classList.add('hide')
    document.getElementById('x2').classList.add('hide')
}

function submitset() {
    var grup_ast = $('#grup_ast').val();
    var asset_num = $('#asset_num').val();

    console.log(grup_ast)
    var data = {
        "grup_ast":grup_ast,
        "asset_num": asset_num,
    }

    $.ajax({
        type: 'POST',
        url: 'http://192.168.193.10/v1/group_asset/relation',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var asset_data = eval(data)
            console.log(asset_data['data'])
            }
     })
}






// 查看资产对应资产组
function querymodel() {
    document.getElementById('o1').classList.remove('hide')
    document.getElementById('o2').classList.remove('hide')
}
function queryasset() {
    document.getElementById('o1').classList.add('hide')
    document.getElementById('o2').classList.add('hide')
}

function querytset() {
    var asset_num = $('#oasset_num').val();

    console.log(asset_num)
    var data = {
        "asset_num": asset_num,
    }

    $.ajax({
        type: 'GET',
        url: 'http://192.168.193.10/v1/group_asset/'+asset_num,
        // data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var asset_data = eval(data)
	    var messg = asset_data['data']['messg']
	    alert(messg)	    
	    window.location.href = 'http://192.168.193.10/group_asset.html';
            }
     })
}
