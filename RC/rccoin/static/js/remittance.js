var id_isValidated = false

function chk_target() {
    let target = $("#target").val()
    msg = ""
    if ( target.length < 1 ) {
        msg = "받는 계정을 입력해주세요."
    } else if ( target == $("#to").val() ) {
        id_isValidated = false
        msg = "자신에게는 송금할 수 없습니다."
    } else {
        $.ajax({
            type: "GET",
            url: "/account/chk_username",
            data: {
                username : target
            },
            dataType : "json",
            async: false,
        }).done(function(res) {
            if ( res["exist"] ) {
                id_isValidated = true
                msg = "송금 가능한 사용자입니다."
            } else {
                msg = "사용자 계정을 확인 할 수 없습니다."
            }        
        });
    }
    alert(msg)
}

function chk_password() {
    var csrf_token = $('meta[name="csrf-token"]').attr("content");
    var password = $("#password").val();
    var exist = false
    $.ajax({
        type: "POST",
        url: "/account/chk_password/",
        data: { password : password, "csrfmiddlewaretoken" : csrf_token },
        dataType : "json",
        async: false,
    }).done( function(res) {
        if ( res["exist"] ) {
            exist = true
        } else {
            exist = false
        }
    });
    return exist
}

function chk_validate() {
    var amount = parseInt($("#point").val().replace(/[^0-9]/g, '')) || 0;
    var balance = parseInt($("#balance").val().replace(/[^0-9]/g, '')) || 0;
    msg = ""
    if ( !id_isValidated ) {
        $("#target").focus()
        msg = '받는 계정을 조회해주세요.'
    } else if ( amount == 0 ) {
        $("#point").focus()
        msg = '송금액(RC)을 입력해 주세요.'
    } else if ( amount > balance ) {
        $("#point").focus()
        msg = '송금액이 보유잔액보다 큽니다.'
    } else if ( !$('#agree').is(":checked") ) {
        $("#agree").focus()
        msg = '송금 약관에 동의해 주세요.'
    } else if ( !chk_password() ) {
        $("#password").focus()
        msg = '비밀번호가 일치하지 않습니다.'
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

function numberWithCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

function getRestBalance() {
    var balance = parseInt($("#balance").val().replace(/[^0-9]/g, '')) || 0;
    var amount = parseInt($("#point").val().replace(/[^0-9]/g, '')) || 0;
    var restBalance = balance - amount;
    // console.log("balance:",balance,"amount:",amount,"restBalance:",restBalance)
    if (restBalance < 0 ){
        $("#point").focus()
        restBalanceCheck = 0;
        //   console.log("restBalanceCheck:",restBalanceCheck)
        $("#rest_balance").attr("value", numberWithCommas(balance))
    }
    else {
        $("#rest_balance").empty();
        $("#rest_balance").attr("value", numberWithCommas(restBalance))
        restBalanceCheck = 1;
        //   console.log("restBalanceCheck:",restBalanceCheck)
    }
}

$(function() {
    $("#target").on("change", function() {
        id_isValidated = false
    })
    $("#point").on("change", function() {
          getRestBalance()
    })
    $('#point').on('keyup', function() {
        if ($(this).val() != null && $(this).val() != '') {
          var tmps = parseInt($(this).val().replace(/[^0-9]/g, '')) || '0';
          var tmps2 = tmps.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
          $(this).val(tmps2);
        }
    });
})