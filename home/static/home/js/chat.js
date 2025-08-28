const sendBtn = document.getElementById('send-btn');
const input = document.getElementById('message-input');
const messagesContainer = document.getElementById('chat-messages');

sendBtn.addEventListener('click', sendMessage);
input.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    // Tin nhắn người dùng
    addMessage(text, 'user');

    input.value = '';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Tin nhắn trợ lý ảo giả lập
    setTimeout(() => {
        const reply = generateReply(text);
        addMessage(reply, 'assistant', true);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 500);
}

function addMessage(text, sender, highlight = false) {
    const msg = document.createElement('div');
    msg.classList.add('chat-message', sender);
    if (highlight) msg.classList.add('new-message');
    msg.innerHTML = `<p>${text}</p>`;
    messagesContainer.appendChild(msg);

    if (highlight) {
        setTimeout(() => msg.classList.remove('new-message'), 1500);
    }
}

// Hàm tạo trả lời giả lập
function generateReply(userText) {
    // Bạn có thể kết nối API AI thực ở đây
    return `Bạn vừa hỏi: "${userText}" 🤖`;
}
