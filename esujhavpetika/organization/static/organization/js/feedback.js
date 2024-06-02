//Code for the showing the dropdown when the three dot icon is clicked
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
            const dropdownContent = this.nextElementSibling;
            dropdownContent.classList.toggle('show');
        });
    });

    //Function for the dropdown item clicked
    function handleDropdownItemClicked(event){
        selectedFeedbackId = this.closest('.feedback-item').getAttribute('data-feedback-id');
        selectedDropdownId=this.getAttribute('dropdown-clicked-id')
        modal.style.display = "block";

    closeModal.onclick = function() {
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
let response="";
    submitFeedbackButton.onclick = function() {
         response = document.getElementById("feedbackMessage").value;

        if (!response) {
            alert("Please enter a message.");
            return;
        }
  
    console.log(response)

            // Prepare data to be sent
    const requestData = {
        feedback_id: selectedFeedbackId,
        dropdown_clicked_id: selectedDropdownId,
        response:response
    };

    // Send AJAX request to the backend
    fetch('/handle-feedback-action/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the backend
        console.log('Success:', data);
        // You can add additional handling here based on the backend response
        modal.style.display = "none";

        // Show a success message using Toastr
        toastr.success(data.message);
        dropdowns.forEach(dropdown => {
            if (dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
            }
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    }
}     

    

    //Code for the registering the event listener for the dropdown item
const dropdownItem=document.querySelectorAll('.dropdown-item');
dropdownItem.forEach(item=>{
    item.addEventListener('click',handleDropdownItemClicked);
});
// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropdown-icon')) {
        dropdowns.forEach(dropdown => {
            if (dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
            }
        });
    }
};
});
    