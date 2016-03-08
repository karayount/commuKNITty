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

    $.post('/update_preference', payload, reprintPreferences);
}

// the 27 event listeners below function on each preference checkbox in the
// form.
var checkboxes = ["#weight-lace", "#weight-fingering", "#weight-sport",
                  "#weight-dk", "#weight-worsted", "#weight-aran",
                  "#weight-bulky", "#pc-cardigan", "#pc-pullover",
                  "#pc-vest", "#pc-socks", "#pc-mittens", "#pc-gloves",
                  "#pc-fingerless", "#pc-beanie-toque", "#pc-earflap",
                  "#pc-cowl", "#pc-scarf", "#pc-shawl-wrap", "#fit-adult",
                  "#fit-child", "#fit-baby", "pa-cables", "pa-lace",
                  "#pa-intarsia", "#pa-stranded", "#pa-stripes-colorwork"];
for (var i = 0; i < checkboxes.length; i++) {
    $(checkboxes[i]).change(updatePreference);
}


