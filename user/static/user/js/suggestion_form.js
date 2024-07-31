
nameModal=document.getElementById("nameModal");
const closeModal = document.getElementsByClassName("close")[0];
closeModal.onclick = function() {
    nameModal.style.display = "none";
};


$(document).ready(function() {
    // Function to filter topics and show suggestions  
    $('#suggestionTopic').on('input', function() {
       
        let query = $(this).val().toLowerCase();
        let suggestions = $('#suggestions');
        suggestions.empty();

        let filteredTopics = topics.filter(topic => topic.topic.toLowerCase().includes(query));

        if (filteredTopics.length > 0) {
            filteredTopics.forEach(function(topic) {
                suggestions.append('<div class="suggestion-item">' + topic.topic + '</div>');
            });
        }

        // Show the query itself as the last suggestion
        suggestions.append('<div class="suggestion-item">' + query + '</div>');
        suggestions.show();
    });
    // Function to handle suggestion click
    $(document).on('click', '#suggestions div', function() {

        $('#id_topic').val($(this).text());
        $('#suggestions').hide();
    });

    // Function to handle form submission
$("#submitSuggestion").on('click', async function(event){
    event.preventDefault();
    suggestion=document.getElementById('suggestion').value
    if(!validateCurrentForm(event)){
        toastr.error("Please fill the current form");
        return;
    };
    profane_status= await checkProfane(suggestion)
    if(profane_status){
        suggestionInput=document.getElementById("suggestion")
        suggestionInput.focus();
        suggestionInput.classList.add("is-invalid");
        toastr.error("Your suggestion contains the profane word. Please behave kindly.");
        return;
    }
    nameModal.style.display="block";  
})

function validateCurrentForm(event){
   let topicInput=document.getElementById("suggestionTopic")
   let suggestionInput=document.getElementById("suggestion")
  

   if (!topicInput.value.trim()) {
    topicInput.focus();
    suggestionInput.classList.remove('is-invalid');
    topicInput.classList.add('is-invalid');
    return false;
}
if (!suggestionInput.value.trim()) {
    suggestionInput.focus();
    topicInput.classList.remove('is-invalid');
    suggestionInput.classList.add('is-invalid');
    return false;
}
return true;
}


async function checkProfane(suggestion) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/suggestion/check-profane/',
            type: 'POST',
            data: JSON.stringify({ suggestion: suggestion }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    resolve(true);
                } else {
                    resolve(false);
                }
            },
            error: function(error) {
                toastr.error(error);
            }
        });
    });
}

function validateModalForm(){
if(authenticated_sender==true){
   nameInput=document.getElementById("id_name")
   if (!nameInput.value.trim()) {
    nameInput.focus();
    nameInput.classList.add('is-invalid');
    toastr.error("Please enter your name for sending suggestion.")
    return false;
}
return true;
}
return true;
}

function getCsrfTokenFromForm() {
    return $('input[name="csrfmiddlewaretoken"]').val();
}

    $('#submit-button').on('click', function(event) {
        event.preventDefault();
        if(!validateModalForm()){
            return;
        }
        id=this.getAttribute("organization-id");
        let formData = $('#suggestion-form').serialize();
        let csrfToken = getCsrfTokenFromForm();
        $.ajax({
            url: `/suggestion/${slug_name}/${id}/`,
            type: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': csrfToken // Include CSRF token in headers
            },
            success: function(response) {
                if (response.success) {
                    $('#suggestion-form')[0].reset(); 
                    location.reload();  // Reload the page to update the topics list

                } else {
                    $('#suggestion-form')[0].reset(); 
                    toastr.error('There was an error: ' + JSON.stringify(response.errors));
                    location.reload();
                }
            }
        });
    });
});
