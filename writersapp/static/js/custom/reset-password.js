$().ready(function() {
   $(document).on('click', '#btn-reset-password', function(event) {
            var email = $('#reset-password-email').val();
            var reset_code = $('#reset-code').val();
            var new_password = $('#new-password').val();
            var confirm_new_password = $('#confirm-new-password').val();
            var csrftoken = getCookie('csrftoken');

             if(email === '' || reset_code === '' || new_password === '' || confirm_new_password === ''){
                swal({
                    title: "Missing fields!",
                    text: "All fields are required",
                    icon: "error",
                    });
                    return false;
             }

             if(new_password != confirm_new_password){
                swal({
                    title: "Password Mismatch!",
                    text: "Check your passwords and try again",
                    icon: "error",
                    });
                    return false;
             }

             var dataString =  'email=' + email + '&reset_code=' + reset_code + '&new_password=' + new_password;
            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/reset-password-api/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 console.log(data);
						 if(status === 'success'){
                            swal({
                            title: "Success!",
                            text: "Password reset successfully",
                            icon: "success",
                            });
                            $('#card-reset-password').hide();
                            $('#password-reset-success').show();
                            return false;
						 }else if(real_data.message === 'invalid_otp'){
							swal({
                            title: "Failed!",
                            text: "Invalid reset code!",
                            icon: "error",
                            });

                            return false;
						 }else{
						 swal({
                            title: "Failed!",
                            text: "There seems to be a technical error. Try again later",
                            icon: "error",
                            });

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

