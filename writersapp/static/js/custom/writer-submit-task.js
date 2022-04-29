$().ready(function() {
   $(document).on('click', '.writer-submit-task', function(event) {
            var id = this.id;
            var task_code = id.replace("writer-submit-task-", "");

			var csrftoken = getCookie('csrftoken');
			var dataString =  'task_code=' + task_code;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/writer-submit-task/",
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
                                text: "Task submitted successfully",
                                icon: "success"
                                });

                            $('#card-' + task_code).hide();
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
