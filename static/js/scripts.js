$(document).ready(function() {
    /*global $*/
    $('.collapsible').collapsible();
    $('select').material_select();
    $(".button-collapse").sideNav();
});

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
} 

