
// Initialize with one department form

let departmentIndex = 0;
let existingUserIndices = [];

function addDepartmentForm() {
    if (validateCurrentForm(departmentIndex - 1)==0) {
        toastr.error('Please fill out the current department form before adding a new one.');
        return;
    }
    if (validateCurrentForm(departmentIndex - 1)==2) {
        toastr.error("Please enter a valid email address.");
        return;
    }
    const container = document.getElementById('department-forms-container');
    const formHTML = `
        <div class="form-section px-1 py-1" data-index="${departmentIndex}">
            <h4>Department ${departmentIndex + 1}</h4>
            <form id="registerForm${departmentIndex}" method="post" enctype="multipart/form-data" novalidate>
                <div class="form-group mb-3">
                    <input type="text" name="name_${departmentIndex}" maxlength="255" required placeholder="Name" id="id_name_${departmentIndex}" class="form-control">
                </div>
                <input type="email" name="email_${departmentIndex}" class="form-control" id="email_${departmentIndex}" placeholder="Email">
                <br>
                <div class="form-group mb-3">
                    <label for="id_authenticated_sender_${departmentIndex}">Do you want information of sender :</label>
                    <div>
                        <input type="radio" name="authenticated_sender_${departmentIndex}" value="1" id="yes_${departmentIndex}"> Yes
                        <input type="radio" name="authenticated_sender_${departmentIndex}" value="0" id="no_${departmentIndex}"> No
                    </div>
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
    if (index < 0) return 1;

    const form = document.getElementById(`registerForm${index}`);
    const nameInput = form.querySelector(`input[name="name_${index}"]`);
    const emailInput = form.querySelector(`input[name="email_${index}"]`);

    if (!nameInput.value.trim()) {
        nameInput.classList.add('is-invalid');
        nameInput.focus();
        return 0;
    }

    if (!emailInput.value.trim()) {
        emailInput.classList.add('is-invalid');
        emailInput.focus();
        return 0;
    }
    function isValidEmail(email) {
        // Regular expression for basic email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    if (!isValidEmail(emailInput.value.trim())) {
        emailInput.classList.add('is-invalid');
        emailInput.focus();
        return 2; 
    }
    return 1;
}

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
            if (input.type === 'radio' && input.checked) {
           
                formData.append(input.name, input.value);
            } else if (input.type !== 'radio') {
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
            toastr.success('Departments registered successfully');
            window.location.href="/organization/details";
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
                toastr.error('Failed to register departments. Please try again.');
            }
        }
    } catch (error) {
        toastr.error('An error occurred while registering departments. Please try again.');
        
    }
}

document.getElementById('add-department-button').addEventListener('click', addDepartmentForm);
document.getElementById('register-button').addEventListener('click', registerAllDepartments);

// Initialize with one department form
addDepartmentForm();
 