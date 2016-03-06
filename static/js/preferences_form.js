/*jslint node: true */
/*jslint browser: true*/
/*global $, jQuery*/

"use strict";

// toggle update preferences form on Update Preferences Button click
$('#update-preferences-button').click(function() {
    if ($('#update-preferences-form').hasClass('hidden')) {
        $('#update-preferences-form').removeClass('hidden');
    }
    else {
        $('#update-preferences-form').addClass('hidden');
    }
});

function reprintPreferences(data) {
    if ($("#" + data).hasClass('hidden')) {
        $("#" + data).removeClass('hidden');
    }
    else {
        $("#" + data).addClass('hidden');
    }
}

function updatePreference(evt) {
    var include = 0;
    var isChecked = $(this).is(":checked");
    if(isChecked)  {
        include = 1;
    }
    var pref = this.id;

    var payload = {"preference": pref, "include": include};

    $.post("/update_preference.json", payload, reprintPreferences);
}

// the 27 event listeners below function on each preference checkbox in the
// form. 
$("#weight-lace").change(updatePreference);
$("#weight-fingering").change(updatePreference);
$("#weight-sport").change(updatePreference);
$("#weight-dk").change(updatePreference);
$("#weight-worsted").change(updatePreference);
$("#weight-aran").change(updatePreference);
$("#weight-bulky").change(updatePreference);
$("#pc-cardigan").change(updatePreference);
$("#pc-pullover").change(updatePreference);
$("#pc-vest").change(updatePreference);
$("#pc-socks").change(updatePreference);
$("#pc-mittens").change(updatePreference);
$("#pc-gloves").change(updatePreference);
$("#pc-fingerless").change(updatePreference);
$("#pc-beanie-toque").change(updatePreference);
$("#pc-earflap").change(updatePreference);
$("#pc-cowl").change(updatePreference);
$("#pc-scarf").change(updatePreference);
$("#pc-shawl-wrap").change(updatePreference);
$("#fit-adult").change(updatePreference);
$("#fit-child").change(updatePreference);
$("#fit-baby").change(updatePreference);
$("#pa-cables").change(updatePreference);
$("#pa-lace").change(updatePreference);
$("#pa-intarsia").change(updatePreference);
$("#pa-stranded").change(updatePreference);
$("#pa-stripes-colorwork").change(updatePreference);

