function check_password() {
    var csrf_token = $('meta[name="csrf-token"]').attr("content");
    var password = $("#password").val();
    var validated_pwd = false;
    $.ajax({
        type: "POST",
        url: "/accounts/check_password2",
        dataType : "json",
        data: { password : password, csrfmiddlewaretoken : csrf_token },
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

function cancel() {
    if ( check_password() ) {
        alert("해당 결제를 취소합니다.");
        $("#cancel_payment").submit();
    }
}