jQuery(function(){
    $('#myModal').modal('hide').css({
        'margin-top': function () {
            return ($(document).height()/2);
        }
    });
    $('#reload').click(function(){
        window.location.reload();
    });
});
