function myFunction1() {
	var csrf_token = $('meta[name="csrf-token"]').attr("content");
	var userid = $("#to").val();
	var urls = "/publish/do_publish/"
	
    $("ol").empty();
    $("ol").append(`<marquee direction="right" scrollamount="55" loop="1"><img src="/static/img/account/bike.png"></img></marquee>`);
	$.ajax({
        type: "POST",
        url: urls,
        data: {
            csrfmiddlewaretoken : csrf_token,
            userid : userid,
            amount : 900
        },
        dataType : "json",
        async: true,
    }).done( function(data) {
        setTimeout(function(){ alert("행남코스를 완주하셨습니다. 900 RC가 발행되었습니다."); }, 1800);
    });
}

function myFunction2() {
	var csrf_token = $('meta[name="csrf-token"]').attr("content");
	var userid = $("#to").val();
	var urls = "/publish/do_publish/"
	
    $("ol").empty();
    $("ol").append(`<marquee direction="right" scrollamount="40" loop="1"><img src="/static/img/account/bike.png"></img></marquee>`);
	$.ajax({
        type: "POST",
        url: urls,
        data: {
            csrfmiddlewaretoken : csrf_token,
            userid : userid,
            amount : 1100
        },
        dataType : "json",
        async: true,
    }).done( function(data) {
        setTimeout(function(){ alert("내수전-석포코스를 완주하셨습니다. 1100 RC가 발행되었습니다."); }, 2500);
    });
}

function myFunction3() {
	var csrf_token = $('meta[name="csrf-token"]').attr("content");
	var userid = $("#to").val();
	var urls = "/publish/do_publish/"
	
    $("ol").empty();
    $("ol").append(`<marquee direction="right" scrollamount="30" loop="1"><img src="/static/img/account/bike.png"></img></marquee>`);
	$.ajax({
        type: "POST",
        url: urls,
        data: {
            csrfmiddlewaretoken : csrf_token,
            userid : userid,
            amount : 1200
        },
        dataType : "json",
        async: true,
    }).done( function(data) {
        setTimeout(function(){ alert("남양-태하코스를 완주하셨습니다. 1200 RC가 발행되었습니다."); }, 3400);
    });
}

function myFunction4() {
	var csrf_token = $('meta[name="csrf-token"]').attr("content");
	var userid = $("#to").val();
	var urls = "/publish/do_publish/"
	
    $("ol").empty();
    $("ol").append(`<marquee direction="right" scrollamount="100" loop="1"><img src="/static/img/account/bike.png"></img></marquee>`);
	$.ajax({
        type: "POST",
        url: urls,
        data: {
            csrfmiddlewaretoken : csrf_token,
            userid : userid,
            amount : 300
        },
        dataType : "json",
        async: true,
    }).done( function(data) {
        setTimeout(function(){ alert("대풍감코스를 완주하셨습니다. 300 RC가 발행되었습니다."); }, 1000);
    });
}