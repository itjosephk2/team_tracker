console.log("✅ scripts.js is loaded and running!");

document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ DOM is fully loaded!");

    let sidebar = document.getElementById("layoutSidenav_nav");
    let sidebarToggle = document.getElementById("sidebarToggle");
    let closeSidebar = document.getElementById("closeSidebar");

    console.log("sidebar:", sidebar);
    console.log("sidebarToggle:", sidebarToggle);
    console.log("closeSidebar:", closeSidebar);

    if (sidebar && sidebarToggle && closeSidebar) {
        sidebarToggle.addEventListener("click", function () {
            console.log("➡️ Sidebar toggle clicked!");
            sidebar.classList.toggle("open");
        });

        closeSidebar.addEventListener("click", function () {
            console.log("➡️ Sidebar close button clicked!");
            sidebar.classList.remove("open");
        });

        document.addEventListener("click", function (event) {
            if (!sidebar.contains(event.target) && !sidebarToggle.contains(event.target)) {
                console.log("➡️ Clicked outside, closing sidebar.");
                sidebar.classList.remove("open");
            }
        });
    } else {
        console.error("❌ Sidebar elements not found. Check IDs in HTML.");
    }
});
