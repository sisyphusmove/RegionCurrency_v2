// validation

var idCheck = 0;
var pwCheck = 0;
var agreeCheck = 0;
var restBalanceCheck = 0;

function getRestBalance() {
    var balance = $("#balance").val();
    var amount = parseInt($("#point").val().replace(/[^0-9]/g, '')) || 0;
    var restBalance = balance - amount;
    // console.log("balance:",balance,"amount:",amount,"restBalance:",restBalance)
    if (restBalance < 0 ){
      alert("송금액이 잔액을 초과하였습니다. 다시 입력해주세요.") 
      restBalanceCheck = 0;
    //   console.log("restBalanceCheck:",restBalanceCheck)
    }
    else {
      $("#rest_balance").empty();
      $("#rest_balance").attr("value", restBalance);
      restBalanceCheck = 1;
    //   console.log("restBalanceCheck:",restBalanceCheck)
    }
  }
  
  $(function() {
    $("#point").change(function() {
    //   console.log($("#point").val());
      getRestBalance();
    });
  
  })


$(function() {
    $("#btn_chk_id").click(function() {
        check_username();
    });
})

function check_username() {
    var username = $("#target").val();
    var from = $("#from").val();
    $.ajax({
        type: "GET",
        url: "/accounts/check_username2",
        data: {
            username : username
        },
        dataType : "json",
        async: false,
        success: function(data) {
            if ( username == from ){
                alert("자신에게 송금할 수 없습니다.");
                idCheck = 0;
            } else if ( data["result"] != 0 ){
                // $("#msg").text("이미 등록된 아이디 입니다.");
                alert("아이디가 확인되었습니다.");
                idCheck = 1;
            } else {
                alert("존재하지 않는 아이디입니다. 아이디를 다시 확인해주세요.");
                idCheck = 0;
            }
        },
        error: function( jqXHR, textStatus, errorThrown ){
            alert("status: " + textStatus + "\nerror: " + jqXHR.error )
        }
    });
    // console.log("idCheck:",idCheck);
    return idCheck;
    
}

function check_password() {
    var csrf_token = $('meta[name="csrf-token"]').attr("content");
    var password = $("#password").val();
    $.ajax({
        type: "POST",
        url: "/accounts/check_password2",
        data: { password : password, "csrfmiddlewaretoken" : csrf_token },
        dataType : "json",
        async: false,
        success: function(data) {
            if ( data["result"] ){
                // $("#msg").text("이미 등록된 아이디 입니다.");
                // alert("비밀번호가 확인되었습니다.");
                pwCheck = 1;
            } else {
                alert("비밀번호가 일치하지 않습니다.");
                pwCheck = 0;
            }
        },
        error: function( jqXHR, textStatus, errorThrown ){
            alert("status: " + textStatus + "\nerror: " + jqXHR.error )
        }
    });
    // console.log("pwCheck:",pwCheck);
    return pwCheck;
}

function agree() {
    if ($('#agree').is(":checked")) {
        agreeCheck = 1;
        // console.log("argeeCheck:",agreeCheck);
    }
    else {
        agreeCheck = 0;
        alert("약관에 동의해주세요.");
        // console.log("argeeCheck:",agreeCheck);
    }

}

function validationCheck() {
    // console.log("test")
    check_password();
    agree();
    if (idCheck==1&&pwCheck==1&&restBalanceCheck==1&&agreeCheck==1) {
        return true;
    }
    return false;
}
