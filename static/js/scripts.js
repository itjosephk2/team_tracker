document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("layoutSidenav_nav");  
    const main = document.getElementById("layoutSidenav_content");
    // sidebar.classList.toggle("open");
        toggleBtn.addEventListener("click", function () {
        if (window.innerWidth <= 768) {
            sidebar.classList.toggle("open");
        } else {
            sidebar.classList.toggle("collapse");
            main.classList.toggle("expand");
        }
    });
});