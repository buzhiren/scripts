

// 申请资产
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
                window.location.href = 'http://192.168.193.10/ord_asset.html';
            } else {
                alert('添加失败'+messg)
            };
         }
     })
}





// 退换资产

function replacement() {
    document.getElementById('t1').classList.remove('hide')
    document.getElementById('t2').classList.remove('hide')
}
function returnmodel() {
    document.getElementById('t1').classList.add('hide')
    document.getElementById('t2').classList.add('hide')
}

function retreat() {
    var g_number = $('#g_number').val();
    // var g_reason = $('#g_reason').val();

    var data = {
       // "apply_demand": "退回",
        "g_number": g_number,
       // "g_reason": g_reason,
    }
    console.log(data)
    $.ajax({
        type: 'POST',
        url: 'http://192.168.193.10/v1/ord_asset/'+g_number,
        data: JSON.stringify(data),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
            var info = eval(data);
            console.log(info)
            var judge = info['data']["judge"]
            var messg = info['data']["messg"]
            if( judge == 'True'){
                alert('退回成功, 状态为： '+messg)
                window.location.href = 'http://192.168.193.10/ord_asset.html';
            } else {
                alert('退回失败'+messg)
            };
         }
     })
}
