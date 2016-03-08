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
    var selector = $("#" + data);
    if (selector.hasClass('hidden')) {
        selector.removeClass('hidden');
    }
    else {
        selector.addClass('hidden');
    }
}

function updatePreference() {
    var include = 0;
    var isChecked = $(this).is(":checked");
    if (isChecked === true) {
        include = 1;
    }
    var pref = this.id;

    var payload = {"preference": pref, "include": include};

    $.post("/update_preference.json", payload, reprintPreferences);
}

// the 27 event listeners below function on each preference checkbox in the
// form.

// TODO: Finish this list
var checkboxes = ["#weight-lace", "#weight-fingering", "#weight-sport"];
for (var i = 0; i < checkboxes.length; i++) {
    $(checkboxes[i]).change(updatePreference);
}

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

