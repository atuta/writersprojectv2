$().ready(function() {
   $(document).on('click', '.btn-save-cost-settings', function(event) {
            var id = this.id

            var basic = $('#basic').val()
            var standard = $('#standard').val()
            var expert = $('#expert').val()
            var extra_proofreading = $('#extra-proofreading').val()
            var priority_order = $('#priority-order').val()
            var payout_perc = $('#payout-perc').val()

			var csrftoken = getCookie('csrftoken');
			var dataString =  'basic=' + basic + '&standard=' + standard + '&expert=' + expert
			+ '&extra_proofreading=' + extra_proofreading + '&priority_order=' + priority_order
			+ '&payout_perc=' + payout_perc;

            try{
			$.ajax({
				type: "POST",
				url: "/writersapp/save-cost-settings/",
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
                            text: "Action was successful",
                            icon: "success"
                            });
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
    });

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
