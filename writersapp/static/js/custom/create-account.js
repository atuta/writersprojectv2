$().ready(function() {
   //$(document).on('click', '#btn-login', function(event) {
   $( "#frm-create-account" ).submit(function( event ) {
            var first_name          = $("#first-name").val();
            var last_name           = $("#last-name").val();
            var phone               = $("#phone").val();
            var email               = $("#email").val();
            var country             = $("select#country").val();
            var password            = $("#password").val();
            var confirm_password    = $("#confirm-password").val();

            if(password !== confirm_password){
                    swal({
                        title: "Password mismatch!",
                        text: "Check your password and try again",
                        icon: "error"
                        });
                    return false;
            }

			var csrftoken = getCookie('csrftoken');
			var dataString =  'first_name=' + first_name + '&last_name=' + last_name + '&phone=' + encodeURIComponent(phone)
			 + '&email=' + email + '&country=' + country + '&password=' + password;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/create-account/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 if(status === 'success'){
                            swal({
                                title: "Account Created!",
                                text: "Your account has been created successfully",
                                icon: "success"
                                });
                            return false;
						 }else{
						    if(real_data.message === 'user_exists'){
                                swal({
                                title: "User Exists!",
                                text: "User with the credentials provided already exists",
                                icon: "error"
                                });
						    }else{
                                swal({
                                    title: "Sign Up Failed!",
                                    text: "Kindly try again later",
                                    icon: "error"
                                    });
                                }

                        return false;
						 }
				 }
				 });

			} catch (err){
				console.log(err.message);
			}
    event.preventDefault();
    });
    });

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


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
