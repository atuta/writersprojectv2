$().ready(function() {
   $(document).on('click', '.message-snippet', function(event) {
          var id = this.id
          message_code = id.replace('message-snippet-', '');

			var csrftoken = getCookie('csrftoken');
			var dataString =  'message_code=' + message_code;

			//console.log(dataString); return false;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/mark-as-read/",
				headers: {'X-CSRFToken': csrftoken},
				beforeSend: function() {},
                complete: function() {},
				data: dataString,
				success: function(data) {
						 var status 	= data.status;
						 var real_data   = data.data;
						 console.log(status);

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
