// Lấy CSRF token từ cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Hàm gọi fetch để đăng ký khóa học
function confirmRegister(courseId) {
    if (!confirm("Bạn có chắc chắn muốn đăng ký khóa học này?")) return;

    fetch(`/home/register-course/${courseId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    })
    .then(data => {
        alert(data.message);
        if (data.success) location.reload(); // Reload để card MyCourse hiển thị thông tin mới
    })
    .catch(error => {
        alert("Lỗi khi gửi request: " + error);
    });
}
