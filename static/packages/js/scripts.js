(function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 72,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#mainNav",
        offset: 74,
    });

    // Collapse Navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-shrink");
        } else {
            $("#mainNav").removeClass("navbar-shrink");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);


})(jQuery); // End of use strict

// for navbar control
const navbarDefault = document.querySelector('.navbar-default')
window.onscroll = function(){
    controlNav()
    controlScrollBar()
}

function controlNav(){
    if(document.body.scrollTop >= 30 || document.documentElement.scrollTop >= 30){
        navbarDefault.classList.add('navbar-pad')
    }else{
        navbarDefault.classList.remove('navbar-pad')
    }
}

// For the scroll bar
function controlScrollBar(){
    let progressBar = document.getElementById('bs-progress-bar');
    let myScolled = document.body.scrollTop || document.documentElement.scrollTop;
    let myHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    let scolled = (myScolled / myHeight) * 100;
    progressBar.style.width = `${scolled}%`
}