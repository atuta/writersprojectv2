$().ready(function() {
   $(document).on('click', '#user-status', function(event) {
             if($('#user-status').is(':checked')){
                var status = 'active'
             }else{
                var status = 'inactive'
             }

            var email = $('#user-email').val();

			var csrftoken = getCookie('csrftoken');
			var dataString =  'email=' + email + '&status=' + status;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/update-user-status/",
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
                            text: "Action was successful",
                            icon: "success"
                            });
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
    // event.preventDefault();
    });
    });

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
