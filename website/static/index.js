function getGame(ID) {
    fetch("/my-game", {
        method: "POST",
        body: JSON.stringify({ id: ID }),
    }).then((_res) => {
        console.log("Successfully aquired");
    });
}
