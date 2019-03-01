function openQRCamera(node) {
    var reader = new FileReader();
    var url = "";
    reader.onload = function() {
        node.value = "";
        qrcode.callback = function(res) {
            if(res instanceof Error) {
                alert("QR코드를 읽는데 실패했습니다. 다시 시도해주세요.");
            } else {
                //node.parentNode.previousElementSibling.value = res;
                url = res;
                window.location.replace(url);
            }
        };
        qrcode.decode(reader.result);
    };
    reader.readAsDataURL(node.files[0]);
}
