$(document).ready(function () {
    $("#info-bubble").on("click", function () {
        var e = document.getElementById('info-bubble-content');
        if (e) {
            if (e.style.display === "none") {
                e.style.display = "block";
            } else {
                e.style.display = "none";
            }
        }
        else {
            var div = document.createElement("div");
            div.id = "info-bubble-content"
            div.className = "alert alert-info"
            div.innerHTML = "Pas d'informations pour cette page"
            $('#body-container').prepend(div);

        }
    });
});