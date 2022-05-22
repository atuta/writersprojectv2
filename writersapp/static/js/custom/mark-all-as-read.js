$().ready(function() {
   $(document).on('click', '.mark-all-as-read', function(event) {
			var csrftoken = getCookie('csrftoken');
			var dataString =  '';

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/mark-all-as-read/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() {},
                complete: function() {},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 //console.log(status);

				 }
				 });

			} catch (err){
				console.log(err.message);
			}
    //event.preventDefault();
    });
    });

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
