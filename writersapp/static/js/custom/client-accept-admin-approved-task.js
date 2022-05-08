$().ready(function() {
   $(document).on('click', '.btn-client-accept-and-rate-task', function(event) {
            // var id = this.id
            var task_code = $('#accept-admin-approved-task-code').val();
            var stars = $('input[name="rating"]:checked').val();

            if(stars === ''){
                swal({
                title: "Hold on!",
                text: "Before you leave kindly rate us.",
                icon: "error"
                });

                $('#card-' + task_code).fadeOut('5000');
             }

			var csrftoken = getCookie('csrftoken');
			var dataString =  'task_code=' + task_code + '&stars=' + stars;

			// console.log(dataString); return false;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/accept-admin-approved-task/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 //console.log(data); return false;
						 if(status === 'success'){
                            swal({
                            title: "Success!",
                            text: "Thank you for the great business",
                            icon: "success"
                            });
                            $('#modal-accept-admin-approved-task').modal('hide');
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
