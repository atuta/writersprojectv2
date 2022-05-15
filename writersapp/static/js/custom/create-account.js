$().ready(function() {
   $( "#frm-create-account" ).submit(function( event ) {

            var first_name          = $("#first-name").val();
            var last_name           = $("#last-name").val();
            var phone               = $("#phone").val();
            var email               = $("#email").val();
            var userrole            = $("#userrole").val();
            var country             = $("select#country").val();
            var preferred_language  = $("select#preferred-language").val();
            var password            = $("#password").val();
            var confirm_password    = $("#confirm-password").val();

            if(first_name === '' || last_name === '' || phone === '' || email === ''
            || country === '' || preferred_language === '' || password === '' || confirm_password === ''){

                    swal({
                        title: "Missing fields!",
                        text: "Fill all required fields",
                        icon: "error"
                        });
                    return false;
            }

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
			+ '&email=' + email + '&userrole=' + userrole + '&country=' + country +  '&language=' + preferred_language +  '&password=' + password;

			  // console.log(dataString); return false;

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
						 //console.log(data)
						 if(status === 'success'){
                            swal({
                                title: "Account Created!",
                                text: "Your account has been created successfully",
                                icon: "success"
                                });
                                $('#signup-card').hide();
                                $('#signup-success').show();
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
