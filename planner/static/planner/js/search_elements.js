$(document).ready(function () {
    $("#search_input").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $('#searchable_element .searchable-container').each(function (panelIndex, panel) {
            var panelMatchesSearch = false;
            $(panel).find('.searchable').each(function () {
                panelMatchesSearch = panelMatchesSearch || $(this).text().toLowerCase().indexOf(value) > -1;
            });
            $(panel.closest('.searchable-container')).toggle(panelMatchesSearch);
        });
    });
});