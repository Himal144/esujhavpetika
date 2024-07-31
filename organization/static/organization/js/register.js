document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    const formData = new FormData(this); // Get the form data

    const dropdown = document.getElementById('dropdown');
    if (dropdown.value === 'Multiple') {
        // Add extra data to the FormData object
        formData.append('type', 'multiple');
    }
    else{
        formData.append('type', 'single');
    }
        // Send the form data using AJAX
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/organization/account/register/', true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                console.log("response received")
                    // Request finished. Redirect based on the response received from the server
                    const response = JSON.parse(xhr.responseText);
                    window.location.href = response.redirect_url;
                
            }
        };
        xhr.send(formData);
    
});
