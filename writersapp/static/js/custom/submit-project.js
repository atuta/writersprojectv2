$().ready(function() {
   $(document).on('click', '.submit-project', function(event) {
            var id = this.id;

			var csrftoken = getCookie('csrftoken');
			var dataString =  'project_code=' + id;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/submit-project/",
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
                            text: "Project submitted successfully",
                            icon: "success"
                            });

                            $('#project-' + id).fadeOut('5000');
						 }else{

                             if(real_data.message === 'no_task'){
                             swal({
                                    title: "Failed!",
                                    text: "You cannot submit a project without a task",
                                    icon: "error"
                                    });

                             }else{
                                 swal({
                                    title: "Failed!",
                                    text: "There seems to be a technical error. Try again later",
                                    icon: "error"
                                    });
                                 }
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
