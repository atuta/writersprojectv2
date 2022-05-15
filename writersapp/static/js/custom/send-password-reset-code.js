$().ready(function() {

   $(document).on('click', '#btn-send-password-reset-code', function(event) {
            var email = $('#reset-password-email').val();
			var csrftoken = getCookie('csrftoken');
			var dataString =  'email=' + email;

             if(email == ''){
                swal({
                    title: "Missing fields!",
                    text: "Kindly provide the email on file",
                    icon: "error",
                    });
                    return false;
             }

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/send-password-reset-code/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 //console.log(status);
						 if(status === 'success'){
                            swal({
                            title: "Success!",
                            text: "Reset code sent successfully",
                            icon: "success",
                            });

                            $('#reset-password-email').hide();
                            $('#btn-reset-password').show();
                            $('#btn-send-password-reset-code').hide();
                            $('#reset-password-controls').fadeIn('5000');
                            $('#reset-code').focus();
                            // return false;
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

