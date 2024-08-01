/* Description: Custom JS file */

/* Navigation*/
// Collapse the navbar by adding the top-nav-collapse class
window.onscroll = function() {
    scrollFunction();
    scrollFunctionBTT(); // back to top button
};

window.onload = function() {
    scrollFunction();
};

function scrollFunction() {
    if (document.documentElement.scrollTop > 30) {
        document.getElementById("navbarExample").classList.add("top-nav-collapse");
    } else if (document.documentElement.scrollTop < 30) {
        document.getElementById("navbarExample").classList.remove("top-nav-collapse");
    }
}

// Navbar on mobile
let elements = document.querySelectorAll(".nav-link:not(.dropdown-toggle)");

for (let i = 0; i < elements.length; i++) {
    elements[i].addEventListener("click", () => {
        document.querySelector(".offcanvas-collapse").classList.toggle("open");
    });
}

document.querySelector(".navbar-toggler").addEventListener("click", () => {
    document.querySelector(".offcanvas-collapse").classList.toggle("open");
});

// Hover on desktop
function toggleDropdown(e) {
    const _d = e.target.closest(".dropdown");
    let _m = document.querySelector(".dropdown-menu", _d);

    setTimeout(
        function() {
            const shouldOpen = _d.matches(":hover");
            _m.classList.toggle("show", shouldOpen);
            _d.classList.toggle("show", shouldOpen);

            _d.setAttribute("aria-expanded", shouldOpen);
        },
        e.type === "mouseleave" ? 300 : 0
    );
}

// On hover
const dropdownCheck = document.querySelector('.dropdown');

if (dropdownCheck !== null) {
    document.querySelector(".dropdown").addEventListener("mouseleave", toggleDropdown);
    document.querySelector(".dropdown").addEventListener("mouseover", toggleDropdown);

    // On click
    document.querySelector(".dropdown").addEventListener("click", (e) => {
        const _d = e.target.closest(".dropdown");
        let _m = document.querySelector(".dropdown-menu", _d);
        if (_d.classList.contains("show")) {
            _m.classList.remove("show");
            _d.classList.remove("show");
        } else {
            _m.classList.add("show");
            _d.classList.add("show");
        }
    });
}

/*Replace me js addded*/

/* Rotating Text - Word Cycle */
var checkReplace = document.querySelector('.replace-me');
if (checkReplace !== null) {
    var replace = new ReplaceMe(document.querySelector('.replace-me'), {
        animation: 'animated fadeIn', // Animation class or classes
        speed: 2000, // Delay between each phrase in miliseconds
        separator: ',', // Phrases separator
        hoverStop: false, // Stop rotator on phrase hover
        clickChange: false, // Change phrase on click
        loopCount: 'infinite', // Loop Count - 'infinite' or number
        autoRun: true, // Run rotator automatically
        onInit: false, // Function
        onChange: false, // Function
        onComplete: false // Function
    });
}




/* Back To Top Button */
// Get the button
let mybutton = document.getElementById("myBtn");

window.onscroll = function () {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
};


// When the user clicks on the button, scroll to the top of the document
function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE, and Opera
}


function sendDeleteRequest() {
    // Assuming you're using jQuery for AJAX
    $.ajax({
        url: '/delete_account', // Your Flask route for account deletion
        method: 'POST',
        success: function (response) {
            // Handle success (e.g., show a message, redirect, etc.)
            console.log(response.message);
        },
        error: function (error) {
            // Handle error (e.g., display an error message)
            console.error('Error deleting account:', error);
        }
    });
}
