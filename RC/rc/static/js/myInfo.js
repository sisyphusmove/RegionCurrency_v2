
function get_history() {
    var from = $("#from").val();
    var urls = "http://210.107.78.166:8000/get_txList/" + from
    console.log(from,urls)
    $.ajax({
        type: "GET",
        url: urls,
        dataType : "json"
    }).done( function(res) {
        if ( res ) {
            res.reverse();
            let type = ['발행', '결제', '결제', '결제', '결제', '송금', '송금', '송금', '송금', '','계좌생성']
            let seq = res.length;
            res.forEach(function(data) {
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
        }
    });
}

function get_myStore(this_page) {
    var userid = $("#user").val();
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
                var status = (data.status) == "a" ? '승인됨' : ((data.status == "w") ? "승인대기" : "삭제됨");
                text = `
                    <tr>
                        <td><a href="/store/read/${data.id}/">${start_seq--}</a></td>
                        <td><a href="/store/read/${data.id}/">${data.name}</a></td>
                        <td><a href="/store/read/${data.id}/">${data.category}</a></td>
                        <td><a href="/store/read/${data.id}/">${data.location}</a></td>
                        <td><a href="/store/read/${data.id}/">${data.registered_date}</a></td>
                        <td><a href="/store/read/${data.id}/">${status}</a></td>
                        <td><a href="/store/delete/${data.id}/">삭제</a></td>
                    </tr>
                    `
                $("#myStoreList").append(text);
            });
            $("#page-area").empty();
            if (current_page_num != 1) {
                $("#page-area").append(`<a onclick="get_myStore(${1})" style="cursor: pointer;">\<\<</a>`);
            }
            if (current_page_num - 3 > 1) {
                $("#page-area").append(`...`);    
            }
            for (let i = current_page_num-3 ; i <= current_page_num+3; i++) {
                if (i > 0 && i <= max_page_num) {
                    if (i == current_page_num) {
                        $("#page-area").append(` '${i}' `);        
                    } else {
                        $("#page-area").append(`<a onclick="get_myStore(${i})" style="cursor: pointer;">${i}</a>`);
                    }
                }
            }
            if (current_page_num + 3 < max_page_num) {
                $("#page-area").append(`...`);    
            }
            if (current_page_num != max_page_num) {
                $("#page-area").append(`<a onclick="get_myStore(${max_page_num})" style="cursor: pointer;">\>\></a>`);
            }
        }
    });
}

$(function() {
    get_history();
    
    $("#myHistory-tab").on('click', function () {
        get_history();
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


