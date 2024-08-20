document.addEventListener('DOMContentLoaded', () => {
    // Hide all specific setting contents initially
    const specificSettingsContent = document.querySelectorAll(".specific-setting-content");
    specificSettingsContent.forEach(element => {
        element.style.display = "none";
    });

    // Smooth scroll and show content on clicking a nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(event) {
            // event.preventDefault();

            // Hide all sections
            const settingContentContainer = document.getElementById('setting-content-container');
            Array.from(settingContentContainer.children).forEach(child => {
                child.style.display = "none";
            });

            // Determine the target content to show
            const targetId = this.getAttribute('id').replace('change-password', 'change-password-content')
                                                      .replace('edit-account', 'setting-edit-account-content')
                                                      .replace('delete-account', 'setting-delete-account-content')
                                                      .replace('sign-out', 'setting-sign-out-account-content')
                                                      .replace('privacy-policy', 'privacy-policy-content')
                                                      .replace('cookie-policy', 'cookie-policy-content');
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                targetElement.style.display = 'block';
                // Smooth scroll to the target element
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Code for the edit account
    document.getElementById('edit-account').addEventListener("click", async (event) => {
        // event.preventDefault();
        const settingContentContainer = document.getElementById('setting-content-container');
        Array.from(settingContentContainer.children).forEach(child => {
            child.style.display = "none";
        });
        document.getElementById('setting-edit-account-content').style.display = 'block';
        try {
            const response = await fetch('/organization/account/settings/edit-account/', {
                method: "GET",
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById("name").value = data.name;
                document.getElementById("email").value = data.email;

                if (data.authenticated_sender == true) {
                    document.getElementById("authenticated_sender_yes").checked = true;
                } else {
                    document.getElementById("authenticated_sender_no").checked = true;
                }
            } else {
                toastr.error('Failed to load account information.');
            }
        } catch (error) {
            toastr.error('An error occurred while editing. Please try again.');
        }
    });

    document.getElementById("submit-edit").addEventListener("click", (event) => {
        // event.preventDefault();
        document.getElementById("edit-account-form").submit();
    });

    // Code for the delete account
    document.getElementById('delete-account').addEventListener("click", (event) => {
        // event.preventDefault();
        const settingContentContainer = document.getElementById('setting-content-container');
        Array.from(settingContentContainer.children).forEach(child => {
            child.style.display = "none";
        });
        document.getElementById('setting-delete-account-content').style.display = "block";
    });

    document.getElementById('delete-account-button').addEventListener('click', () => {
        document.getElementById('delete-account-form').submit();
    });

    // Code for the change password
    const changePasswordLink = document.getElementById('change-password');
    const changePasswordContent = document.getElementById('change-password-content');

    changePasswordLink.addEventListener('click', function(event) {
        event.preventDefault();
        // Hide all specific setting contents
        const settingContentContainer = document.getElementById('setting-content-container');
        Array.from(settingContentContainer.children).forEach(child => {
            child.style.display = "none";
        });
        // Show the change password content
        changePasswordContent.style.display = 'block';
        // Smooth scroll to the target element
        changePasswordContent.scrollIntoView({ behavior: 'smooth' });
    });

    // Code for the sign out
    document.getElementById('sign-out').addEventListener("click", (event) => {
        event.preventDefault();
        const settingContentContainer = document.getElementById('setting-content-container');
        Array.from(settingContentContainer.children).forEach(child => {
            child.style.display = "none";
        });
        document.getElementById('setting-sign-out-account-content').style.display = "block";
    });

    // Code for the privacy policy
    document.getElementById('privacy-policy').addEventListener("click", (event) => {
        event.preventDefault();
        const settingContentContainer = document.getElementById('setting-content-container');
        Array.from(settingContentContainer.children).forEach(child => {
            child.style.display = "none";
        });
        document.getElementById('privacy-policy-content').style.display = "block";
    });

    // Code for the cookie policy
    document.getElementById('cookie-policy').addEventListener("click", (event) => {
        event.preventDefault();
        const settingContentContainer = document.getElementById('setting-content-container');
        Array.from(settingContentContainer.children).forEach(child => {
            child.style.display = "none";
        });
        document.getElementById('cookie-policy-content').style.display = "block";
    });

    // Code for edit the organization logo
    document.getElementById('edit-logo-button').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('logo').click();
    });

    document.getElementById('logo').addEventListener('change', function() {
        document.getElementById('edit-logo-button').style.display = 'none';
        document.getElementById('save-logo-button').style.display = 'block';

        const file = document.getElementById('logo').files[0];
        const reader = new FileReader();
        reader.onloadend = function() {
            document.getElementById('current-logo').src = reader.result;
        }
        if (file) {
            reader.readAsDataURL(file);
        }
    });

    document.getElementById('save-logo-button').addEventListener('click', function() {
        document.getElementById('logo-upload-form').submit();
        alert("Done");
    });
});
