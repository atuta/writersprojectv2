$().ready(function() {
   $(document).on('click', '.update-task-status', function(event) {
            var id = this.id
            var splitted_id = id.split("-");

            var task_code      = splitted_id[1];
            var task_status    = splitted_id[0];

			var csrftoken = getCookie('csrftoken');
			var dataString =  'task_code=' + task_code + '&task_status=' + task_status;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/update-task-status/",
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

                            $('#card-' + task_code).fadeOut('5000');
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

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
