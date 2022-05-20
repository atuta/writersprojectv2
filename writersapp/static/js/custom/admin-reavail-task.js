$().ready(function() {
   $(document).on('click', '.reavail-task', function(event) {
            var id = this.id
            var task_code = id.replace('reavail-task-', '');

			var csrftoken = getCookie('csrftoken');
			var dataString =  'task_code=' + task_code;
			//console.log(dataString); return false;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/admin-reavail-task/",
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
                            text: "Task was reavailed successfully",
                            icon: "success"
                            });

                         $('#tr-' + task_code).fadeOut('5000');

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
