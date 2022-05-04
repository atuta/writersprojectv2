$().ready(function() {
   $(document).on('click', '.admin-pay', function(event) {
            var id = this.id;
            var task_code = id.replace("admin-pay-", "");

			var csrftoken = getCookie('csrftoken');
			var dataString =  'task_code=' + task_code;

			//console.log(id); return false;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/admin-pay/",
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
                                text: "Payment recorded successfully",
                                icon: "success"
                                });

                            $('#tr-' + task_code).hide();
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
