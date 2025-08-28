const searchInput = document.getElementById('search-input');
const filterSelect = document.getElementById('filter-type');
const markAllBtn = document.getElementById('mark-all-read');
const toggleThemeBtn = document.getElementById('toggle-theme');
const notificationCards = document.querySelectorAll('.notification-card');

const modal = document.getElementById('notificationModal');
const modalTitle = document.getElementById('modal-title');
const modalBody = document.getElementById('modal-body');
const modalTime = document.getElementById('modal-time');
const closeModal = modal.querySelector('.close');
const toast = document.getElementById('toast');

// Filter notifications
function filterNotifications() {
    const query = searchInput.value.toLowerCase();
    const filter = filterSelect.value;
    
    notificationCards.forEach(card => {
        const title = card.querySelector('.notification-title').textContent.toLowerCase();
        const body = card.querySelector('.notification-body').textContent.toLowerCase();
        const isNew = card.classList.contains('new');

        const matchesSearch = title.includes(query) || body.includes(query);
        const matchesFilter = filter === 'all' || (filter === 'new' && isNew) || (filter === 'read' && !isNew);

        card.style.display = matchesSearch && matchesFilter ? 'flex' : 'none';
    });
}

searchInput.addEventListener('input', filterNotifications);
filterSelect.addEventListener('change', filterNotifications);

// Mark all read
markAllBtn.addEventListener('click', () => {
    notificationCards.forEach(card => card.classList.remove('new'));
    showToast('Đã đánh dấu tất cả thông báo là đã đọc');
});

// Toggle dark mode
toggleThemeBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
});

// Open modal on click
notificationCards.forEach(card => {
    card.addEventListener('click', () => {
        modalTitle.textContent = card.querySelector('.notification-title').textContent;
        modalBody.textContent = card.querySelector('.notification-body').textContent;
        modalTime.textContent = card.querySelector('.notification-time').textContent;
        modal.style.display = 'flex';
        card.classList.remove('new'); // mark as read
    });
});

// Close modal
closeModal.addEventListener('click', () => modal.style.display = 'none');
window.addEventListener('click', e => {
    if (e.target === modal) modal.style.display = 'none';
});

// Toast function
function showToast(message) {
    toast.textContent = message;
    toast.style.opacity = 1;
    toast.style.transform = 'translateY(0)';
    setTimeout(() => {
        toast.style.opacity = 0;
        toast.style.transform = 'translateY(20px)';
    }, 2500);
}

// Mock realtime notifications
function addNotification(title, content) {
    const newCard = document.createElement('div');
    newCard.className = 'notification-card new';
    newCard.innerHTML = `
        <div class="notification-icon">
            <img src="/static/home/images/notification.png" alt="icon">
            <span class="badge">Mới</span>
        </div>
