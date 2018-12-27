var toId = 0;

function check_username() {
    var username = $("#target").val();
    $.ajax({
        type: "GET",
        url: "/accounts/check_username2",
        data: {
            username : username
        },
        dataType : "json",
        async: false,
        success: function(data) {
            if ( data["result"] != 0 ){
                // $("#msg").text("이미 등록된 아이디 입니다.");
                alert("확인되었습니다.");
                toId = data["result"];
            } else {
                alert("아이디를 다시 확인해주세요. 존재하지 않는 아이디입니다.");
            }
        },
        error: function( jqXHR, textStatus, errorThrown ){
            alert("status: " + textStatus + "\nerror: " + jqXHR.error )
        }
    });

    return toId;
}

function check_password() {
    var password = $("#password").val();
    $.ajax({
        type: "GET",
        url: "/accounts/check_password2",
        data: {
            password : password
        },
        dataType : "json",
        async: false,
        success: function(data) {
            if ( data["result"] ){
                // $("#msg").text("이미 등록된 아이디 입니다.");
                alert("확인되었습니다.");
            } else {
                alert("비밀번호가 일치하지 않습니다.");
            }
        },
        error: function( jqXHR, textStatus, errorThrown ){
            alert("status: " + textStatus + "\nerror: " + jqXHR.error )
        }
    });
}

$(function() {
    $("#btn_chk_id").click(function() {
        check_username();
    });

    $("#btn_submit").click(function() {
        if ( check_password() ) {
            return true;
        }
        return false;
    });
})

function withdraw_submit() {
    var transfer = "transfer"
    var from_id = $("#from").val();
    var to_id = check_username();
    var amount = $("#point").val();
	amount = parseInt(amount.replace(/,/g, ''));
	

    var type = 5;
    var current = new Date().toISOString().slice(0,10); 
 
    console.log(transfer,from_id,to_id,amount,type,current);
    var urls = "http://210.107.78.166:8000/transfer/"+from_id+"/"+to_id+"/"+amount+"/"+type+"/"+current
    $.ajax({
        url: urls, // 클라이언트가 HTTP 요청을 보낼 서버의 URL 주소
        method: "GET",
        dataType: "json",
        success: function(data) {
            if ( data["result"] ){
                // $("#msg").text("이미 등록된 아이디 입니다.");
                alert("확인되었습니다.");
            } else {
                alert("비밀번호가 일치하지 않습니다.");
            }
        },
        error: function( jqXHR, textStatus, errorThrown ){
            alert("status: " + textStatus + "\nerror: " + jqXHR.error )
        }
    })
    
}


$(function() {
    $("#btn_submit").click(function() {
        withdraw_submit();

    });
});