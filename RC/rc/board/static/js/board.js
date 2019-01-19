

function ctl_cookie(board_type){
    console.log("ctl cookie ########")
    var getCookie = function(name) {
      var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
      return value? value[2] : null;
    };
    var setCookie = function(name, value, exp) {
      var date = new Date();
      date.setTime(date.getTime() + exp*24*60*60*1000);
      document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
    };
    var deleteCookie = function(name) {
      document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
    deleteCookie('current_board')

    setCookie('current_board', board_type, 7)
    return getCookie('current_board')
}

function ctl_btn_by_board_type(board_type){
    if( board_type == 1 ){
        $("#btn_board_type_1").css({'background-color': 'white'})
        $("#btn_board_type_2").css({'background-color': 'white'})
        $("#btn_board_type_1").css({'background-color': '#71c55d'})
        $("#btn_board_type_1").css({'color': 'white'})
    }
    if( board_type == 2 ){
        $("#btn_board_type_1").css({'background-color': 'white'})
        $("#btn_board_type_2").css({'background-color': 'white'})
        $("#btn_board_type_2").css({'background-color': '#71c55d'})
        $("#btn_board_type_2").css({'color': 'white'})
    }
}

function btn_click_ctl(){

     $('.btn_board_type_1').on('click', function(){
        var board_type_for_cookie = $('#board_type_1').val()
        ctl_cookie(board_type_for_cookie)
    })

    $('.btn_board_type_2').on('click', function(){
        var board_type_for_cookie = $('#board_type_2').val()
        ctl_cookie(board_type_for_cookie)
    })

}

function chg_board(board_type, page){

        console.log(1234)
        ctl_cookie(board_type)

        var category = ''
        var keyword = ''

        if( $('#search_categoty option:selected').val() != "" &&  $('#search_categoty > option:selected').val() != undefined ){
            category = $('#search_categoty > option:selected').val()
        }
        if( $('.keyword').val() != "" &&  $('.keyword').val() != undefined ){
            keyword = $('.keyword').val()
        }

        $.ajax({
            type: 'GET',
            url: '/board/chg',
            data: {
                board_type : board_type,
                page : page,
                category : category,
                keyword : keyword
            },
            dataType : 'json',
            success: function(data) {
                if (board_type == 1){
                    console.log("가맹점 게시판")
                }
                else {
                    console.log("사용자 게시판")
                }

                html = ''
                html += '<section id="contact">'
                html += '    <div class="btn_write_area" style="background-color: white; background-color:67px;">'
                html += '     <select id="search_categoty" class="category" name="search_categoty" style="height: 30px; border: 1px solid #CCC;color:#777">'
                html += '       <option value="">전체</option>'
                html += '       <option value="writer">작성자</option>'
                html += '       <option value="title">제목</option>'
                html += '       <option value="content">게시글</option>'
                html += '     </select>'
                html += '    <input class="keyword" type="text" placeholder="검색어를 입력하세요. "'
                html += '    style="background-image:url(../../static/img/search.png);background-position-x: 2px; background-position-y: 1px; background-repeat: no-repeat;border:#CCC solid 1px;padding-left: 30px;">'
                
                html += '    <a class="btn btn_search" style="color:#fff" onclick="search_board_by_word()">찾기</a>'
                html += '    <a class="btn btn_write" href="/board/add" style="display: none; position: absolute; margin-top: -53px; right: 20%; background-color: #71c55d;">글쓰기</a>'
                html += '    </div>'
                html += '    <table class="table table-hover">'
                html += '    <thead>'
                html += '    <tr>'
                html += '    <th scope="col">번호</th>'
                html += '    <th scope="col">제목</th>'
                html += '    <th scope="col">작성자</th>'
                html += '    <th scope="col">날짜</th>'
                html += '    <th scope="col">조회수</th>'
                html += '    <th scope="col">추천</th>'
                html += '    </tr>'
                html += '    </thead>'
                html += '    <tbody>'
                for( var i=0; i<data.max_page; i++){
                    if( data.object[i] != null ){
                        html += "<tr class='tag_text'>"
                        html += "<th scope='row'>" + (data.start_index+i) + "</th>"
                        html += "<td><a href='" + data.object[i].get_absolute_url + "'>" + data.object[i].title + "</a></td>"
                        html += "<td>" +  data.object[i].writer + "</td>"
                        html += "<td>" + data.object[i].modify_date + "</td>"
                        html += "<td style='text-align: center'>" + data.object[i].count + "</td>"
                        html += "<td style='text-align: center'>" + data.object[i].recommend + "</td>"
                        html += "</tr>"
                    }else{
                        html += "<tr class='tag_text'>"
                        html += "<td>&nbsp;</td>"
                        html += "<td><a href=''>&nbsp;</a></td>"
                        html += "<td>&nbsp;</td>"
                        html += "<td>&nbsp;</td>"
                        html += "<td style='text-align: center'>&nbsp;</td>"
                        html += "<td style='text-align: center'>&nbsp;</td>"
                        html += "</tr>"
                    }
                }
                html += '        </tbody>'
                html += '        </table>'
                html += '        <nav aria-label="Page navigation" style="margin-left: 50%">'
                html += '        <ul class="pagination">'
                if( data.has_prev ){
                    html += '        <li class="page-item">'
                    html += '        <a class="page-link" onclick="chg_board(' + board_type + ',' + data.prev_page + ')" aria-label="Previous">'
                    html += '        <span aria-hidden="true">«</span>'
                    html += '        <span class="sr-only">Previous</span>'
                    html += '        </a>'
                    html += '        </li>'
                }
                for( var i=0; i<data.num_pages; i++){
                    if( data.current_page == (i+1) ){
                        html += '        <li class="active page-item"><a class="page-link">' + (i+1) + '</a></li>'
                    }else{
                        html += '        <li class="page-item"><a class="page-link" onclick="chg_board(' + board_type + ',' + (i+1) + ')">' + (i+1) + '</a></li>'
                    }
                }
                if( data.has_next ){
                    html += '        <li class="page-item">'
                    html += '        <a class="page-link" onclick="chg_board(' + board_type + ',' + data.next_page + ')" aria-label="Next">'
                    html += '        <span aria-hidden="true">»</span>'
                    html += '        <span class="sr-only">Next</span>'
                    html += '        </a>'
                    html += '        </li>'
                }
                html += '        </ul>'
                html += '        </nav>'
                html += '</section>'
                $('div.board_content').html(html)

                if( $('#user_type').val() != board_type ){
                    $('.btn_write').css('display', 'none')
                }else if( $('#user_type').val() == board_type ){
                    $('.btn_write').css('display', 'table')
                }

                ctl_btn_by_board_type(board_type)
            },
            error: function( jqXHR, textStatus, errorThrown ){
                    alert('status: ' + textStatus + '\nerror: ' + jqXHR.error )
            }
        })
    }

    function back_to_list(){

        var setCookie = function(name, value, exp) {
            var date = new Date();
            date.setTime(date.getTime() + exp*24*60*60*1000);
            document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
          };
          setCookie('from', "not_intro", 7)

    }