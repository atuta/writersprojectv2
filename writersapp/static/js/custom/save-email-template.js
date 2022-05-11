$().ready(function() {
  $(document).on('click', '#btn-save-email', function(event) {
            var category_id = $("#email-template-category").val();
            var email_body  = tinymce.get("email-body").getContent();

            if(email_body === ''){
                    swal({
                        title: "Missing Fields!",
                        text: "Email body required.",
                        icon: "error"
                        });
                    return false;
            }

			var csrftoken = getCookie('csrftoken');
			var dataString =  'category_id=' + category_id
			+ '&email_body=' + encodeURIComponent(email_body);

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/save-email-template/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
				//console.log(data);
                        var status 	= data.status;
                        if(status === 'success'){
                            swal({
                                title: "Email Template Updated!",
                                text: "Email Template has been updated successfully.",
                                icon: "success"
                            });
						 }else{
						    swal({
                            title: "Update Failed!",
                            text: "There seems to be a technical error. Try again later",
                            icon: "error"
                            });
                        return false;
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
