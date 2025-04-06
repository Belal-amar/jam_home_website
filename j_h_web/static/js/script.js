

$(document).ready(function() {
    // Open Register Popup
    $('#register-btn').click(function() {
        $('#register-popup').fadeIn();
    });

    // Open Login Popup
    $('#login-btn').click(function() {
        $('#login-popup').fadeIn();
    });

    // Close Register Popup
    $('.close-register').click(function() {
        $('#register-popup').fadeOut();
    });

    // Close Login Popup
    $('.close-login').click(function() {
        $('#login-popup').fadeOut();
    });

    // Close the modal when clicking outside of the modal content
    $(window).click(function(event) {
        if ($(event.target).is('.modal')) {
            $('.modal').fadeOut();
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const slider = document.querySelector(".slider");
    const images = document.querySelectorAll(".slider img");
    const prevBtn = document.querySelector(".prev");
    const nextBtn = document.querySelector(".next");

    let index = 0;
    const totalSlides = images.length;

    function updateSlider() {
        slider.style.transform = `translateX(-${index * 100}%)`;
    }

    function nextSlide() {
        index++;
        if (index >= totalSlides) {
            index = 0; // Loop back to first image
        }
        updateSlider();
    }

    function prevSlide() {
        index--;
        if (index < 0) {
            index = totalSlides - 1; // Loop to last image
        }
        updateSlider();
    }

    nextBtn.addEventListener("click", nextSlide);
    prevBtn.addEventListener("click", prevSlide);

    // Auto scroll every 3 seconds
    setInterval(nextSlide, 3000);
});
