document.addEventListener('DOMContentLoaded', function() {
    const dropdownIcons = document.querySelectorAll('.dropdown-icon');
    const modal = document.getElementById("feedbackModal");
    const closeModal = document.getElementsByClassName("close")[0];
    const submitFeedbackButton = document.getElementById("submitFeedback");
    const dropdowns = document.querySelectorAll('.dropdown-content');
    let selectedFeedbackId = null;
    let selectedDropdownId = null;

    dropdownIcons.forEach(icon => {
        icon.addEventListener('click', function(event) {
            event.stopPropagation(); // Prevent click event from bubbling up to window
            const dropdownContent = this.nextElementSibling;
            dropdownContent.classList.toggle('show');
        });
    });
  
    function handleDropdownItemClicked(event) {
        event.stopPropagation(); // Prevent click event from bubbling up to window
        selectedFeedbackId = this.closest('.feedback-item').getAttribute('data-feedback-id');
        selectedDropdownId = this.getAttribute('dropdown-clicked-id');
        modal.style.display = "block";
        document.getElementById("feedbackMessage").value = ""; // Clear the textarea
    }

    closeModal.onclick = function() {
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        } else {
            let isClickInsideDropdown = false;

            dropdowns.forEach(dropdown => {
                if (dropdown.contains(event.target)) {
                    isClickInsideDropdown = true;
                }
            });

            if (!isClickInsideDropdown) {
                dropdowns.forEach(dropdown => {
                    dropdown.classList.remove('show');
                });
            }
        }
    };

    submitFeedbackButton.onclick = function() {
        const response = document.getElementById("feedbackMessage").value;

        if (!response) {
            toastr.error("Please enter a message.");
            return;
        }

        const requestData = {
            feedback_id: selectedFeedbackId,
            dropdown_clicked_id: selectedDropdownId,
            response: response
        };

        fetch('/organization/handle-feedback-action/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
           
            modal.style.display = "none";
            toastr.success(data.message);
            dropdowns.forEach(dropdown => {
                dropdown.classList.remove('show');
            });
            window.location.href = '/organization/dashboard';
        })
        .catch((error) => {
            toastr.error(error)
        });
    };

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('dropdown-item')) {
            handleDropdownItemClicked.call(event.target, event);
        }


        
    // Send AJAX request to the backend
    // fetch('/organization/handle-feedback-action/', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify(requestData)
    // })
    // .then(response => response.json())
    // .then(data => {
    //     // Handle the response from the backend
    //     console.log('Success:', data);
    //     // You can add additional handling here based on the backend response
    //     modal.style.display = "none";

    //     // Show a success message using Toastr
    //     toastr.success(data.message);
    //     dropdowns.forEach(dropdown => {
    //         if (dropdown.classList.contains('show')) {
    //             dropdown.classList.remove('show');
    //         }
    //     });
    // })
    // .catch((error) => {
    //     console.error('Error:', error);
    // });
  })
});
