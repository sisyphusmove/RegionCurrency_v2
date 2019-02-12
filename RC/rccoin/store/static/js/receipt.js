function cancel(num) {
    var csrf_token = $('meta[name="csrf-token"]').attr("content")
    var url = "/wallet/cancel_payment/"
    var to = $(`data${num}`).attr("to")
    var amount = $(`data${num}`).attr("amount")
    var tx = $(`data${num}`).attr("tx")
    var form = $(`<form action="${url}" method="POST">` +
        `<input type="text" name="csrfmiddlewaretoken" value="${csrf_token}"/>` + 
        `<input type="text" name="to" value="${to}"/>` + 
        `<input type="text" name="amount" value="${amount}"/>` + 
        `<input type="text" name="tx" value="${tx}"/>` + 
        `</form>`)
    $("body").append(form)
    form.submit()
}

function get_receipt(this_page, option) {
    var urls = "/wallet/receipt/"
    $.ajax({
        type: "GET",
        url: urls,
        data: {
            this_page : this_page,
            option : option, 
        },
        dataType : "json"
    }).done( function(data) {
        if ( data["receipt_list"] ) {
            var type = ["결제", "결제취소"];
            var css = ["payment", "canceled"];
            var img = ["wallet1.png", "deposit.png", "withdraw.png"]
            var current_page_num = parseInt(data["current_page_num"]);
            var max_page_num = parseInt(data["max_page_num"]);
            var seq = 0
            $("#receipt").empty();
            data["receipt_list"].forEach(function(r) {
                seq++
                var idx = parseInt(r.txType) % 2;
                var text = `<tr class="${css[idx]}">
                                <td>
                                    <div class="media">
                                        <a href="#" class="pull-left">
                                            <img src="../../static/img/${img[r.txType-1]}" class="media-photo d-none d-md-block">
                                        </a>
                                        <div class="media-body">
                                            <span class="media-meta pull-right">${r.date}</span>
                                            <span class="${css[idx]}">
                                                ${type[idx]}
                                            </span>`
                if ( r.canceled ) {
                    text +=                 `<strike>`
                }
                text +=                     `<p class="summary"><font class="title">${r.trader}</font>님이 <font class="title">${r.amount} RC</font>를 결제</p>`
            
                if ( r.canceled ) {
                    text +=                 `</strike>`
                }
                if ( !r.canceled & r.txType == 2 ) {
                    text +=                 `<span class="pull-right btn btn-danger"><data${seq} to="${r.trader}" amount="${r.amount}" tx="${r.txHash}" onclick="cancel(${seq});">취소</span>`
                } else if ( r.canceled ) {
                    text +=                 `<span class="pull-right text-danger">결제취소 완료</span>`
                }
                text +=                 `</div>
                                    </div>
                                </td>
                            </tr>`
                $("#receipt").append(text)
            });
            
            $("#page-area").empty();
            if (current_page_num != 1) {
                $("#page-area").append(`<li class="page-item"><a class="page-link" onclick="get_receipt(${1})" style="cursor: pointer;">처음</a></li>`);
            }
            if (current_page_num - 2 > 1) {
                $("#page-area").append(`<li class="page-item"><a class="page-link">...</a></li>`);    
            }
            for (let i = current_page_num-2 ; i <= current_page_num+2; i++) {
                if (i > 0 && i <= max_page_num) {
                    if (i == current_page_num) {
                        $("#page-area").append(`<li class="page-item"><a class="page-link"><u>${i}</u></a></li>`);        
                    } else {
                        $("#page-area").append(`<li class="page-item"><a class="page-link" onclick="get_receipt(${i})" style="cursor: pointer;">${i}</a></li>`);
                    }
                }
            }
            if (current_page_num + 2 < max_page_num) {
                $("#page-area").append(`<li class="page-item"><a class="page-link">...</a></li>`);    
            }
            if (current_page_num != max_page_num) {
                $("#page-area").append(`<li class="page-item"><a class="page-link" onclick="get_receipt(${max_page_num})" style="cursor: pointer;">끝</a></li>`);
            }
        }
        
    });
}

$(function() {
    get_receipt(1, 0)
})