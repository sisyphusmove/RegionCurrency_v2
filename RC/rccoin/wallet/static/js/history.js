function get_history(this_page, query_type) {
    var from = $("#from").val()
    var urls = "/wallet/history/"
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
        if ( res["history_list"] ) {
            var type = ["발행", "결제", "결제취소", "송금", "송금취소", "계좌발급"]
            var exp = ["님으로부터", "에서", "님이", "에서", "님이", "에게", "으로부터", "에게", "으로부터", "", "으로부터"]
            var css = ["publish", "payment", "remittance", "init"]
            var img = [
                "deposit.png",
                "withdraw.png", "deposit.png",
                "withdraw.png", "deposit.png",
                "withdraw.png", "deposit.png",
                "withdraw.png", "deposit.png",
                "", "wallet1.png"]
            var current_page_num = parseInt(res["current_page_num"])
            var max_page_num = parseInt(res["max_page_num"])
            
            $("#history").empty()
            res["history_list"].forEach(function(data) {
                var idx = Math.floor((parseInt(data.txType)+1)/2)
                var text = `<tr class="${css[Math.floor((parseInt(idx)+1)/2)]}">
                                <td>
                                    <div class="media">
                                        <a href="#" class="pull-left">
                                            <img src="../../static/img/${img[data.txType]}" class="media-photo d-none d-md-block">
                                        </a>
                                        <div class="media-body">
                                            <span class="media-meta pull-right">${data.date}</span>
                                            <span class="${css[Math.floor((parseInt(idx)+1)/2)]}">
                                                ${type[idx]}
                                            </span>
                                            <p class="summary"><font class="title">${data.trader}</font>${exp[parseInt(data.txType)]} <font class="title">${(data.amount).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")} RC</font>를 ${type[idx]}</p>
                                            <span class="pull-right title">잔액 : ${(data.balance).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}RC</span>
                                        </div>
                                    </div>
                                </td>
                            </tr>`
                $("#history").append(text)
            })
            $("#page-area").empty()
            if (current_page_num != 1) {
                $("#page-area").append(`<li class="page-item"><a class="page-link" onclick="get_history(${1}, ${query_type})" style="cursor: pointer">처음</a></li>`)
            }
            if (current_page_num - 2 > 1) {
                $("#page-area").append(`<li class="page-item"><a class="page-link">...</a></li>`)    
            }
            for (let i = current_page_num-2;  i <= current_page_num+2; i++) {
                if (i > 0 && i <= max_page_num) {
                    if (i == current_page_num) {
                        $("#page-area").append(`<li class="page-item"><a class="page-link"><u>${i}</u></a></li>`)        
                    } else {
                        $("#page-area").append(`<li class="page-item"><a class="page-link" onclick="get_history(${i}, ${query_type})" style="cursor: pointer">${i}</a></li>`)
                    }
                }
            }
            if (current_page_num + 2 < max_page_num) {
                $("#page-area").append(`<li class="page-item"><a class="page-link">...</a></li>`)    
            }
            if (current_page_num != max_page_num) {
                $("#page-area").append(`<li class="page-item"><a class="page-link" onclick="get_history(${max_page_num}, ${query_type})" style="cursor: pointer">끝</a></li>`)
            }
        }
        
    })
}

$(function() {
    get_history(1, 0)
})