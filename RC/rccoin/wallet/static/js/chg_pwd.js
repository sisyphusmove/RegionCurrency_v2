function chk_password() {
    var msg = ""
    var pattern = /^.*(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$]).*$/
    
    if ( $("#password").val().length < 1) {
        $("#password").focus()
        msg = "현재 비밀번호를 입력해주세요."
    } else if ( ($("#password1").val()).length < 8 )  {
        $("#password1").focus()
        msg = "새 비밀번호는 8자 이상의 길이이어야 합니다."
    } else if (! pattern.test($("#password1").val()) ) {
        $("#password1").focus()
        msg = "새 비밀번호는 알파벳 대소문자, 숫자, 특수문자(!@#$)를 최소 하나씩 포함해야합니다."
    } else if ( $("#password").val() == $("#password1").val() ) {
        $("#password1").focus()
        msg = "현재 비밀번호와 같은 비밀번호는 사용할 수 없습니다."
    } else if ( $("#password1").val() != $("#password2").val() ) {
        $("#password2").focus()
        msg = "새 비밀번호가 일치하지 않습니다."
    } else {    
        $("#btn-submit").attr("onClick", "return false");
        $("#btn-cancel").attr("onClick", "return false");
        return true
    }
    alert(msg)
    return false

    $("body").loadingModal({
        position: "auto",
        color: "#fff",
        opacity: "0.7",
        backgroundColor: "rgb(0,0,0)",
        animation: "fadingCircle",
        text: "Loading..."
    })
    // return true
}