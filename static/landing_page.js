/**
 * Created by Kara on 2/28/16.
 */

$( document ).ready(function() {
    $('#logout-button').addClass('hidden');
    $('#login-button').removeClass('hidden');
});


$('#login-button').click(function() {
    $('.overlay').removeClass('hidden');
    $('.modal').removeClass('hidden');
    $('#login-modal').removeClass('hidden');
});
