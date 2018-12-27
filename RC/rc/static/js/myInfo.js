
function get_history() {
    var from_id = $("#from").val();
    var urls = "http://210.107.78.166:8000/get_txList/"+from_id
    console.log(from_id,urls)
    $.ajax({
        type: "GET",
        url: urls,
        dataType : "json",
        async: false,
        success:function(data) {
            console.log(data);
        }
    })
    
}

$(function() {
    get_history();
    
    $('.ckbox label').on('click', function () {
        $(this).parents('tr').toggleClass('selected');
    });
    $('.btn-filter').on('click', function () {
        var $target = $(this).data('target');
        $('input[name=filter]').val($target);
        <!--$('form').submit();-->
        if ($target != 'all') {
            $('.table tr').css('display', 'none');
            $('.table tr[data-status="' + $target + '"]').fadeIn('slow');
        } else {
            $('.table tr').css('display', 'none').fadeIn('slow');
        }
    });
})


