$().ready(function() {
     $(document).on('click', '.return-admin-approved-task', function(event) {
        var id = this.id;
        var task_code = id.replace("return-task-", "");
        $('#client-return-task-code').val(task_code);
        $('#modal-client-return-task').modal('show');
     });

   $(document).on('click', '#client-actual-return-admin-approved-task', function(event) {
            var id = this.id;
            //var task_code = id.replace("return-task-", "");
            var task_code = $('#client-return-task-code').val();
            var reason = $('#client-return-task-reason').val();
            //console.log(return_reason);
            if(reason === ''){
                swal({
                    title: "Hold on!",
                    text: "Kindly let the writer know why the article is being returned",
                    icon: "error"
                    });

                    return false;
            }

			var csrftoken = getCookie('csrftoken');
			var dataString =  'task_code=' + task_code + '&reason=' + reason;
            $('#modal-client-return-task').modal('hide');
			// console.log(task_code); return false;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/client-writer-return/",
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
                                text: "Task returned successfully",
                                icon: "success"
                                });
                            $('#client-return-task-reason').val('');
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


    $(document).on('click', '.show-article', function(event) {
    var id = this.id;
    //console.log(id);
    var task_id = id.replace('show-article-', '');
    $('#article-' + task_id).show();
    $('#hide-article-div-' + task_id).show();
    $('#hide-article-' + task_id).show();
    $('#' + id).hide();
    event.preventDefault();
    });

    $(document).on('click', '.hide-article', function(event) {
    var id = this.id;
    //console.log(id);
    var task_id = id.replace('hide-article-', '');
    $('#article-' + task_id).hide();
    $('#show-article-div-' + task_id).show();
    $('#show-article-' + task_id).show();
    $('#' + id).hide();
    event.preventDefault();
    });


    });


    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
