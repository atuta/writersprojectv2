$().ready(function() {
   $(document).on('click', '.actual-task-avail', function(event) {
            var id = this.id
            var splitted_id = id.split("-");

            var task_code = $('#task-code-holder').val();
            var admin_payout = $('#admin-payout-general').val();

            if(admin_payout === ''){
                swal({
                    title: "Missing fields!",
                    text: "Payout amount cannot be blank",
                    icon: "error"
                    });
                 return false;
            }

            var tarehe = $('#admin-date-general').val();
            var masaa = $('#admin-time-general').val();

            if(tarehe !== '' && masaa === ''){
                swal({
                    title: "Missing fields!",
                    text: "Kindly choose time",
                    icon: "error"
                    });
                 return false;
            }

            var deadline = tarehe + ' ' + masaa;
			var csrftoken = getCookie('csrftoken');
			var dataString =  'task_code=' + task_code + '&admin_payout='
			+ admin_payout + '&deadline=' + deadline;

			//console.log(dataString); return false;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/admin-avail-task/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 //console.log(data);
						 if(status === 'success'){
                            swal({
                            title: "Success!",
                            text: "Task was assigned successfully",
                            icon: "success"
                            });
                            $('#modal-writers-list').modal('hide')
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
