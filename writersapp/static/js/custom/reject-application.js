$().ready(function() {
   $(document).on('click', '.reject-application', function(event) {
            var id = this.id;
            var application_id  = id.replace('reject-', '');

			var csrftoken = getCookie('csrftoken');
			var dataString =  'application_id=' + application_id;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/reject-application/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 // console.log(status);
						 if(status === 'success'){
                            swal({
                            title: "Success!",
                            text: "Application rejected successfully",
                            icon: "success",
                            });
                             $('#card-' + application_id).fadeOut('5000');
						 }else{
						 swal({
                            title: "Failed!",
                            text: "There seems to be a technical error. Try again later",
                            icon: "error",
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

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

