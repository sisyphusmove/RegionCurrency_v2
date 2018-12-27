
function get_history() {
    var from = $("#from").val();
    var urls = "http://210.107.78.166:8000/get_txList/" + from
    console.log(from,urls)
    $.ajax({
        type: "GET",
        url: urls,
        dataType : "json",
        async: false
    }).done( function(res) {
        if ( res ) {
            res.reverse();
            let type = ['발행', '결제', '결제', '결제', '결제', '송금', '송금', '송금', '송금', '계좌생성']
            let seq = res.length;
            
            res.forEach(function(data) {
                let exp1;
                let exp2;
                let text;
                
                if( data.txType == '' ) {
                    data.txType = 9;
                }

                if( data.txType == 0 || data.txType == 9 || data.txType % 2 == 0) {
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

$(function() {
    get_history();

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


