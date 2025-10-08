document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("theme-toggle");

    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");

        // Store theme preference
        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    });

    // Apply saved theme
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
});
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("admin-login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            e.preventDefault();

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            // Hardcoded admin credentials (Change as needed)
            const adminUsername = "admin";
            const adminPassword = "password123";

            if (username === adminUsername && password === adminPassword) {
                // Store login status in localStorage
                localStorage.setItem("adminLoggedIn", "true");

                // Redirect to the student expectation form page
                window.location.href = "student-form.html";
            } else {
                document.getElementById("error-message").innerText = "Invalid Username or Password!";
            }
        });
    }

    // Check if user is not logged in and trying to access student-form.html
    if (window.location.pathname.includes("student-form.html")) {
        const isLoggedIn = localStorage.getItem("adminLoggedIn");
        if (!isLoggedIn) {
            alert("Access Denied! Please log in first.");
            window.location.href = "admin-login.html";
        }
    }
});

// Logout function
function logout() {
    localStorage.removeItem("adminLoggedIn");
    window.location.href = "admin-login.html";
}
