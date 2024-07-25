function deleteGame(ID, location) {
    /*
      Deletes the client with the given ID (clientID) from the database and Clients table
    */
    let link = '/delete-game';
    let data = {
      game_id: ID,
      req_loc: location
    };
  
    if (!confirm("Are you sure you want to delete this game?")) {
        return
    }
  
    $.ajax({
      url: link,
      type: 'DELETE',
      data: JSON.stringify(data),
      contentType: "application/json; charset=utf-8",
      dataType: 'json',
      success: function(result) {
        deleteRow(ID);
      }
    });
  }


function deleteRow(ID){
	/*
	Deletes row with the given clientID from the Clients UI table
	*/
	let table = document.getElementById("my_games_table");

	if (table === null) {
		window.location.href = "/";
	}
	for (let i = 0, row; row = table.rows[i]; i++) {
	// Looks through Clients UI table for row with matching clientID
		if (table.rows[i].getAttribute("data-value") == ID) {
			table.deleteRow(i);
			break;
		}
	}
}

$(function autoComplete() {
	$('#autocomplete').autocomplete({
		serviceUrl: 'http://127.0.0.1:5000/search',
		datatype: 'json',
		onSelect: function (suggestion) {
			let form = document.getElementById("auto_submit");
			form.action = `/my-game/${suggestion.value}`
			document.getElementById("id").value = suggestion.data
			form.submit();
		}
	  });
})