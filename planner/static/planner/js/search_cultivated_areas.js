        $(document).ready(function () {
            $("#search_input").on("keyup", function () {
                var value = $(this).val().toLowerCase();
                $('#searchable_panels .panel').each(function(panelIndex, panel) {
                    var panelMatchesSearch = false;
                    $(panel).find('.searchable').each(function() {
                        panelMatchesSearch = panelMatchesSearch || $(this).text().toLowerCase().indexOf(value) > -1;
                    });
                    $(panel.closest('.panel')).toggle(panelMatchesSearch);
                });
            });
        });