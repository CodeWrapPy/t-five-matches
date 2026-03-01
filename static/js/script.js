document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector("header");
    const navLinks = document.querySelectorAll("nav a");
    const revealElements = document.querySelectorAll(".reveal, .stat-item, .service-card, .card");

    // --- 1. Dynamic Header Logic ---
    const handleHeader = () => {
        // Adds 'scrolled' class after 50px of scrolling for the shrink effect
        if (window.scrollY > 50) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }
    };

    // --- 2. Scroll-Reveal Logic (Intersection Observer) ---
    const revealOptions = {
        threshold: 0.15, // Element must be 15% visible to trigger
        rootMargin: "0px 0px -50px 0px"
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("active");
                // Stop observing once the animation has played
                observer.unobserve(entry.target);
            }
        });
    }, revealOptions);

    // --- 3. Auto-Highlight Active Nav Link ---
    const setActiveLink = () => {
        const currentPath = window.location.pathname;
        navLinks.forEach(link => {
            // Remove active class from all
            link.classList.remove("active");
            // Add to the one matching the current URL
            if (link.getAttribute("href") === currentPath || 
                (currentPath === "/" && link.getAttribute("href").includes("home"))) {
                link.classList.add("active");
            }
        });
    };

    // --- Initialize ---
    // Start observing elements for scroll animations
    revealElements.forEach(el => revealObserver.observe(el));

    // Listen for scroll events for the dynamic header
    window.addEventListener("scroll", handleHeader);

    // Initial checks on page load
    handleHeader();
    setActiveLink();
});