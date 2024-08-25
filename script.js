function validateForm() {
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const age = document.getElementById('age').value;
    const comment = document.getElementById('comment').value.trim();

    if (!firstName || !lastName || !age || !comment) {
        alert("All fields are required.");
        return false;
    }

    if (age > 100) {
        alert("Age cannot be more than 100.");
        return false;
    }

    if (comment.split(' ').length < 3) {
        alert("Comment must contain at least 3 words.");
        return false;
    }

    return true;
}
