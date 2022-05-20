$().ready(function() {
   $(document).on('click', '.pick-task', function(event) {
            var id = this.id;
            var task_code = id.replace("pick-task-", "");

			var csrftoken = getCookie('csrftoken');
			var dataString =  'task_code=' + task_code;

			//console.log(task_code);

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/pick-task/",
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
                                text: "Task picked successfully",
                                icon: "success"
                                });

                            $('#card-' + task_code).hide();
						 }else if(real_data.message === 'blacklisted'){
						    swal({
                                title: "Failed!",
                                text: "You are not allowed to pick this task again.",
                                icon: "error"
                                });
                         }else if(real_data.message === 'not_favourite'){
						    swal({
                                title: "Failed!",
                                text: "Sorry, the client prefers someone else. Try a task from a different client.",
                                icon: "error"
                                });
                         }
						 else{

                             swal({
                                title: "Failed!",
                                text: "This task might have been picked by someone else already.",
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
