var id_isValidated = false

function setSelectForYear() {
    let myYear = $("#_birth_year").val()
    let toYear = new Date().getFullYear()
    for ( let year = toYear; year >= 1900; year-- ) {
        let option = `<option value="${year}">${year}</option>`
        $("#birth_year").append(option)
    }
}

function setSelectForMonth() {
    let myMonth = $("#_birth_month").val()
    for ( let month = 1; month <= 12; month++ ) {
        let option = `<option value="${month}">${month}</option>`
        $("#birth_month").append(option)
    }
}

function setSelectForDate() {
    let myDate = $("#_birth_date").val()
    for ( let month = 1; month <= 31; month++ ) {
        let option = `<option value="${month}">${month}</option>`
        $("#birth_date").append(option)
    }
}

function chk_username() {
    var msg = ""
    var pattern = /^[a-zA-Z0-9]*$/g
    if ( $("#username").val() == "") {
        msg = "아이디를 입력해주세요."
    } else if ( $("#username").val().length < 4 ||  $("#username").val().length > 20 )  {
        msg = "아이디는 '4 이상 20 이하'의 길이만 가능합니다."
    } else if (! $("#username").val().match(pattern) ) {
        msg = "아이디는 알파벳 대소문자, 숫자만 사용 가능합니다."
    } else {
        let username = $("#username").val()
        $.ajax({
            type: "GET",
            url: "/account/chk_username",
            data: {
                username : username
            },
            dataType : "json",
            async: false,
        }).done(function(res) {
            if ( res['exist'] ) {
                msg = "사용할 수 없는 아이디 입니다."
            } else {
                id_isValidated = true
                msg = "사용 가능한 아이디 입니다."
            }        
        });
    }
    if( !id_isValidated ) {
        $("#username").focus()
    }
    alert(msg)
}

function chk_password() {
    var msg = ""
    var pattern = /^.*(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$]).*$/
    // if ( $("#password1").val().length < 8 )  {
    //     msg = "비밀번호는 8자 이상의 길이이어야 합니다."
    // } else if (! pattern.test($("#password1").val()) ) {
    //     msg = "비밀번호는 알파벳 대소문자, 숫자, 특수문자(!@#$)를 최소 하나씩 포함해야합니다."
    // } else if ( ( $("#username").val().length != 0 ) &&
    //         ( $("#password1").val().includes($("#username").val()) || $("#username").val().includes($("#password1").val()) ) ) {
    //     msg = "아이디와 유사한 비밀번호는 사용할 수 없습니다."
    // } else if ( $("#password1").val() != $("#password2").val() ) {
    //     msg = "비밀번호가 일치하지 않습니다."
    // } else {
    //     return true
    // }
    // $("#password1").focus()
    // alert(msg)
    // return false
    return true
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
    $("#email").focus()
    alert(msg)
    return false
}

function chk_validate() {
    if ( !id_isValidated ) {
        alert("아이디 중복확인을 해주세요.")
        return false
    } else if ( !chk_password() ) {
        return false
    } else if ( !chk_email() ) {
        return false
    }
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
    // hide the loading modal
    // $('body').loadingModal('hide');
    // destroy the plugin
    // $('body').loadingModal('destroy');
    return true
}

// onload
$(function () {
    setSelectForYear()
    setSelectForMonth()
    setSelectForDate()
    
    $("#username").on("change", function() {
        id_isValidated = false
    })
})