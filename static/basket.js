/**
 * Created by Kara on 2/22/16.
 */

$('#add-yarn-button').click(function() {
    $('.overlay').toggle();
    $('.modal').toggle();
    $('#search-yarn').toggle();
});

function showYarnOptions(result) {

    var yarnList = result["yarns"];
    if (yarnList.length !== 0) {
        var text = "<label>Select a yarn from the list below: </label><br>" +
            "<form id='yarn-select-form'><select name='yarn_select'>";

        for (var i = 0; i < yarnList.length; i++) {
            var yarn = yarnList[i];
            text += "<option value='" + yarn.yarn_id + "'>" + yarn.company + " " + yarn.yarn_name + "</option><br>";
        }


        text +=  "<input type='submit' value='Submit'>" +
            "</select></form>";
        // the part below doesn't appear to work
        text += "<br><p>Don't see the yarn you were looking for?</p>" +
            "<button class='search-again-button'>Search again</button>";

        $('#yarn-search-results').html(text);
    }
}

function showYarnAddForm(evt) {
    evt.preventDefault();
    $('#yarn-search-results').toggle();
    $('#new-yarn-form').toggle();

    var text = '<form id="add-yarn-form">' +
        '<label>Yarn </label>' +
        '<label>Yardage :<input type="number" name="yards"></label>' +
        '<label>Color: <input type="text" name="colorway"></label>' +
        '<input type="submit" id="add-yarn-submit" value="Add this yarn">' +
        '</form>';

}

$('#yarn-select-form').submit(showYarnAddForm);

$('body').on('click', '.search-again-button', function() {
    $('#yarn-search-results').toggle();
    $('#search-yarn').toggle();
});


function searchForYarns(evt) {
    evt.preventDefault();
    $('#search-yarn').toggle();
    $('#yarn-search-results').toggle();
    var name = $('#yarn-name-field').val();
    var payload = {"yarn_name": name};

    $.post("/find_yarn_matches.json", payload, showYarnOptions);
}

$('#search-yarn-form').submit(searchForYarns);

