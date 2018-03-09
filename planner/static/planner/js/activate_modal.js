$('.modal').on('show.bs.modal', function (event) {
    var modal = $(this)
    var link = $(event.relatedTarget);
    modal.load(link.attr("href"));
})