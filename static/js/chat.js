$(document).ready(function() {
    $('#text').keydown(function(e) {
        // Nếu người dùng nhấn Enter mà không giữ Shift
        if (e.keyCode === 13 && !e.shiftKey) {
            e.preventDefault(); // Ngăn không cho xuống dòng
            $('#messageArea').submit(); // Gửi form
        }
        // Không cần xử lý gì đặc biệt cho trường hợp Shift+Enter
    });

    $("#messageArea").on("submit", function(event) {
        const date = new Date();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const str_time = hour+":"+minute;
        var rawText = $("#text").val();
        var selectedModel = $("#modelSelect").val();
        var selectDocument = $("#documentSelect").val();

        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send"><pre>' + rawText + '</pre><span class="msg_time_send">' + str_time + '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';
        $("#text").val("");
        $("#messageFormeight").append(userHtml);
        scrollToBottom();
        $.ajax({
            data: {
                msg: rawText,
                model: selectedModel,
                document: selectDocument
            },
            type: "POST",
            url: "/get",
            contentType: "application/x-www-form-urlencoded", // Đặt kiểu dữ liệu của yêu cầu thành form data
        }).done(function(data) {
            var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer"><pre>' + data + '</pre><span class="msg_time">' + str_time + '</span></div></div>';
            $("#messageFormeight").append($.parseHTML(botHtml));
            scrollToBottom();
        });
        event.preventDefault();
    });

    function scrollToBottom() {
    var messages = $("#messageFormeight");
    messages.scrollTop(messages[0].scrollHeight);
    }
});



$(document).ready(function() {
    // Xử lý sự kiện click cho nút Tải lên
    $('#uploadButton').on('click', function() {
        console.log('Nút Tải lên được click');

        var fileInput = document.getElementById('fileInput');
        var file = fileInput.files[0];
        if (!file) {
            alert("Vui lòng chọn một file để tải lên.");
            return;
        }

        var formData = new FormData();
        formData.append('file', file);
        // Thêm trường 'user_name' vào formData
        var userName = '';
        formData.append('user_name', userName);

        fetch('/upload', {
            method: 'PUT', // Hoặc 'POST', tùy thuộc vào cấu hình server của bạn
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert('Tải lên thành công!');
        })
        .catch(error => {
            console.error('Lỗi khi tải lên:', error);
            alert('Lỗi khi tải lên.');
        });
    });
}
);





