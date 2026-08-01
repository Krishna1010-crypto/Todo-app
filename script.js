const form = document.getElementById("task-form");
const input = document.getElementById("task-input");
const list = document.getElementById("task-list");

// Load all tasks when page loads
async function loadTasks() {
    const res = await fetch("/api/tasks");
    const tasks = await res.json();
    list.innerHTML = "";
    tasks.forEach(renderTask);
}

// Render a single task in the list
function renderTask(task) {
    const li = document.createElement("li");
    li.className = "task-item" + (task.completed ? " completed" : "");
    li.dataset.id = task.id;

    li.innerHTML = `
        <div class="task-left">
            <input type="checkbox" ${task.completed ? "checked" : ""}>
            <span>${task.title}</span>
        </div>
        <button class="delete-btn">Delete</button>
    `;

    // Toggle completed
    li.querySelector("input").addEventListener("change", async (e) => {
        await fetch(`/api/tasks/${task.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ completed: e.target.checked ? 1 : 0 })
        });
        loadTasks();
    });

    // Delete task
    li.querySelector(".delete-btn").addEventListener("click", async () => {
        await fetch(`/api/tasks/${task.id}`, { method: "DELETE" });
        loadTasks();
    });

    list.appendChild(li);
}

// Add new task
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = input.value.trim();
    if (!title) return;

    await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
    });

    input.value = "";
    loadTasks();
});

loadTasks();
