$(document).ready(function() {
    $('.pagination .disabled a, .pagination .active a').on('click', function(e) {
        e.preventDefault();
    });

    function getGravatar(email) {
        var md5 = $.md5(email);
        return 'http://www.gravatar.com/avatar/'.concat(md5).concat('?s=50&d=retro');
    }

    // set user avatar
    $('#userAvatar').attr('src', getGravatar($('#userEmail').text()));

    // initialize bootstrap tooltips
    $('[data-toggle="tooltip"]').tooltip();
});
