function check_password() {
    var csrf_token = $('meta[name="csrf-token"]').attr("content");
    var password = $("#password").val();
    var validated_pwd = false;
    $.ajax({
        type: "POST",
        url: "/accounts/check_password2",
        dataType : "json",
        data: { password : password, "csrfmiddlewaretoken" : csrf_token },
        async: false
    }).done(function(res) {
        if ( res['result'] ) {
            validated_pwd = true;
        } else {
            alert("비밀번호가 일치하지 않습니다.");
        }
    });
    if (validated_pwd) {
        return true;
    }
    return false;
}

function check_amount() {
    var csrf_token = $('meta[name="csrf-token"]').attr("content");
    var u_id = $("#u_id").val();
    var amount = $("#amount").val();
    var validated_amount = false;
    $.ajax({
        type: "POST",
        url: "/accounts/myBalance",
        dataType : "json",
        data: { u_id : u_id, "csrfmiddlewaretoken" : csrf_token },
        async: false
    }).done(function(res) {
        var balance = parseInt(res['balance']);
        if ( balance && (balance >= amount) ) {
            validated_amount = true;
        } else {
            alert("보유 잔액이 부족합니다.");
        }
    });
    if (validated_amount) {
        return true;
    }
    return false;
}


function payment() {
    var csrf_token = $('meta[name="csrf-token"]').attr("content");
    var u_id = $("#u_id").val();
    var s_id = $("#s_id").val();
    var amount = $("#amount").val();
    $.ajax({
        type: "POST",
        url: "/payment/payment",
        dataType : "json",
        data: { u_id : u_id, s_id : s_id, amount : amount, csrfmiddlewaretoken : csrf_token },
        async: false
    }).done(function(res) {
        var res = res['result'];
        alert(res);
        if (res) {
            alert("결제가 완료 되었습니다.");
            document.location.href = `"{% url 'profile:account_myInfo' ${ u_id }"`;
        } else {
            alert("결제 실패... 다시 시도해주세요.");
        }
    });
}


function check_validation() {
    if ( check_password() && check_amount() ) {
        payment();
    }
}