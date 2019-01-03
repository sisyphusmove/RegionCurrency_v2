
function get_history(this_page, query_type) {
    var from = $("#from").val();
    var urls = "/payment/get_history/"
    $.ajax({
        type: "GET",
        url: urls,
        data: {
            fro : from,
            this_page : this_page,
            type : query_type
        },
        dataType : "json"
    }).done( function(res) {
        if ( res['history_list'] ) {
            let type = ['발행', '결제', '결제', '결제취소', '결제취소', '송금', '송금', '송금취소', '송금취소', '','계좌생성']
            let seq = res["fullLength"]
            var current_page_num = parseInt(res['current_page_num']);
            var max_page_num = parseInt(res['max_page_num']);
            $("#history").empty();
            res['history_list'].forEach(function(data) {
                let exp1;
                let exp2;
                let text;

                if( data.txType == 0 || data.txType % 2 == 0) {
                    exp1 = '으로부터';
                    exp2 = '받음';
                } else {
                    exp1 = '에게'
                    exp2 = '보냄';
                }
            
                text = `
                <tr data-status="${type[data.txType]}">
                    <td>
                        <div class="ckbox">
                            ${seq--}
                        </div>
                    </td>
                    <td>
                        <a href="javascript:;" class="star">
                            <i class="glyphicon glyphicon-star"></i>
                        </a>
                    </td>
                    <td>
                        <div class="media">
                            <div class="media-body">
                                <span class="media-meta pull-right">${data.date}</span>
                                <h4 class="title">
                                    ${data.trader}
                                    <span class="pull-right ${type[data.txType]}">${type[data.txType]}</span>
                                </h4>
                                <p class="summary">${data.trader}님${exp1} ${data.amount} RC를 ${type[data.txType]}${exp2}</p>
                            </div>
                        </div>
                    </td>
                </tr>
                `;
                $("#history").append(text);
            });
            $("#page-area-2").empty();
            if (current_page_num != 1) {
                $("#page-area-2").append(`<li class="page-item"><a class="page-link" onclick="get_history(${1}, ${query_type})" style="cursor: pointer;">\<\<</a></li>`);
            }
            if (current_page_num - 2 > 1) {
                $("#page-area-2").append(`<li class="page-item"><a class="page-link">...</a></li>`);    
            }
            for (let i = current_page_num-2 ; i <= current_page_num+2; i++) {
                if (i > 0 && i <= max_page_num) {
                    if (i == current_page_num) {
                        $("#page-area-2").append(`<li class="page-item"><a class="page-link"><u>${i}</u></a></li>`);        
                    } else {
                        $("#page-area-2").append(`<li class="page-item"><a class="page-link" onclick="get_history(${i}, ${query_type})" style="cursor: pointer;">${i}</a></li>`);
                    }
                }
            }
            if (current_page_num + 2 < max_page_num) {
                $("#page-area-2").append(`<li class="page-item"><a class="page-link">...</a></li>`);    
            }
            if (current_page_num != max_page_num) {
                $("#page-area-2").append(`<li class="page-item"><a class="page-link" onclick="get_history(${max_page_num}, ${query_type})" style="cursor: pointer;">\>\></a></li>`);
            }
        }
        
    });
}

function get_myStore() {
    var u_id = $("#u_id").val();
    var urls = "/store/getMyStore"
    $.ajax({
        type: "GET",
        url: urls,
        data: { u_id : u_id },
        dataType : "json"
    }).done( function(data) {
        if ( data.name ) {
            status = (data.status == "a") ? "승인됨" : ((data.status == "w") ? "승인대기중" : "삭제됨");
            $("#btn_add").hide();
            $("#del_id").attr("value", data.id);
            $("#s_id").attr("value", data.id);
            $("#image").attr("src", data.photo);
            $("#store_name").text(data.name);
            $("#corp_num").text(data.corporate_number);
            $("#category").text(data.category);
            $("#location").text(data.location);
            $("#phone_num").text(data.phone_number);
            $("#url").text(data.url);
            $("#address").text(data.address);
            $("#registered_date").text(data.registered_date);
            $("#modified_date").text(data.modified_date);
            $("#opening_hours").text(data.opening_time + " ~ " + data.closing_time);
            $("#status").text(status);
        } else {
            $("#myStore").empty();
            $("#myStore").append(`<center>등록된 가맹점이 없습니다. <a href="/store/apply">[가맹점 신청하기]</a></center>`);
        }
    });
}

function get_myboard(this_page) {
    var userid = $("#userid").val();
    var urls = "/board/board_search/"
    $.ajax({
        type: 'GET',
        url: urls,
        dataType : 'json',
        data: {
            userid : userid,
            this_page : this_page
        },
    }).done(function(res) {
        if ( res['a'] ) {
            let seq = res["start_seq"]
            var current_page_num = parseInt(res['current_page_num']);
            var max_page_num = parseInt(res['max_page_num']);
            $("#myboard").empty();
            res['a'].forEach(function(data) {
                text = `
                    <tr>
                        <td>${data.id}</td>
                        <td style="max-width:500px"><a href="/board/read/${data.id}/" style="color:#000">${data.title}</a></td>
                        <td>${data.create_date}</td>
                        <td>${data.count}</td>
                    </tr>
                    `;
                    $("#myboard").append(text); 
            })
            $("#page-area-3").empty();
            if (current_page_num != 1) {
                $("#page-area-3").append(`<li class="page-item"><a class="page-link" onclick="get_myboard(1)" style="cursor: pointer;">\<\<</a></li>`);
            }
            if (current_page_num - 2 > 1) {
                $("#page-area-3").append(`<li class="page-item"><a class="page-link">...</a></li>`);    
            }
            for (let i = current_page_num-2 ; i <= current_page_num+2; i++) {
                if (i > 0 && i <= max_page_num) {
                    if (i == current_page_num) {
                        $("#page-area-3").append(`<li class="page-item"><a class="page-link"><u>${i}</u></a></li>`);        
                    } else {
                        $("#page-area-3").append(`<li class="page-item"><a class="page-link" onclick="get_myboard(${i})" style="cursor: pointer;">${i}</a></li>`);
                    }
                }
            }
            if (current_page_num + 2 < max_page_num) {
                $("#page-area-3").append(`<li class="page-item"><a class="page-link">...</a></li>`);    
            }
            if (current_page_num != max_page_num) {
                $("#page-area-3").append(`<li class="page-item"><a class="page-link" onclick="get_myboard(${max_page_num})" style="cursor: pointer;">\>\></a></li>`);
            }
        }
    });
}


function openQRCamera(node) {
    var reader = new FileReader();
    reader.onload = function() {
        node.value = "";
        qrcode.callback = function(res) {
            if(res instanceof Error) {
                alert("No QR code found. Please make sure the QR code is within the camera's frame and try again.");
            } else {
                node.parentNode.previousElementSibling.value = res;
                alert("a:"+res);
            }
        };
        qrcode.decode(reader.result);
    };
    reader.readAsDataURL(node.files[0]);
    alert(node.files[0]);
}


$(function() {
    get_history(1, 0);

    $("#myHistory-tab").on('click', function () {
        $("history").empty();
        get_history(1, 0);
    });

    $("#myStore-tab").on('click', function () {
        get_myStore();
    });

    $("#myBoard-tab").on('click', function () {
        get_myboard(1);
    });

    $('.ckbox label').on('click', function () {
        $(this).parents('tr').toggleClass('selected');
    });

    $('.btn-filter').on('click', function () {
        var $target = $(this).data('target');
        $('input[name=filter]').val($target);
        if ($target != 'all') {
            $('.table tr').css('display', 'none');
            $('.table tr[data-status="' + $target + '"]').fadeIn('slow');
        } else {
            $('.table tr').css('display', 'none').fadeIn('slow');
        }
    });
})
