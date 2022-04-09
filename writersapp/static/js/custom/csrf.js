$().ready(function() {
    $( "#frm-login" ).submit(function( event ) {

            //var username            = $("input#login-username").val();
            //var password            = $("input#login-password").val();
            //var inforedirect        = $("input#inforedirect").val();

            var username            = 'atuta';
            var password            = 'Crypto@50';

			try {
                var csrftoken = getCookie('csrftoken');
                var dataString =  'username=' + username + '&password=' + password;
                console.log("1:" + csrftoken);
				$.ajax({
					headers: {
					'Content-Type': 'application/json; charset=utf-8'
				  },
				type: "POST",
				url: "/writersapp/login-api/",
				beforeSend: function(xhr, settings) {
					//console.log("2:" + csrftoken);
					 $(".loading").show();
					if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
						xhr.setRequestHeader("X-CSRFToken", csrftoken);
					}
				},
				complete: function() { $(".loading").hide(); },
				data: dataString,
				success: function(data) {
				//var resp 		= JSON.parse(data);
				console.log(data);

				}
				});
			} catch (e)	{
				console.log(e);
			}


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