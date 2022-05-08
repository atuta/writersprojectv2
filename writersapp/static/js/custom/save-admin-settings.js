$().ready(function() {
   $( "#frm-save-admin-settings" ).submit(function( event ) {
            var words_per_hour      = $("input#words-per-hour").val();
            var buffer_in_hours     = $("input#buffer-in-hours").val();

            if(words_per_hour === '' || buffer_in_hours === ''){
                    swal({
                        title: "Missing Fields!",
                        text: "All fields are required.",
                        icon: "error"
                        });
                    return false;
            }

			var csrftoken = getCookie('csrftoken');
			var dataString =  'words_per_hour=' + words_per_hour + '&buffer_in_hours=' + buffer_in_hours;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/save-admin-settings/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
				//console.log(data);
                        var status 	= data.status;
                        if(status === 'success'){
                            swal({
                                title: "Settings Updated!",
                                text: "Settings have been updated successfully.",
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
