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

// Sidebar toggle
document.addEventListener("DOMContentLoaded", function () {
    console.log('Listening');
    let sidebar = document.getElementById("layoutSidenav_nav");
    let sidebarToggle = document.getElementById("sidebarToggle");
    let closeSidebar = document.getElementById("closeSidebar");

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", function () {
            console.log('Open');
            sidebar.classList.toggle("open");
        });
    }

    if (closeSidebar && sidebar) {
        closeSidebar.addEventListener("click", function () {
            sidebar.classList.remove("open");
        });
    }

    document.addEventListener("click", function (event) {
        if (
            sidebar &&
            !sidebar.contains(event.target) &&
            sidebarToggle &&
            !sidebarToggle.contains(event.target)
        ) {
            sidebar.classList.remove("open");
        }
    });

    // Alert timeout & progress bar
    const ALERT_TIMEOUT = 4000;
    const alerts = document.querySelectorAll('.messages-container .alert');

    alerts.forEach(function (alert) {
        const progressBar = alert.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.transition = `width ${ALERT_TIMEOUT}ms linear`;
            progressBar.style.width = '0%';
        }

        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, ALERT_TIMEOUT);
    });
});
