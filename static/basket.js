/**
 * Created by Kara on 2/22/16.
 */

$('#add-yarn-button').click(function() {
    $('.overlay').toggle();
    $('.modal').toggle();
    $('#search-yarn').toggle();
});

$('#search-yarn-form').submit(searchForYarns);

function searchForYarns(evt) {
    evt.preventDefault();
    $('#search-yarn').toggle();
    $('#add-new-yarn').toggle();
    var name = $('#yarn-name-field').val();
    var payload = {"yarn_name": name};

    $.post("/find_yarn_matches.json", payload, showYarnOptions);
}

function showYarnOptions(result) {
    var yarnList = result["yarns"];
    if (yarnList.length !== 0) {
        var text = "<label>Select a yarn from the list below: </label><br>" +
            "<form id='yarn-select-form' action='/add_yarn_to_basket' method='POST'>" +
            "<select name='yarn_select'>";
        for (var i = 0; i < yarnList.length; i++) {
            var yarn = yarnList[i];
            text += "<option value='" + yarn.yarn_id + "'>" + yarn.company + " " + yarn.yarn_name + "</option><br>";
        }
        text += "</select><label>How many yards? <input type='number' name='yardage'></label>" +
            "<br><label>What color? <input type='text' name='colorway'></label>" +
            "<br><input type='submit' value='Submit'>" +
            "</form>";
        text += "<br><p>Don't see the yarn you were looking for?</p>" +
            "<button class='search-again-button'>Search again</button>";

        $('#add-new-yarn').html(text);
    }
}

$('body').on('click', '.search-again-button', function() {
    $('#add-new-yarn').toggle();
    $('#search-yarn').toggle();
});
