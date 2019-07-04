$(document).ready(function() {
    /*global $*/
    $('.collapsible').collapsible();
    $('select').material_select();
    $(".button-collapse").sideNav();
    
    // Function for scroll to top. Fades in when greater than 100px from the top.
    $(window).scroll(function(){ 
        if ($(this).scrollTop() > 100) { 
            $('#scroll').fadeIn(); 
        } else { 
            $('#scroll').fadeOut(); 
        } 
    }); 
    
    // Once button is clicked it'll scroll to the top.
    $('#scroll').click(function(){ 
        $("html, body").animate({ scrollTop: 0 }, 600); 
        return false; 
    });
    
});

