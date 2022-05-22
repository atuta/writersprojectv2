$().ready(function() {
    $(document).on('click', '.show-modal-2212121211', function(event) {
        var id = this.id
         console.log(id);
        var application_id = id.replace('show-modal-', '');
        $('#modal-writer-application-article').modal('show');
        var article = $('#article-' + application_id).html();
        $('#article-text').html(article);
    });



   $(document).on('click', '.accept-application', function(event) {
            var id = this.id;
            var application_id  = id.replace('approve-', '');

			var csrftoken = getCookie('csrftoken');
			var dataString =  'application_id=' + application_id;

            try{
			$.ajax({
				type: "POST",
				url: "/clapp/approve-application/",
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
                            text: "Application approved successfully",
                            icon: "success",
                            });
                            $('#card-' + application_id).fadeOut('5000');
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
