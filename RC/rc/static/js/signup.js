var isSignup = true;
var existId = false;

function modal_setMsg(msg) {
    $("#msg").text(msg);
}

function modal_toggle() {
    $("#myModal").modal("show");
}

function setSelectForYear() {
    let myYear = $("#_birth_year").val();
    let toYear = new Date().getFullYear();
    for ( let year = toYear; year >= 1900; year-- ) {
        let option = `<option value="${year}">${year}</option>`;
        $("#birth_year").append(option);
    }
    if ( myYear ) {
        $("#birth_year").val(myYear).prop("selected", true);
    }
}

function setSelectForMonth() {
    let myMonth = $("#_birth_month").val();
    for ( let month = 1; month <= 12; month++ ) {
        let option = `<option value="${month}">${month}</option>`;
        $("#birth_month").append(option);
    }
    if ( myMonth ) {
        $("#birth_month").val(myMonth).prop("selected", true);
    }
}

function setSelectForDate() {
    let myDate = $("#_birth_date").val();
    for ( let month = 1; month <= 31; month++ ) {
        let option = `<option value="${month}">${month}</option>`;
        $("#birth_date").append(option);
    }
    if( myDate ) {
        $("#birth_date").val(myDate).prop("selected", true);
    }
}

function selectGender() {
    let myGender = $("#_gender").val();
    if ( myGender ) {
        $("#gender").val(myGender).prop("selected", true);
        isSignup = false;
    }
}

function check_username() {
    $("#msg").empty();
    var pattern = /^[a-zA-Z0-9]*$/g;
    if ( $("#username").val() == "") {
        $("#msg").text("아이디는 필수 입력 항목입니다.");
    } else if ( $("#username").val().length < 4 ||  $("#username").val().length > 20 )  {
        $("#msg").text("아이디는 '4 이상 20 이하'의 길이만 가능합니다.");
    } else if (! $("#username").val().match(pattern) ) {
        $("#msg").text("아이디는 알파벳 대소문자, 숫자만 사용 가능합니다.");
    } else {
        return true;
    }
    modal_toggle();
    return false;
}

function check_password1() {
    $("#msg").empty();
    // var pattern = /^.*(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$]).*$/;
    // if ( $("#password1").val().length < 8 )  {
    //     $("#msg").text("비밀번호는 8자 이상의 길이이어야 합니다.");
    // } else if (! pattern.test($("#password1").val()) ) {
    //     $("#msg").text("비밀번호는 알파벳 대소문자, 숫자, 특수문자(!@#$)를 최소 하나씩 포함해야합니다.");
    // } else if ( ( $("#username").val().length != 0 ) &&
    //         ( $("#password1").val().includes($("#username").val()) || $("#username").val().includes($("#password1").val()) ) ) {
    //     $("#msg").text("아이디와 유사한 비밀번호는 사용할 수 없습니다.");
    // } else {
    //     return true;
    // }
    // modal_toggle();
    // return false;
    return true;
};

function check_password2() {
    $("#msg").empty();
    if ( $("#password1").val() != $("#password2").val() )  {
        $("#msg").text("비밀번호가 일치하지 않습니다.");
    } else {
        return true;
    }
    modal_toggle();
    return false;
}


function check_email() {
    var email = $("#email").val();
    var regex = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
    if (email.length < 1) {
        $("#msg").text("이메일을 입력해주세요.");
    } else if (email.match(regex) == null) {
        $("#msg").text("이메일 형식이 잘못되었습니다.");
    } else {
        return true;
    }
    modal_toggle();
    return false;
}

function check_validate() {
    var success = false;
    var username = $("#username").val();
    if( isSignup && check_username() ) {
        $.ajax({
            type: "GET",
            url: "check_username/",
            data: {
                username : username
            },
            dataType : "json",
            async: false,
            success: function(data) {
                if ( data["result"] ){
                    $("#msg").text("이미 등록된 아이디 입니다.");
                    existId = true;
                } else {
                    if ( check_password1() && check_password2() && check_email()) {
                        $("#btn_submit").text("등록중");
                        $("#btn_submit").prop("disabled", true);
                        $("#btn_cancel").attr("onClick", "return false");
                        success = true;
                    }
                }
            },
            error: function( jqXHR, textStatus, errorThrown ){
                    alert("status: " + textStatus + "\nerror: " + jqXHR.error )
            }
        });
    }
    if ( !isSignup && !existId && check_password1() && check_password2()  && check_email() ) {
        return true;
    }
    if ( success ) {
        return true;
    }
    modal_toggle();
    return false;
}

// onload
$(function () {
    setSelectForYear();
    setSelectForMonth();
    setSelectForDate();
    selectGender();
})