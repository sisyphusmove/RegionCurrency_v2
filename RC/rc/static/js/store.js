function setStore() {
    var oh = $("#myOpening_hour").val();
    if ( oh == "None" ) {
        $("#myOpening_hour").attr("value", "");
        $("#name").attr("value", "");
        $("#corporate_number").attr("value", "");
        $("#url").attr("value", "");
        $("#phone_number").attr("value", "");
        $("#address").attr("value", "");
        $("#description").attr("value", "");
        $("#image").attr("value", "");
    }
}

function setCategory() {
    var myCategory = $("#myCategory").val();
    var categoryList = JSON.parse($("#categoryList").val());

    categoryList.forEach(function(category) {
        $("#category").append(`<option value="${category.id}">${category.domain}</option>`);
    });

    $("#category option:eq(0)").prop("selected", true);
    if( myCategory != null && myCategory != "") {
        $("#category").val(myCategory).prop("selected", true);
    }
}

function setLocation() {
    var myLocation = $("#myLocation").val();
    var locationList = JSON.parse($("#locationList").val());

    locationList.forEach(function(location) {
        $("#location").append(`<option value="${location.id}">${location.loc}</option>`);
    });
    $("#location option:eq(0)").prop("selected", true);
    if( myLocation != null && myLocation != "") {
        $("#location").val(myLocation).prop("selected", true);
    }
}

function setTime() {
    var myOpening_hour = $("#myOpening_hour").val();
    var myOpening_minute = $("#myOpening_minute").val();
    var myClosing_hour = $("#myClosing_hour").val();
    var myClosing_minute = $("#myClosing_minute").val();

    for( var i=0; i<24; i++ ) {
        var ii = i >= 10 ? i : '0' + i.toString();
        var option = '<option value="' + ii + '">' + ii + '</option>';
        $("#opening_hour").append(option);
        $("#closing_hour").append(option);
    }

    for( var i=0; i<60; i++ ) {
        var ii = i >= 10 ? i : '0' + i.toString();
        var option = '<option value="' + ii + '">' + ii + '</option>';
        $("#opening_minute").append(option);
        $("#closing_minute").append(option);
    }

    $("#opening_hour").val("00").prop("selected", true);
    $("#opening_minute").val("00").prop("selected", true);
    $("#closing_hour").val("00").prop("selected", true);
    $("#closing_minute").val("00").prop("selected", true);

    if( myOpening_hour ) {
        $("#opening_hour").val(myOpening_hour).prop("selected", true);
        $("#opening_minute").val(myOpening_minute).prop("selected", true);
        $("#closing_hour").val(myClosing_hour).prop("selected", true);
        $("#closing_minute").val(myClosing_minute).prop("selected", true);
    }
}

$(function() {
    setStore();
    setCategory();
    setLocation();
    setTime();

    $("#btn_submit").on("click", function(event) {
        var name = $("#name").val();
        var corporate_number = $("#corporate_number").val();
        var description = $("#description").val();
        var image = $("#image").val();
        var pattern = /^\d{3}-\d{2}-\d{5}$/;
        
        if( name == "" ) {
            alert("상호명을 입력해주세요.");
        } else if( corporate_number == "" ) {
            alert("사업자등록번호를 입력해주세요.");
        } else if( !corporate_number.match(pattern) ) {
            alert("사업자등록번호 형식이 올바르지 않습니다. 'ex) 111-11-11111'");
        } else if( image == "" ) {
            alert("가맹점 사진을 등록하세요.");
        } else if( description == "" ) {
            alert("가맹점 설명을 입력해주세요.");
        } else {
            $("#edit_form").submit();
        }

        return false;
    });
})