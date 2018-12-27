
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
            console.log(res);
            let type = ['발행', '결제', '결제', '결제취소', '결제취소', '송금', '송금', '송금취소', '송금취소']
            let seq = res.length;
            let text = '';
            let trader
            let amount
            let txType
            
            res.forEach(function(data) {

            })
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


