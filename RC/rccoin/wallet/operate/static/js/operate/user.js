$('.btn-example').click(function(){
    var $href = $(this).attr('href');
    var user_id = $(this).attr('id');
    var tag_name = ""
    tag_name = "tr#" + user_id + " > td";
    var alltag = []
    alltag = $(tag_name)
    var like = ''
    var board = ''
    
    $.ajax({
        type: 'GET',
        url: '/operate/get_like',
        data: {
            user_id : user_id
        },
        dataType : 'json',
        success: function(data) {
            
            like = data.like_cnt
            board = data.board_cnt
            $('.profile-usertitle-like').text(like)
            $('.profile-usertitle-board').text(board)
        }, 
        error: function( jqXHR, textStatus, errorThrown ){
                alert('status: ' + textStatus + '\nerror: ' + jqXHR.error )
        }
    })
    
    var username = alltag[0].innerHTML
    var email = alltag[1].innerHTML
    var gender = alltag[2].innerHTML
    var birth = alltag[3].innerHTML
    var type = alltag[4].innerHTML
    var status = alltag[5].innerHTML
  
    $('.profile-usertitle-name').text(username)
    $('.profile-usertitle-email').text(email)
    $('.profile-usertitle-gender').text(gender)
    $('.profile-usertitle-birth').text(birth)
    $('.profile-usertitle-type').text(type)
    $('.profile-usertitle-status').text(status)
    
    layer_popup($href);
});
function layer_popup(el){
    var $el = $(el);        //레이어의 id를 $el 변수에 저장
    var isDim = $el.prev().hasClass('dimBg');   //dimmed 레이어를 감지하기 위한 boolean 변수
    isDim ? $('.dim-layer').fadeIn() : $el.fadeIn();
    var $elWidth = ~~($el.outerWidth()),
        $elHeight = ~~($el.outerHeight()),
        docWidth = $(document).width(),
        docHeight = $(document).height();
    // 화면의 중앙에 레이어를 띄운다.
    if ($elHeight < docHeight || $elWidth < docWidth) {
        $el.css({
            marginTop: -$elHeight /2,
            marginLeft: -$elWidth/2
        })
    } else {
        $el.css({top: 0, left: 0});
    }
    $el.find('a.btn-layerClose').click(function(){
        isDim ? $('.dim-layer').fadeOut() : $el.fadeOut(); // 닫기 버튼을 클릭하면 레이어가 닫힌다.
        return false;
    });
    $('.layer .dimBg').click(function(){
        $('.dim-layer').fadeOut();
        return false;
    });
}