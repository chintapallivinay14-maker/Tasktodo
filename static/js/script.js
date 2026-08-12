document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("themeToggle");
    const savedTheme = localStorage.getItem("taskflow-theme");
    if (savedTheme === "dark") document.body.classList.add("dark");

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            document.body.classList.toggle("dark");
            localStorage.setItem(
                "taskflow-theme",
                document.body.classList.contains("dark") ? "dark" : "light"
            );
        });
    }

    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", async () => {
            const id = button.dataset.id;
            if (!confirm("Delete this task? This action cannot be undone.")) return;

            const response = await fetch(`/tasks/${id}`, { method: "DELETE" });
            if (response.ok) {
                window.location.reload();
            } else {
                alert("Unable to delete the task.");
            }
        });
    });

    document.querySelectorAll(".status-btn").forEach(button => {
        button.addEventListener("click", async () => {
            const id = button.dataset.id;
            const status = button.dataset.status;

            const response = await fetch(`/tasks/${id}/status`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ status })
            });

            if (response.ok) {
                window.location.reload();
            } else {
                alert("Unable to update task status.");
            }
        });
    });

    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", () => {
            const submitButton = form.querySelector("button[type='submit']");
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.dataset.originalText = submitButton.textContent;
                submitButton.textContent = "Saving...";
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.textContent = submitButton.dataset.originalText;
                }, 4000);
            }
        });
    });
});
