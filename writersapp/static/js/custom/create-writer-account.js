$().ready(function() {

   $(document).on('click', '#writer-signup-proceed', function(event) {
            setTimeout(sinup_timer, 3000);

            var first_name          = $("#first-name").val();
            var last_name           = $("#last-name").val();
            var phone               = $("#phone").val();
            var email               = $("#email").val();
            var country             = $("select#country").val();
            var password            = $("#password").val();
            var confirm_password    = $("#confirm-password").val();


            if(first_name === '' || last_name === '' || phone === '' || email === ''
            || country === '' || password === '' || confirm_password === ''){

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

            $('#writer-signup-first').hide();
            $('#writer-signup-second').show();
   });

   $( "#frm-create-writer-account" ).submit(function( event ) {

            var first_name          = $("#first-name").val();
            var last_name           = $("#last-name").val();
            var phone               = $("#phone").val();
            var email               = $("#email").val();
            var country             = $("select#country").val();
            var password            = $("#password").val();
            var confirm_password    = $("#confirm-password").val();

            var preferred_language = $('#preferred-language').val();
            var application_article = tinymce.get("application-article").getContent();

            if(first_name === '' || last_name === '' || phone === '' || email === ''
            || country === '' || password === '' || confirm_password === ''
            || preferred_language === '' || application_article === ''){

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
			+ '&email=' + email + '&country=' + country
			  + '&article=' + encodeURIComponent(application_article) + '&userrole=4' + '&language='
			  + preferred_language + '&password=' + password;

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
						 if(status === 'success'){
                            swal({
                                title: "Account Created!",
                                text: "Your account has been created successfully",
                                icon: "success"
                                });
                                $('#writer-signup-card').hide();
                                 $('#writer-signup-success').show();
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

  function sinup_timer() {
  alert('Hello');
}


