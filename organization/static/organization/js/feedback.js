document.addEventListener('DOMContentLoaded', function() {
    const dropdownIcons = document.querySelectorAll('.dropdown-icon');
    const modal = document.getElementById("feedbackModal");
    const closeModal = document.getElementsByClassName("close")[0];
    const submitFeedbackButton = document.getElementById("submitFeedback");
    const dropdowns = document.querySelectorAll('.dropdown-content');
    let selectedFeedbackId = null;
    let selectedDropdownId = null;
    let similarFeedbackModal=document.getElementById("similarFeedbackModal")
    
    similarFeedbackModal.style.display='none';

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


//Code for handling the similar suggestion click

 function handleSimilarOthersClicked(event){
    const feedbackId=selectedFeedbackId = this.closest('.feedback-item').getAttribute('data-feedback-id');
    requestData={"feedback_id":feedbackId}
    fetch('/organization/get-similar-feedback/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        const similarFeedbacks = data.similar_feedbacks;
        const modalContent = document.getElementById('similarFeedbackContent');
        modalContent.innerHTML = '';  // Clear any existing content

        // Build the HTML content for similar feedbacks
        similarFeedbacks.forEach(feedback => {

           //Function for calsulating the timesince

           function customTimeSince(date) {
            // Implement your custom logic here
            var now = new Date();
            var seconds = Math.floor((now - date) / 1000);
            
            var interval = Math.floor(seconds / 31536000);
            if (interval >= 1) {
                return interval + " year" + (interval > 1 ? "s" : "") + " ago";
            }
            interval = Math.floor(seconds / 2592000);
            if (interval >= 1) {
                return interval + " month" + (interval > 1 ? "s" : "") + " ago";
            }
            interval = Math.floor(seconds / 86400);
            if (interval >= 1) {
                return interval + " day" + (interval > 1 ? "s" : "") + " ago";
            }
            interval = Math.floor(seconds / 3600);
            if (interval >= 1) {
                return interval + " hour" + (interval > 1 ? "s" : "") + " ago";
            }
            interval = Math.floor(seconds / 60);
            if (interval >= 1) {
                return interval + " minute" + (interval > 1 ? "s" : "") + " ago";
            }
            return Math.floor(seconds) + " seconds ago";
        }

        
        var timeSince = customTimeSince(new Date(feedback.date));


            const feedbackHTML = `
                <div class="similar-feedback-item">
                <p> ${feedback.feedback}</p>
                    <p>By: ${feedback.sender}</p>
                    <p> ${timeSince}</p>
                    <hr>
                </div>
            `;
            modalContent.innerHTML += feedbackHTML;
        });

        // Show the Bootstrap modal
        similarFeedbackModal.style.display='block';
        document.getElementById("close-similar-feedback-modal").addEventListener("click",()=>{
            similarFeedbackModal.style.display='none';
        }
        )
    })
    .catch((error) => {
        toastr.error(error)
    });
    

 }

let othersSpan=document.querySelectorAll('.feedback-others')
othersSpan.forEach(element=>{
    element.addEventListener('click',handleSimilarOthersClicked)
})


});
