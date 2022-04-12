$().ready(function() {
    $( "#frm-login" ).submit(function( event ) {

            var username            = $("input#username").val();
            var password            = $("input#password").val();

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
					var resp_data 	= JSON.parse(JSON.stringify(data));
					var real_data = resp_data.data;
					var status = resp_data.status;
					if(status == "success"){
                        document.cookie = "firstname=" + real_data.firstname + "; Path=/";document.cookie = "lastname=" + real_data.lastname + "; Path=/";document.cookie = "phone=" + real_data.phone + "; Path=/";document.cookie = "email=" + real_data.email + "; Path=/";document.cookie = "country=" + real_data.country + "; Path=/";document.cookie = "role=" + real_data.role + "; Path=/";
                        $(location).attr('href', "/writersapp/");
                    }
                    else {
                        swal({
                        title: "Login failed!",
                        text: "Check your credentials and try again",
                        icon: "error",
                        });
                    }
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
