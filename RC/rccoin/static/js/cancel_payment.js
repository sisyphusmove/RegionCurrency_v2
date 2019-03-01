function check_password() {
    var csrf_token = $('meta[name="csrf-token"]').attr("content");
    var password = $("#password").val();
    var validated_pwd = false;
    $.ajax({
        type: "POST",
        url: "/account/chk_password/",
        dataType : "json",
        data: { password : password, csrfmiddlewaretoken : csrf_token },
        async: false
    }).done(function(res) {
        if ( res['exist'] ) {
            validated_pwd = true;
        }
    });
    return validated_pwd
}

function chk_validate() {
    var msg = ""
    if ( !$("#agree").is(":checked") ) {
        $("#agree").focus()
        msg = "약관 동의 후, 결제취소가 가능합니다."
    } else if ( !check_password() ) {
        $("#password").focus()
        msg = "비밀번호가 일치하지 않습니다."
    }  else {
        $("#btn-submit").attr("onClick", "return false")
        $("#btn-cancel").attr("onClick", "return false")
        $("body").loadingModal({
            position: "auto",
            color: "#fff",
            opacity: "0.7",
            backgroundColor: "rgb(0,0,0)",
            animation: "fadingCircle",
            text: "Loading..."
        })
        return true
    }
    alert(msg)
    return false
}