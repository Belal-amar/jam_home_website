

$(document).ready(function() {

    $('#register-btn').click(function() {
        $('#register-popup').fadeIn();
    });


    $('#login-btn').click(function() {
        $('#login-popup').fadeIn();
    });

  
    $('.close-register').click(function() {
        $('#register-popup').fadeOut();
    });

    $('.close-login').click(function() {
        $('#login-popup').fadeOut();
    });


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
            index = 0; 
        }
        updateSlider();
    }

    function prevSlide() {
        index--;
        if (index < 0) {
            index = totalSlides - 1; 
        updateSlider();
    }

    nextBtn.addEventListener("click", nextSlide);
    prevBtn.addEventListener("click", prevSlide);

  
    setInterval(nextSlide, 3000);
});
