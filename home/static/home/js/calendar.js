// Cập nhật thời gian hiện tại
function updateTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2,'0');
    const minutes = now.getMinutes().toString().padStart(2,'0');
    const seconds = now.getSeconds().toString().padStart(2,'0');
    document.getElementById('current-time').textContent = `${hours}:${minutes}:${seconds}`;

    // Cập nhật ngày hôm nay
    const todayElems = document.querySelectorAll('.calendar-cell.today');
    todayElems.forEach(el => el.classList.remove('today')); // bỏ highlight cũ

    const dayCells = document.querySelectorAll('.calendar-cell');
    dayCells.forEach(el => {
        const dayId = el.id.replace('day-', '');
        const cellDate = new Date(dayId);
        if (cellDate.toDateString() === now.toDateString()) {
            el.classList.add('today');
        }
    });
}

// Cuộn đến ngày hôm nay khi bấm nút
document.getElementById('today-btn').addEventListener('click', function() {
    const todayElem = document.querySelector('.calendar-cell.today');
    if(todayElem) {
        todayElem.scrollIntoView({ behavior: 'smooth', block: 'center' });
        todayElem.style.boxShadow = '0 0 15px 3px rgba(0,122,255,0.7)';
        setTimeout(()=>{ todayElem.style.boxShadow='0 3px 6px rgba(0,0,0,0.1)'; }, 1500);
    }
});

// Cập nhật thời gian & ngày hôm nay mỗi giây
setInterval(updateTime, 1000);
updateTime();