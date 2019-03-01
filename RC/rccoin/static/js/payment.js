function chk_password() {
    var csrf_token = $('meta[name="csrf-token"]').attr("content")
    var password = $("#password").val()
    var isValid = false
    $.ajax({
        type: "POST",
        url: "/account/chk_password/",
        data: { password : password, "csrfmiddlewaretoken" : csrf_token },
        dataType : "json",
        async: false,
        success: function(data) {
            if ( data["exist"] ){
                isValid = true
            }
        },
        error: function( jqXHR, textStatus, errorThrown ){
            alert("status: " + textStatus + "\nerror: " + jqXHR.error )
        }
    })
    return isValid
}

function agree() {
    if ($('#agree').is(":checked")) {
        return true
    }
    return false
}

function chk_validate() {
    var msg = ""
    var amount = parseInt($("#amount").val().replace(/[^0-9]/g, "")) || 0;
    var balance = parseInt($("#balance").val().replace(/[^0-9]/g, "")) || 0;
    var pwd = $("#password").val()

    if ( amount == 0 ) {
        $("#amount").focus()
        msg = "결제금액을 입력해주세요."
    } else if ( amount > balance ) {
        $("#amount").select()
        msg = "결제금액이 보유금액을 초과합니다."
    } else if ( !agree() ) {
        $("#agree").focus()
        msg = "약관에 동의후, 결제를 진행할 수 있습니다."
    } else if ( pwd.length < 1 ) {
        $("#password").select()
        msg = "비밀번호를 입력해주세요."
    } else if ( !chk_password() ) {
        $("#password").select()
        msg = "비밀번호가 일치하지 않습니다."
    } else {
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