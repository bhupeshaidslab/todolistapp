function confirmDelete(event) {
    return window.confirm("Delete this reminder?");
}

function confirmClearCompleted(event) {
    return window.confirm("Remove all completed reminders?");
}

function initThemeToggle() {
    const toggle = document.getElementById("themeToggle");
    if (!toggle) return;

    const root = document.documentElement;
    const themeMeta = document.querySelector('meta[name="theme-color"]');

    function syncUi() {
        const isDark = root.dataset.theme === "dark";
        toggle.textContent = isDark ? "☀" : "◐";
        toggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
        if (themeMeta) {
            themeMeta.setAttribute("content", isDark ? "#000000" : "#f2f2f7");
        }
    }

    syncUi();

    toggle.addEventListener("click", () => {
        const isDark = root.dataset.theme === "dark";
        if (isDark) {
            delete root.dataset.theme;
            localStorage.setItem("taskflow-theme", "light");
        } else {
            root.dataset.theme = "dark";
            localStorage.setItem("taskflow-theme", "dark");
        }
        syncUi();
    });
}

function initFilterSheet() {
    const toggle = document.getElementById("filterToggle");
    const sheet = document.getElementById("filterSheet");
    if (!toggle || !sheet) return;

    toggle.addEventListener("click", () => {
        const open = sheet.hasAttribute("hidden");
        if (open) {
            sheet.removeAttribute("hidden");
            toggle.setAttribute("aria-expanded", "true");
        } else {
            sheet.setAttribute("hidden", "");
            toggle.setAttribute("aria-expanded", "false");
        }
    });

    if (
        sheet.querySelector('select[name="priority"]')?.value ||
        sheet.querySelector('select[name="category"]')?.value ||
        sheet.querySelector('select[name="label"]')?.value ||
        sheet.querySelector('select[name="sort"]')?.value !== "newest"
    ) {
        sheet.removeAttribute("hidden");
        toggle.setAttribute("aria-expanded", "true");
    }
}

function initSearchSubmit() {
    const form = document.getElementById("searchForm");
    if (!form) return;

    const input = form.querySelector('input[name="q"]');
    if (!input) return;

    let timer;
    input.addEventListener("input", () => {
        clearTimeout(timer);
        timer = setTimeout(() => form.requestSubmit(), 450);
    });
}

function initTaskSwipe() {
    const rows = document.querySelectorAll(".task-swipe");
    const deleteWidth = 88;

    rows.forEach((row) => {
        const content = row.querySelector(".task-swipe-content");
        if (!content) return;

        let startX = 0;
        let currentX = 0;
        let dragging = false;

        function setOffset(x) {
            const clamped = Math.max(-deleteWidth, Math.min(0, x));
            content.style.transform = `translateX(${clamped}px)`;
            currentX = clamped;
        }

        function snap() {
            if (currentX < -deleteWidth / 2) {
                setOffset(-deleteWidth);
            } else {
                setOffset(0);
            }
        }

        function onStart(clientX) {
            dragging = true;
            startX = clientX - currentX;
        }

        function onMove(clientX) {
            if (!dragging) return;
            setOffset(clientX - startX);
        }

        function onEnd() {
            if (!dragging) return;
            dragging = false;
            snap();
        }

        content.addEventListener("touchstart", (e) => onStart(e.touches[0].clientX), { passive: true });
        content.addEventListener("touchmove", (e) => onMove(e.touches[0].clientX), { passive: true });
        content.addEventListener("touchend", onEnd);

        content.addEventListener("mousedown", (e) => {
            if (e.target.closest("button, a, input, select, textarea")) return;
            onStart(e.clientX);
        });
        window.addEventListener("mousemove", (e) => onMove(e.clientX));
        window.addEventListener("mouseup", onEnd);

        document.addEventListener("click", (e) => {
            if (!row.contains(e.target) && currentX !== 0) {
                setOffset(0);
            }
        });
    });
}

window.addEventListener("DOMContentLoaded", () => {
    initThemeToggle();
    initFilterSheet();
    initSearchSubmit();
    initTaskSwipe();

    const toasts = document.querySelectorAll(".toast");
    if (!toasts.length) return;

    setTimeout(() => {
        toasts.forEach((toast) => toast.classList.add("hide"));
    }, 2600);
});
