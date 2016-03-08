function searchForYarns(evt) {
    evt.preventDefault();
    $('#search-yarn').addClass('hidden');
    $('#add-new-yarn').removeClass('hidden');
    var name = $('#yarn-name-field').val();
    var payload = {"yarn_name": name};

    $.post("/find_yarn_matches.json", payload, showYarnOptions);
}

function showYarnOptions(result) {
    var yarnList = result['yarns'];
    if (yarnList.length !== 0) {
        var text = "<label>Select a yarn from the list below: </label><br>" +
            "<form id='yarn-select-form' action='/add_yarn_to_basket' method='POST'>" +
            "<select name='yarn_select'>";
        for (var i = 0; i < yarnList.length; i++) {
            var yarn = yarnList[i];
            text += "<option value='" + yarn.yarn_id + "'>" + yarn.company + " " + yarn.yarn_name + "</option>";
        }
        text += "</select><label>How many yards? <input type='number' name='yardage'></label>" +
            "<br><label>What color? <input type='text' name='colorway'></label>" +
            "<br><input class='btn btn-info' type='submit' value='Submit'>" +
            "</form>";
        text += "<br><p>Don't see the yarn you were looking for?</p>" +
            "<button class='btn btn-info search-again-button'>Search again</button>";

        $('#add-new-yarn').html(text);
    }
}

$('#container').freetile();

$('#search-yarn-form').submit(searchForYarns);

$('body').on('click', '.search-again-button', function() {
    $('#add-new-yarn').addClass('hidden');
    $('#search-yarn').removeClass('hidden');
});
