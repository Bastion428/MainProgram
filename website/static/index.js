let updateGameForm = document.getElementById('edit-game-form');

updateGameForm.addEventListener("submit", function (e) {
   
    e.preventDefault();

    let link = '/update-game';

    let inputID = document.getElementById("id").value;
    let inputTitle = document.getElementById("title").value;
    let inputYear = document.getElementById("year").value;
    let inputPlatform = document.getElementById("platform").value;
    let inputDeveloper = document.getElementById("developer").value;
    let inputPublisher = document.getElementById("publisher").value;
    let inputImage = document.getElementById('image').value;
    let inputHours = document.getElementById("hours").value;
    let inputScore = document.getElementById("score").value;
    let inputOwn = document.getElementById("own-edit").value;
    let inputBeat = document.getElementById("beat-edit").value;
    let inputReview = document.getElementById("review").value;


    let data = {
        id: inputID,
        title: inputTitle,
        year: inputYear,
        platform: inputPlatform,
        image: inputImage,
        developer: inputDeveloper,
        publisher: inputPublisher,
        play_hours: inputHours,
        score: inputScore,
        own: inputOwn,
    beat: inputBeat,
    review: inputReview
    };
      

    $.ajax({
        url: link,
        type: 'PUT',
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: 'text',
        success: function(result) {
            window.location.href = '/';
        },
        error: function(request,status,errorThrown) {
            alert(`Error (${request.status}): ${request.responseText}`);
            if (request.status !== 400) {
                window.location.href = '/';
            }

       }
    });

})


function deleteGame(ID, location) {
    let link = '/delete-game';
    let data = {
      game_id: ID,
      req_loc: location
    };
  
    if (!confirm("Are you sure you want to delete this game? This will permanently remove the game from your collection.")) {
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
    let table = document.getElementById("my_games_table");

    if (table === null) {
        window.location.href = "/";
    }
    for (let i = 0, row; row = table.rows[i]; i++) {
        if (table.rows[i].getAttribute("data-value") == ID) {
            table.deleteRow(i);
            break;
        }
    }
}