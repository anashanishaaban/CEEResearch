document.getElementById("submit-chat").addEventListener("click", function() {
    const chatBox = document.getElementById("chat-box");
    const userInput = chatBox.value;
    const feedback = document.getElementById("chat-feedback");

    if (!userInput.trim()) {
        feedback.textContent = "Please enter some input.";
        feedback.style.color = "red";
        return;
    }

    feedback.textContent = "Processing...";
    feedback.style.color = "blue";

    fetch("/update-table", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrfToken
        },
        body: `user_input=${encodeURIComponent(userInput)}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            feedback.textContent = data.message || "Table updated successfully!";
            feedback.style.color = "green";
            location.reload();
        } else {
            feedback.textContent = data.error || "Unknown error occurred";
            feedback.style.color = "red";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        feedback.textContent = `An error occurred: ${error.message}`;
        feedback.style.color = "red";
    });
});