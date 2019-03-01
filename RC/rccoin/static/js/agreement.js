function not_all_chk() {
    $("#chk_agreeAll").prop("checked", false)
}

function chk_agreeAll() {
    $("#chk_agree1").prop("checked", true)
    $("#chk_agree2").prop("checked", true)
}

function unchk_agreeAll() {
    $("#chk_agree1").prop("checked", false)
    $("#chk_agree2").prop("checked", false)
}

function check_validate() {
    if ( $("#chk_agree1").is(":checked") && $("#chk_agree2").is(":checked") ) {
        return true
    }
    return false
}

$(function() {
    $("#chk_agree1").change(function() {
        if (! $(this).is(":checked") ) {
            not_all_chk()
        }
    })

    $("#chk_agree2").change(function() {
        if (! $(this).is(":checked") ) {
            not_all_chk()
        }
    })

    $("#chk_agreeAll").change(function() {
        if ( $(this).is(":checked") ) {
            chk_agreeAll()
        } else {
            unchk_agreeAll()
        }
    })

    $("#btn_submit").click(function() {
        if ( check_validate() ) {
            return true
        }
        alert("약관에 동의 후, 회원가입이 가능합니다.")
        return false
    })
})