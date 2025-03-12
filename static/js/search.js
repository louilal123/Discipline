document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('.desktop-search-form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form submission

        let query = document.querySelector('.search-bar').value.trim().toLowerCase();

        let pages = [
            { url: "/", keywords: ["home", "main", "welcome"] },
            { url: "/about", keywords: ["about", "info", "company"] },
            { url: "/stats", keywords: ["stats", "data", "graph", "chart"] }
        ];

        let match = pages.find(page => page.keywords.includes(query));

        if (match) {
            window.location.href = match.url;
        } else {
            window.location.href = "/404.html";
        }
    });
});