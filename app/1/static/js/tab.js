$(document).ready( function () {
    $('#table_id').DataTable({
        "ajax":"/data",
        "columns":[
            {"data":"name"},
            {"data":"time"},
            {"data":"bytes"}
        ]
    });

    $('#table_id tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
        $('#hid').show();
    } );

});