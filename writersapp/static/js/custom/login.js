$().ready(function() {
   //$(document).on('click', '#btn-login', function(event) {
   $( "#frm-login" ).submit(function( event ) {
            var username            = $("input#username").val();
            var password            = $("input#password").val();

            if(username === '' || password === ''){
                    return false;
            }

			var csrftoken = getCookie('csrftoken');
			var dataString =  'email=' + username + '&password=' + password;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/custom-login/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() { $(".loading").show(); },
                complete: function() { $(".loading").hide();},
				data: dataString,
				success: function(data) {
                        var status 	= data.status;
                        var real_data   = data.data;
                        if(status === 'success'){

                        if(real_data.userrole === '2'){
                        $(location).attr('href', '/writersapp/admin-dashboard/');
                        }
                        if(real_data.userrole === '3'){
                        $(location).attr('href', '/writersapp/client-dashboard/');
                        }
                        if(real_data.userrole === '4'){
                        $(location).attr('href', '/writersapp/writer-dashboard/');
                        }

						 }else{
						    swal({
                            title: "Login Failed!",
                            text: "Check your credentials and try again",
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
