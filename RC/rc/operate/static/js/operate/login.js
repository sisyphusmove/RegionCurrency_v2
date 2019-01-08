var isValidated = false;

function modal_setMsg(msg) {
    // $("#msg").text(msg);
    if(msg == 'id'){
        $(".alert_bar_id").show();
    }else if(msg == 'pass'){
        $(".alert_bar_pass").show();
    }else if(msg == 'id_or_pass'){
        $(".alert_bar_id_or_pass").show();
    }
}

function modal_toggle() {
    $("#myModal").modal("show");
}

function check_validate() {
    var username = $("#modalLRInput10").val();
    var password = $("#modalLRInput11").val();
    alert(username)
    if (username.length < 1) {
        modal_setMsg('id');
        // modal_toggle();
        return false;
    } else if (password.length < 1) {
        modal_setMsg('pass');
        // modal_toggle();
        return false;
    }
    alert(1234)
    return true;
}

function login_failed() {
    if ($("#status").val() == "failed") {
        modal_setMsg('id_or_pass');
    }
}

$(function() {
    login_failed();
})