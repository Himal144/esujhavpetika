let departmentIndex = 0;
let existingUserIndices = [];

function addDepartmentForm() {
    if (!validateCurrentForm(departmentIndex - 1)) {
        alert('Please fill out the current department form before adding a new one.');
        return;
    }

    const container = document.getElementById('department-forms-container');
    const formHTML = `
        <div class="form-section mb-3" data-index="${departmentIndex}">
            <h4>Department ${departmentIndex + 1}</h4>
            <form id="registerForm${departmentIndex}" method="post" enctype="multipart/form-data" novalidate>
                <div class="form-group mb-3">
                    <input type="text" name="name_${departmentIndex}" maxlength="255" required placeholder="Name" id="id_name_${departmentIndex}" class="form-control">
                </div>
                <input type="email" name="email_${departmentIndex}" class="form-control" id="email_${departmentIndex}" placeholder="Email">
                <br>
                <div class="form-group mb-3">
                    <label for="id_authenticated_sender_${departmentIndex}">Authenticated Sender:</label>
                    <input type="checkbox" name="authenticated_sender_${departmentIndex}" id="id_authenticated_sender_${departmentIndex}" class="form-check-input">
                </div>
            </form>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', formHTML);
    departmentIndex++;
}

function removeDepartmentForm(index) {
    const formSection = document.querySelector(`.form-section[data-index="${index}"]`);
    formSection.remove();
    existingUserIndices = existingUserIndices.filter(i => i !== index);
}

function validateCurrentForm(index) {
    if (index < 0) return true;

    const form = document.getElementById(`registerForm${index}`);
    const nameInput = form.querySelector(`input[name="name_${index}"]`);
    const emailInput = form.querySelector(`input[name="email_${index}"]`);

    if (!nameInput.value.trim()) {
        nameInput.focus();
        return false;
    }

    if (!emailInput.value.trim()) {
        emailInput.focus();
        return false;
    }

    return true;
}


//function for unhighlight the previously highlighted email field

function unhighlightExistingEmails() {
    existingUserIndices.forEach(index => {
        const form = document.querySelector(`.form-section[data-index="${index}"]`);
        const emailInput = form.querySelector(`input[name="email_${index}"]`);
        emailInput.classList.remove('is-invalid');
    });
}

async function registerAllDepartments() {
    const container = document.getElementById('department-forms-container');
    const forms = container.querySelectorAll('form');
    const formData = new FormData();

    forms.forEach((form, index) => {
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            if (input.type === 'checkbox') {
                formData.append(input.name, input.checked.toString());
            } else {
                formData.append(input.name, input.value);
            }
        });
    });

    try {
        const response = await fetch('/organization/register/multi-department/', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const responseData = await response.json();
            
            toastr.success('Departments registered succcessfully');
        } else {
            const responseData = await response.json();
            if (responseData.existing_user) {
                unhighlightExistingEmails()
                existingUserIndices = responseData.existing_email.map(user => user.index);
                existingUserIndices.forEach(index => {
                    const form = document.querySelector(`.form-section[data-index="${index}"]`);
                    const emailInput = form.querySelector(`input[name="email_${index}"]`);
                    emailInput.classList.add('is-invalid');
                    emailInput.focus();
                });
               
                toastr.error('Some users already exist. Please enter another email');
            } else {
                alert('Failed to register departments. Please try again.');
            }
        }
    } catch (error) {
        alert('An error occurred while registering departments. Please try again.');
        console.error(error);
    }
}

document.getElementById('add-department-button').addEventListener('click', addDepartmentForm);
document.getElementById('register-button').addEventListener('click', registerAllDepartments);

// Initialize with one department form
addDepartmentForm();

// document.getElementById('registerForm').addEventListener('submit', function(event) {
//     event.preventDefault();
//     var form = event.target;

//     if (!form.checkValidity()) {
//         form.reportValidity();
//     } else {
//         var formData = new FormData(form);

//         fetch(form.action, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 window.location.href = "/"; // Redirect to the base app or success page
//             } else {
//                 alert('Form submission failed: ' + JSON.stringify(data.errors));
//             }
//         })
//         .catch(error => console.error('Error:', error));
//     }
// });
