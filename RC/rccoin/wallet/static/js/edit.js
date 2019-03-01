function setSelectForYear() {
    let myYear = $("#_birth_year").val()
    let toYear = new Date().getFullYear()
    for ( let year = toYear; year >= 1900; year-- ) {
        let option = `<option value="${year}">${year}</option>`
        $("#birth_year").append(option)
    }
    if ( myYear ) {
        $("#birth_year").val(myYear).prop("selected", true)
    }
}

function setSelectForMonth() {
    let myMonth = $("#_birth_month").val()
    for ( let month = 1; month <= 12; month++ ) {
        let option = `<option value="${month}">${month}</option>`
        $("#birth_month").append(option)
    }
    if ( myMonth ) {
        $("#birth_month").val(myMonth).prop("selected", true)
    }
}

function setSelectForDate() {
    let myDate = $("#_birth_date").val()
    for ( let month = 1; month <= 31; month++ ) {
        let option = `<option value="${month}">${month}</option>`
        $("#birth_date").append(option)
    }
    if( myDate ) {
        $("#birth_date").val(myDate).prop("selected", true)
    }
}

function selectGender() {
    let myGender = $("#_gender").val()
    if ( myGender ) {
        $("#gender").val(myGender).prop("selected", true)
        isSignup = false
    }
}

function chk_email() {
    var msg = ""
    var email = $("#email").val()
    var regex = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i
    if ( email.length < 1 ) {
        msg = "이메일을 입력해주세요."
    } else if ( email.match(regex) == null ) {
        msg = "이메일 형식이 잘못되었습니다."
    } else {
        return true
    }
    alert(msg)
    return false
}

function chk_validate() {
    if ( !chk_email() ) {
        return false
    }
    $("#btn-submit").attr("onClick", "return false");
    $("#btn-cancel").attr("onClick", "return false");
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

// onload
$(function () {
    setSelectForYear()
    setSelectForMonth()
    setSelectForDate()
    selectGender()
})