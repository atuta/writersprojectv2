$().ready(function() {
   $(document).on('click', '.send-message', function(event) {
   //console.log('success');
    $('#message-subject').val('');
    $('#message-body').val('');
    $('#modal-message').modal('show');

    $('#modal-message').on('shown.bs.modal', function () {
    $('#message-subject').focus();
    })

   var email = this.id;
   $('#send-to-email-display').text(email);
   $('#to-email').val(email);
    event.preventDefault();
    });


    $(document).on('click', '.btn-send-message', function(event) {
            var to_email = $('#to-email').val()
            var message_subject = $('#message-subject').val()
            var message_body = $('#message-body').val()

			var csrftoken = getCookie('csrftoken');
			var dataString =  'to_email=' + to_email + '&message_subject=' + message_subject
			+ '&message_body=' + message_body;

			//console.log(dataString); return false;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/send-message/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 console.log(status);
						 if(status === 'success'){
                            swal({
                                title: "Success!",
                                text: "Message sent successfully",
                                icon: "success"
                                });

                            $('#modal-message').modal('hide');
						 }else{
                             swal({
                                title: "Failed!",
                                text: "There seems to be a technical error. Try again later",
                                icon: "error"
                                });
                             }
				 }
				 });

			} catch (err){
				console.log(err.message);
			}
    event.preventDefault();
    });



    });

