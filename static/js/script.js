document.addEventListener("DOMContentLoaded", () => {
    const header    = document.querySelector("header");
    const mobileNav = document.getElementById("mobile-nav");
    const hamburger = document.querySelector(".hamburger");
    const overlay   = document.querySelector(".nav-overlay");
    const allLinks  = document.querySelectorAll("#desktop-nav a, #mobile-nav a");

    // ── 1. Sticky Header ──────────────────────────────────────
    window.addEventListener("scroll", () => {
        header.classList.toggle("scrolled", window.scrollY > 50);
    });
    header.classList.toggle("scrolled", window.scrollY > 50);

    // ── 2. Hamburger Menu ─────────────────────────────────────
    function openNav() {
        mobileNav.classList.add("open");
        hamburger.classList.add("open");
        overlay.classList.add("open");
        document.body.style.overflow = "hidden";
    }

    function closeNav() {
        mobileNav.classList.remove("open");
        hamburger.classList.remove("open");
        overlay.classList.remove("open");
        document.body.style.overflow = "";
    }

    if (hamburger) {
        hamburger.addEventListener("click", () => {
            mobileNav.classList.contains("open") ? closeNav() : openNav();
        });
    }

    if (overlay) overlay.addEventListener("click", closeNav);

    // ── 3. Scroll Reveal ─────────────────────────────────────
    const revealEls = document.querySelectorAll(".reveal, .stat-item");
    const observer  = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

    revealEls.forEach(el => observer.observe(el));

    // ── 4. Highlight active nav link ─────────────────────────
    const path = window.location.pathname;
    allLinks.forEach(link => {
        link.classList.remove("active");
        const href = link.getAttribute("href");
        if (href === path || (path === "/" && href && href.includes("home"))) {
            link.classList.add("active");
        }
    });
});
