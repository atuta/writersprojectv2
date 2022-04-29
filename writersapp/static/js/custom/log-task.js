$().ready(function() {
   $(document).on('click', '#btn-save-do-task', function(event) {
   //$( "#frm-login" ).submit(function( event ) {
            var task_code          = $("input#task-code").val();
            var article            = $("#article").text();

			var csrftoken = getCookie('csrftoken');
			var dataString =  'task_code=' + task_code + '&article=' + article;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/log-task/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 console.log(status);
						 if(status === 'success'){
                            swal({
                            title: "Success!",
                            text: "Task has been saved",
                            icon: "success",
                            });

                            $('.writer-submit-task').show();
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


	function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }
