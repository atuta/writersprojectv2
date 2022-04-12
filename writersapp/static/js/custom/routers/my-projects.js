$().ready(function() {
    $(document).on('click', '#link-my-projects', function( event ) {
         $.redirect("/writersapp/my-projects/", {"email": "isaacatuta@gmail.coms"}, "POST", "_self");
    });
    });

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}