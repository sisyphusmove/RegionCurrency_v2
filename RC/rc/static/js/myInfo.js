
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
        dataType : "json",
        async: true
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

function get_myStore(this_page) {
    var userid = $("#userid").val();
    var urls = "/store/getMyStore/"
    $.ajax({
        type: "GET",
        url: urls,
        data: {
            userid : userid,
            this_page : this_page
        },
        dataType : "json",
        async: true
    }).done( function(res) {
        if ( res['store_list'] ) {
            var current_page_num = parseInt(res['current_page_num']);
            var max_page_num = parseInt(res['max_page_num']);
            var start_seq = parseInt(res['start_seq']);
            var text = '';
            $("#myStoreList").empty();
            res['store_list'].forEach(function(data) {
                text = `
                    <tr data-status="pagado">
                        <td>
                            ${start_seq--}
                        </td>
                        <td>
                        </td>
                        <td>
                            <div class="media">
                                <div class="media-body">
                                    <span class="media-meta pull-right">${data.registered_date}</span>
                                    <h4 class="title">
                                        [${data.corporate_number}]&nbsp;${data.name}
                                        <span class="pull-right cancelado"><a href="/store/delete/${data.id}">삭제</a></span>
                                        <span class="pull-right primary"><a href="/store/read/${data.id}">상세보기</a></span>`;
                                    
                if (data.status == "a") {
                    text += `                    <span class="pull-right pagado">(승인)</span>`;
                } else if (data.status == "w") {
                    text += `                    <span class="pull-right pendiente">(승인대기)</span>`;
                }
                text += `           </h4>
                                    <p class="summary">등록지역&nbsp;:&nbsp;[${data.category}]&nbsp;,&nbsp;등록업종&nbsp;:&nbsp;[${data.location}]</p>
                                </div>
                            </div>
                        </td>
                    </tr>
                    `;
                $("#myStoreList").append(text);
            });
            $("#page-area").empty();
            if (current_page_num != 1) {
                $("#page-area").append(`<li class="page-item"><a class="page-link" onclick="get_myStore(${1})" style="cursor: pointer;">\<\<</a></li>`);
            }
            if (current_page_num - 2 > 1) {
                $("#page-area").append(`<li class="page-item"><a class="page-link">...</a></li>`);    
            }
            for (let i = current_page_num-2 ; i <= current_page_num+2; i++) {
                if (i > 0 && i <= max_page_num) {
                    if (i == current_page_num) {
                        $("#page-area").append(`<li class="page-item"><a class="page-link"><u>${i}</u></a></li>`);        
                    } else {
                        $("#page-area").append(`<li class="page-item"><a class="page-link" onclick="get_myStore(${i})" style="cursor: pointer;">${i}</a></li>`);
                    }
                }
            }
            if (current_page_num + 2 < max_page_num) {
                $("#page-area").append(`<li class="page-item"><a class="page-link">...</a></li>`);    
            }
            if (current_page_num != max_page_num) {
                $("#page-area").append(`<li class="page-item"><a class="page-link" onclick="get_myStore(${max_page_num})" style="cursor: pointer;">\>\></a></li>`);
            }
        }
    });
}

$(function() {
    get_history(1, 0);
    
    $("#myHistory-tab").on('click', function () {
        get_history(1, 0);
    });

    $("#myStore-tab").on('click', function () {
        get_myStore(1);
    });

    $('.ckbox label').on('click', function () {
        $(this).parents('tr').toggleClass('selected');
    });

    $('.btn-filter').on('click', function () {
        var $target = $(this).data('target');
        $('input[name=filter]').val($target);
        // $('form').submit();
        if ($target != 'all') {
            $('.table tr').css('display', 'none');
            $('.table tr[data-status="' + $target + '"]').fadeIn('slow');
        } else {
            $('.table tr').css('display', 'none').fadeIn('slow');
        }
    });
})


