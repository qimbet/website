

function setupSidebarToggle(container) {
    const sidebar = container.querySelector(":scope #sidebar");
    const tab = container.querySelector(":scope #sidebar-tab");
    const overlay = container.querySelector(":scope #sidebar-overlay");

    if (!sidebar || !tab || !overlay) return;

    tab.addEventListener("click", () => {
        sidebar.classList.toggle("open");
        overlay.classList.toggle("active");
        tab.classList.toggle("open");
    });

    overlay.addEventListener("click", () => {
        sidebar.classList.remove("open");
        overlay.classList.remove("active");
        tab.classList.remove("open");
    });
}

function getCurrentPage() {
    let path = window.location.pathname;

    if (path.endsWith("/")) {
        path = path.slice(0, -1);
    }

    const last = path.split("/").pop();

    return last || "index.html";
}

function highlightCurrentPage(container) {
    const current = getCurrentPage();

    container.querySelectorAll("#sidebar a").forEach(link => {
        const href = link.getAttribute("href")?.split("/").pop();

        if (href === current) {
            link.classList.add("active");
        }
    });
}

function lockActiveSectionsOpen(container) {
    container.querySelectorAll("#sidebar a.active")
        .forEach(activeLink => {
            let section = activeLink.closest(".section");

            while (section && container.contains(section)) {
                const checkbox = section.querySelector('input[type="checkbox"]');

                if (checkbox) {
                    checkbox.checked = true;
                    checkbox.disabled = true;
                }

                section = section.parentElement?.closest(".section");
            }
        });
}

export function initSidebar() {
    const container = document.getElementById("sidebar-container");

    if (!container) return;

    setupSidebarToggle(container);
    highlightCurrentPage(container);
    lockActiveSectionsOpen(container);
}

initSidebar();