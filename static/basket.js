/**
 * Created by Kara on 2/22/16.
 */

$('#add_yarn_button').click(function() {
    $('.overlay').toggle();
    $('.modal').toggle();
    $('#search_yarn').toggle();
});

function showYarnOptions(result) {

    var yarnList = result["yarns"];
    if (yarnList.length !== 0) {
        var text = "<label>Select a yarn from the list below: </label><br>" +
            "<form id='yarn_select_form'><select name='yarn_select'>";

        for (var i = 0; i < yarnList.length; i++) {
            var yarn = yarnList[i];
            text += "<option value='" + yarn.yarn_id + "'>" + yarn.company + " " + yarn.yarn_name + "</option><br>";
        }


        text +=  "<input type='submit' value='Submit'>" +
            "</select></form>";
        // the part below doesn't appear to work
        text += "<br><p>Don't see the yarn you were looking for?</p>" +
            "<button class='search_again_button'>Search again</button>";

        $('#yarn_search_results').html(text);
    }
}

function showYarnAddForm(evt) {
    evt.preventDefault();
    $('#yarn_search_results').toggle();
    $('#new_yarn_form').toggle();

    var text = '<form id="add_yarn_form">' +
        '<label>Yarn </label>' +
        '<label>Yardage :<input type="number" name="yards"></label>' +
        '<label>Color: <input type="text" name="colorway"></label>' +
        '<input type="submit" id="add_yarn_submit" value="Add this yarn">' +
        '</form>';

}

$('#yarn_select_form').submit(showYarnAddForm);

$('body').on('click', '.search_again_button', function() {
    $('#yarn_search_results').toggle();
    $('#search_yarn').toggle();
});


function searchForYarns(evt) {
    evt.preventDefault();
    $('#search_yarn').toggle();
    $('#yarn_search_results').toggle();
    var name = $('#yarn_name_field').val();
    var payload = {"yarn_name": name};

    $.post("/find_yarn_matches.json", payload, showYarnOptions);
}

$('#search_yarn_form').submit(searchForYarns);

