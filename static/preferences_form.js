"use strict";

// toggle update preferences form on Update Preferences Button click
$('#update_preferences_button').click(function() {
  $('#update_preferences_form').toggle();
});

// the 27 event listeners below function on each preference checkbox in the
// form. Each one 

function updatePreference(evt) {
 
        if( $(this).is(':checked') ) {
            alert("checked");
        }
    
    var pref = this.id

    $.post("/update_preference", pref);
}

$("#WHICH CHECKBOX").on("toggle", updatePreference);

$("#something").change(updatePreference);





// this should make thing next to checkbox also change the checked-ness
$('input:checkbox').change(function() {
    $('#' + this.id).toggle(this.checked);
});