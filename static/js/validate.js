/**
 * Description: Use this file for form validation of this project
 */


let login_form = document.getElementById('loginform');
let signup_form = document.getElementById('signupForm');
const password_regex = new RegExp("^(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^\w\d]).*$");


/**
 * ****************************  Validating Sugn Up  form  of Users ****************************
 */
if (signup_form) {
    signup_form.onsubmit = function () {
        let email = document.getElementById('email');
        let name = document.getElementById('name');
        let password = document.getElementById('password');
        let term_status = document.getElementById('check');

        email.addEventListener('blur', handleInputField);
        name.addEventListener('blur', handleInputField);
        password.addEventListener('blur', handleInputField);
        term_status.addEventListener('change', handleCheckboxField);

        console.log(password.value, password_regex.test(password.value));

        // for Email Address 
        if (!email.value) {
            document.getElementById("floatingInput_error").innerHTML = "Email is required";
        } else {
            document.getElementById("floatingInput_error").innerHTML = "";
        }

        // for Name
        if (!name.value.trim()) {
            document.getElementById("floatingInput2_error").innerHTML = "Name is required";
        } else {
            document.getElementById("floatingInput2_error").innerHTML = "";
        }

        // For Password
        if (!password.value) {
            document.getElementById("floatingPassword_error").innerHTML = "Password is required";
        } else if (!password_regex.test(password.value)) {
            document.getElementById("floatingPassword_error").innerHTML = "Password should be at least 8 characters, having at least one lower case, one upper case, one special characters, one number";
        } else {
            document.getElementById("floatingPassword_error").innerHTML = "";
        }


        // For Checkbox Button
        if (!term_status.checked) {
            document.getElementById("exampleCheck1_error").innerHTML = "Field is required";
        } else {
            document.getElementById("exampleCheck1_error").innerHTML = "";
        }

        const isValid = password_regex.test(password.value);

        if (!email.value || !password.value || !isValid) {
            return false;
        } else {
            return true;
        }
    };
}



/**
 * ****************************  Validating login form  of Users ****************************
 */
if (login_form) {
    login_form.onsubmit = function () {
        let email = document.getElementById('email');
        let password = document.getElementById('password');
        let term_status = document.getElementById('check');

        email.addEventListener('blur', handleInputField);
        password.addEventListener('blur', handleInputField);
        term_status.addEventListener('change', handleCheckboxField);

        // for Email Address input feild
        if (!email.value) {
            document.getElementById("floatingInput_error").innerHTML = "Email is required";
        } else {
            document.getElementById("floatingInput_error").innerHTML = "";
        }


        // for Password inpur feild
        if (!password.value) {
            document.getElementById("floatingPassword_error").innerHTML = "Password is required";
        } else {
            document.getElementById("floatingPassword_error").innerHTML = "";
        }

        // for terms and condition checkbox feild
        if (!term_status.checked) {
            document.getElementById("exampleCheck1_error").innerHTML = "Field is required";
        } else {
            document.getElementById("exampleCheck1_error").innerHTML = "";
        }

        if (!email.value || !password.value) {
            return false;
        } else {
            return true;
        }
    };
}



/**
 * *************************  validating for feedback and contact Form ******************************
 */
const contact_form = document.getElementById('contactForm');
if (contact_form) {
    contact_form.onsubmit = function () {
        let name = document.getElementById('name');
        let email = document.getElementById('email');
        let note = document.getElementById('note');

        name.addEventListener('blur', handleInputField);
        email.addEventListener('blur', handleInputField);
        note.addEventListener('change', handleCheckboxField);


        // for name input feild
        if (!name.value) {
            document.getElementById("name_error").innerHTML = "Name is required";
        } else {
            document.getElementById("name_error").innerHTML = "";
        }


        // for Email input feild
        if (!email.value) {
            document.getElementById("email_error").innerHTML = "Email is required";
        } else {
            document.getElementById("email_error").innerHTML = "";
        }


        // for Note input feild
        if (!note.value) {
            document.getElementById("note_error").innerHTML = "Note is required";
        } else {
            document.getElementById("note_error").innerHTML = "";
        }

        if (!email.value || !name.value || !note.value) {
            return false;
        } else {
            return true;
        }
    };
}


/**
        * *************************  validating for Booking a slot Form ******************************
        */
function validate(event) {
    let plate = document.getElementById('plate')
    let arival_date = document.getElementById('arival_date');
    let arival_time = document.getElementById('arival_time');
    let departure_date = document.getElementById('departure_date');
    let departure_time = document.getElementById('departure_time');
    let duration = document.getElementById('duration');
    let slot_number = document.getElementById('slot_number');
    let term_status = document.getElementById('check');
    let submitButton = document.getElementById('submitButton');



    // for plate input feild
    if (plate.value.trim() === '') {
        document.getElementById("plate_error").innerHTML = "License Number Plate of vihicle is required";
    } else {
        document.getElementById("plate_error").innerHTML = "";
    }



    // for Arival Date input feild
    if (arival_date.value === '') {
        document.getElementById("arival_date_error").innerHTML = "Arival Date is required";
    } else {
        document.getElementById("arival_date_error").innerHTML = "";
    }

    // for Arival Time input feild
    if (arival_time.value === '') {
        document.getElementById("arival_time_error").innerHTML = "Arival Time is required";
    } else {
        document.getElementById("arival_time_error").innerHTML = "";
    }

    // for Departure Date input feild
    if (departure_date.value === '') {
        document.getElementById("departure_date_error").innerHTML = "Departure Date is required";
    } else {
        document.getElementById("departure_date_error").innerHTML = "";
    }

    // for Arival Time input feild
    if (departure_time.value === '') {
        document.getElementById("departure_time_error").innerHTML = "Departure Time is required";
    } else {
        document.getElementById("departure_time_error").innerHTML = "";
    }

    // for time duration in hour
    if (duration.value == '') {
        document.getElementById("duration_error").innerHTML = "You must specify the time duration that are staying parking area";
    } else {
        document.getElementById("duration_error").innerHTML = "";
    }

    // for time duration in hour
    if (slot_number.value == '') {
        document.getElementById("slot_number_error").innerHTML = "You should choose a slot Number";
    } else {
        document.getElementById("slot_number_error").innerHTML = "";
    }

    // for terms and condition checkbox feild
    if (!term_status.checked) {
        document.getElementById("check_error").innerHTML = "Field is required";
    } else {
        document.getElementById("eheck_error").innerHTML = "";
    }


    if (plate.value.trim() === '' || arival_date.value === '' || duration.value === '' || arival_time.value === '' ||
        departure_date.value === '' || departure_time.value === '' || slot_number.value === '' || !term_status.checked) {
        event.preventDefault(); // Prevent default form submission
        return false; // Explicitly return false (optional)
    } else {
        return true;
    }
}









function setCurrentDate() {
    var date = new Date();
    var today = date.getDate();
    if (today < 10) {
        today = "0" + today;
    }
    var month = date.getMonth() + 1;
    if (month < 10) {
        month = "0" + month;
    }
    var year = date.getUTCFullYear();
    var currentDate = year + "-" + month + "-" + today;
    document.getElementById("arival_date").setAttribute("min", currentDate);
    document.getElementById("departure_date").setAttribute("min", currentDate);
    document.getElementById("date").setAttribute("max", currentDate);


}
/**
 * Method for handling input fields
 */
let handleInputField = function () {
    let el_ID = this.getAttribute('id') + '_error';
    if (this.value) {
        document.getElementById(el_ID).innerHTML = "";
    }
}

/**
 * Method for handling checkbox fields
 */
let handleCheckboxField = function () {
    let el_ID = this.getAttribute('id') + '_error';
    if (this.checked) {
        document.getElementById(el_ID).innerHTML = "";
    }
}