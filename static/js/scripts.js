document.addEventListener("DOMContentLoaded", function() {
    let sidebar = document.getElementById("layoutSidenav_nav");
    let sidebarToggle = document.getElementById("sidebarToggle");
    let closeSidebar = document.getElementById("closeSidebar");

    sidebarToggle.addEventListener("click", function() {
        sidebar.classList.toggle("open");
    });

    closeSidebar.addEventListener("click", function() {
        sidebar.classList.remove("open");
    });

    document.addEventListener("click", function(event) {
        if (!sidebar.contains(event.target) && !sidebarToggle.contains(event.target)) {
            sidebar.classList.remove("open");
        }
    });
});