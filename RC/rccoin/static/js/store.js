function setStore() {
    var oh = $("#myOpening_hour").val();
    if ( oh == "None" ) {
        $("#name").attr("value", "");
        $("#corporate_number").attr("value", "");
        $("#url").attr("value", "");
        $("#phone_number").attr("value", "");
        $("#address").attr("value", "");
        $("#description").attr("value", "");
    }
}

function setCategory() {
    var categoryList = JSON.parse($("#categoryList").val())
    categoryList["category_list"].forEach(function(category) {
        $("#category").append(`<option value="${category.id}">${category.domain}</option>`)
    })
    $("#category option:eq(0)").prop("selected", true)

    // 내 가맹점 정보로 셋팅
    var myCategory = $("#myCategory").val();
    if( myCategory != null && myCategory != "") {
        $("#category").val(myCategory).prop("selected", true);
    }
}

function setLocation() {
    var locationList = JSON.parse($("#locationList").val())

    locationList["location_list"].forEach(function(location) {
        $("#location").append(`<option value="${location.id}">${location.loc}</option>`)
    })
    $("#location option:eq(0)").prop("selected", true)

    // 내 가맹점 정보로 셋팅
    var myLocation = $("#myLocation").val();
    if( myLocation != null && myLocation != "") {
        $("#location").val(myLocation).prop("selected", true);
    }
}

function setTime() {
    for( var i=0; i<24; i++ ) {
        var ii = i >= 10 ? i : '0' + i.toString()
        var option = '<option value="' + ii + '">' + ii + '</option>'
        $("#opening_hour").append(option)
        $("#closing_hour").append(option)
    }

    for( var i=0; i<60; i++ ) {
        var ii = i >= 10 ? i : '0' + i.toString()
        var option = '<option value="' + ii + '">' + ii + '</option>'
        $("#opening_minute").append(option)
        $("#closing_minute").append(option)
    }

    // 내 가맹점 정보로 셋팅
    var myOpening_hour = $("#myOpening_hour").val();
    var myOpening_minute = $("#myOpening_minute").val();
    var myClosing_hour = $("#myClosing_hour").val();
    var myClosing_minute = $("#myClosing_minute").val();
    if( myOpening_hour != "None") {
        $("#opening_hour").val(myOpening_hour).prop("selected", true);
        $("#opening_minute").val(myOpening_minute).prop("selected", true);
        $("#closing_hour").val(myClosing_hour).prop("selected", true);
        $("#closing_minute").val(myClosing_minute).prop("selected", true);
    } else {
        $("#opening_hour").val("00").prop("selected", true)
        $("#opening_minute").val("00").prop("selected", true)
        $("#closing_hour").val("00").prop("selected", true)
        $("#closing_minute").val("00").prop("selected", true)
    }
}

function chk_validate() {
    var name = $("#name").val()
    var corporate_number = $("#corporate_number").val()
    var description = $("#description").val()
    var image = $("#image").val()
    var pattern = /^\d{3}-\d{2}-\d{5}$/
    var msg = ""
    if( name == "" ) {
        msg = "상호명을 입력해주세요."
    } else if( corporate_number == "" ) {
        msg = "사업자등록번호를 입력해주세요."
    } else if( !corporate_number.match(pattern) ) {
        $("#corporate_number").focus()
        msg = "사업자등록번호 형식이 올바르지 않습니다. 'ex) 123-12-12345'"
    } else if( image == "" ) {
        msg = "가맹점 사진을 등록하세요."
    } else if( description == "" ) {
        msg = "가맹점 설명을 입력해주세요."
    } else {
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

$(function() {
    setStore()
    setCategory()
    setLocation()
    setTime()
})