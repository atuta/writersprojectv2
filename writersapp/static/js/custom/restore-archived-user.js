$().ready(function() {
   $(document).on('click', '.restore-user', function(event) {
            var email = this.id;

			var csrftoken = getCookie('csrftoken');
			var dataString =  'email=' + encodeURIComponent(email) + '&status=no';

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/update-user-archive-status/",
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
                            text: "Action was successful",
                            icon: "success"
                            });
                            if(real_data.message == '2'){ $(location).attr('href', '/writersapp/admins/'); }
                            if(real_data.message == '3'){ $(location).attr('href', '/writersapp/clients/'); }
                            if(real_data.message == '4'){ $(location).attr('href', '/writersapp/writers/'); }
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
    // event.preventDefault();
    });
    });

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
