$().ready(function() {
    $( "#frm-login" ).submit(function( event ) {

            //var username            = $("input#login-username").val();
            //var password            = $("input#login-password").val();
            //var inforedirect        = $("input#inforedirect").val();

            var username            = 'isaacatuta@gmail.com';
            var password            = 'qwerty';

			var csrftoken = getCookie('csrftoken');
			$.ajax({
				url: '/writersapp/custom-login/',
				dataType: 'json',
				type: 'post',
				contentType: 'application/json',
				data: JSON.stringify( { "email": username, "password": password } ),
				processData: false,
				beforeSend: function(xhr, settings) {
					$(".loading").show();
					if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
						xhr.setRequestHeader("X-CSRFToken", csrftoken);
					}
				},
				complete: function() { $(".loading").hide(); },
				success: function( data ){
					console.log( data );
				},
				error: function( jqXhr, textStatus, errorThrown ){
					console.log( errorThrown );
				}
			});
    event.preventDefault();
    });
    });


	function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}