document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    var username = document.getElementById("login-username").value;
    var password = document.getElementById("login-password").value;
    var role = document.querySelector('input[name="role"]:checked').value;
    // Your login logic here
    console.log("Username: " + username + ", Password: " + password + ", Role: " + role);
});

document.getElementById("signup-form").addEventListener("submit", function(event) {
    event.preventDefault();
    var username = document.getElementById("signup-username").value;
    var password = document.getElementById("signup-password").value;
    var confirmPassword = document.getElementById("signup-confirm-password").value;
    // Your signup logic here
    console.log("Username: " + username + ", Password: " + password + ", Confirm Password: " + confirmPassword);
});

