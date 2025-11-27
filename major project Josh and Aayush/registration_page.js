// registration.js

document.addEventListener("DOMContentLoaded", function() {
  const registrationForm = document.getElementById("registration-form");

  registrationForm.addEventListener("submit", function(event) {
      event.preventDefault(); // Prevent form submission
      
      // Get form inputs
      const username = document.getElementById("registration-username").value;
      const password = document.getElementById("registration-password").value;
      const phoneNumber = document.getElementById("phone-number").value;
      const pincode = document.getElementById("pincode").value;
      const registrationNumber = document.getElementById("registration-number").value;
      const rollNumber = document.getElementById("roll-number").value;
      const role = document.querySelector('input[name="role"]:checked').value;

      // Basic validation
      if (username.trim() === "" || password.trim() === "" || phoneNumber.trim() === "" || pincode.trim() === "" || registrationNumber.trim() === "" || rollNumber.trim() === "") {
          alert("Please fill in all fields");
          return;
      }

      // Perform additional validation if needed

      // Send registration data to server (you would typically use AJAX for this)
      // Example:
      // const formData = {
      //     username: username,
      //     password: password,
      //     phoneNumber: phoneNumber,
      //     pincode: pincode,
      //     registrationNumber: registrationNumber,
      //     rollNumber: rollNumber,
      //     role: role
      // };
      // fetch("registration_endpoint_url", {
      //     method: "POST",
      //     body: JSON.stringify(formData),
      //     headers: {
      //         "Content-Type": "application/json"
      //     }
      // })
      // .then(response => {
      //     if (response.ok) {
      //         // Registration successful
      //         // Redirect or show success message
      //     } else {
      //         // Registration failed
      //         // Handle error
      //     }
      // })
      // .catch(error => console.error("Error:", error));
      
      // For demonstration, just show a success message
      alert("Registration successful");
      
      // Clear form fields
      registrationForm.reset();
  });
});
