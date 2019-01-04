
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
            var type = ['발행', '결제', '결제취소', '송금', '송금취소', '계좌발급'];
            var exp1 = ['님으로부터', '에서', '님이', '에서', '님이', '에게', '으로부터', '에게', '으로부터', '', '으로부터'];
            var exp2 = ['받음', '보냄'];
            var seq = res["fullLength"];
            var css = ['cancelado', 'pendiente', 'pendiente', 'pagado', 'pagado', ''];
            var current_page_num = parseInt(res['current_page_num']);
            var max_page_num = parseInt(res['max_page_num']);

            $("#history").empty();
            res['history_list'].forEach(function(data) {
                var idx = Math.floor((parseInt(data.txType)+1)/2);
                var text = `
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
                                        <span class="${css[idx]}">${type[idx]}</span>
                                        <span class="pull-right">잔액: ${(data.balance).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</span>
                                    </h4>
                                    <p class="summary">${data.trader}${exp1[parseInt(data.txType)]} ${(data.amount).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")} RC ${type[idx]}</p>
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
            if ( data.status == "w" ) {
                $("#btn_qr").hide();
            }
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
    var userid = $("#u_id").val();
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
        if ( res['board_list'] ) {
            let seq = res["start_seq"]
            var current_page_num = parseInt(res['current_page_num']);
            var max_page_num = parseInt(res['max_page_num']);
            $("#myboard").empty();
            res['board_list'].forEach(function(data) {
                text = `
                    <tr>
                        <td>${seq--}</td>
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


function remove_store() {
    alert(1);
    $("#del_form").submit();
}


function openQRCamera(node) {
    var reader = new FileReader();
    var url = "";
    reader.onload = function() {
        node.value = "";
        qrcode.callback = function(res) {
            if(res instanceof Error) {
                alert("QR code를 찾을 수 없습니다. 다시 시도해주세요.");
            } else {
                //node.parentNode.previousElementSibling.value = res;
                url = res;
                window.location.replace(url);
            }
        };
        qrcode.decode(reader.result);
    };
    reader.readAsDataURL(node.files[0]);
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

    $("#btn_submit").on("click", function() {
        remove_store();
    });
})
