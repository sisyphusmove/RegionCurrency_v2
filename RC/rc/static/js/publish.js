var modal1 = document.getElementById('myModal1');
var modal2 = document.getElementById('myModal2');
var modal3 = document.getElementById('myModal3');
var modal4 = document.getElementById('myModal4');
// Get the button that opens the modal
var btn = document.getElementById("myBtn");
var btn2 = document.getElementById("myBtn2");
var btn3 = document.getElementById("myBtn3");
var btn4 = document.getElementById("myBtn4");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close1")[0];
var span1 = document.getElementsByClassName("close2")[0];
var span2 = document.getElementsByClassName("close3")[0];
var span3 = document.getElementsByClassName("close4")[0];

// When the user clicks the button, open the modal 
// btn.onclick = function() {
//   modal.style.display = "block";
// }

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal1.style.display = "none";
}
span1.onclick = function() {
    modal2.style.display = "none";
}
span2.onclick = function() {
    modal3.style.display = "none";
}
span3.onclick = function() {
    modal4.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal1 ) {
    modal1.style.display = "none";
  }
  else if (event.tagget == modal2) {
    modal2.style.display = "none";
  }
  else if (event.tagget == modal3) {
    modal3.style.display = "none";
  }
    else if (event.tagget == modal4) {
    modal4.style.display = "none";
  }
}

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
        setTimeout(function() {
            modal1.style.display = "block";
          } , 1800);
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
        setTimeout( function() {
            modal2.style.display = "block";
          }, 2500);
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
        setTimeout(function() {
            modal3.style.display = "block";
          }, 3400);
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
        setTimeout(function() {
            modal4.style.display = "block";
          }, 1000);
    });
}