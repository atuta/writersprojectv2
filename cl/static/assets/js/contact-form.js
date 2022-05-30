$().ready(function() {
   $(document).on('click', '#btn-send-site-message', function(event) {

            var from_name = $('#name').val();
            var from_email = $('#email').val();
            var subject = $('#subject').val();
            var message = $('#message').val();

            if(from_name === '' || from_email === '' || subject === '' || message === ''){
                swal({
                    title: "Missing fields!",
                    text: "All fields are required",
                    icon: "error"
                    });

                    return false;
            }



            var message_subject = "Enquiry from: " + from_name;
			var csrftoken = getCookie('csrftoken');
			var dataString =  'from_email=' + encodeURIComponent(from_email)
			+ '&from_name=' + encodeURIComponent(from_name)
			+ '&message_subject=' + encodeURIComponent(message_subject)
			+ '&message_body=' + encodeURIComponent(message);

			//console.log(dataString); return false;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/send-site-message/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $("#message-controls").hide();  $("#wait").show();},
                complete: function() { $("#wait").hide();},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 console.log(data);
						 if(status === 'success'){
                            swal({
                                title: "Success!",
                                text: "Message sent successfully. We will get back to you as soon as possible.",
                                icon: "success"
                                });

                                $("#success").show();
                                $("#fail").hide();

                                return false;
						 }else{
                             swal({
                                title: "Failed!",
                                text: "There seems to be a technical error. Try again later",
                                icon: "error"
                                });

                                $("#success").hide();
                                $("#fail").show();

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