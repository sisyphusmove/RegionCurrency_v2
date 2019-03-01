function make_form() {
    var url = "/store/list/filter/4/"
    var keyword = $("#keyword").val()
    if ( keyword == "None" | keyword.length < 1) {
        alert("검색어를 입력하세요.")
        return false
    } else {
        $("#searchform").prop("action", `${url}?keyword=${keyword}`)
        return true
    }
}