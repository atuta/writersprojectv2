$().ready(function() {

	$(document).on('click', '#btn-finish', function( event ) {
		var project_code = readCookie('project_code');
        var writer_level = $('input[name="writer-level"]:checked').val();

        if($('#extra-proofreading').is(':checked')){
            var extra_proofreading = $('#extra-proofreading:checked').val();
        }else{
            var extra_proofreading = 'no';
        }

        if($('#priority-order').is(':checked')){
            var priority_order = $('#priority-order:checked').val();
        }else{
            var priority_order = 'no';
        }

        if($('#favorite-writers').is(':checked')){
            var favourite_writers = $('#favorite-writers:checked').val();
        }else{
            var favourite_writers = 'no';
        }

        if(writer_level == '' || extra_proofreading == '' || priority_order == '' || favourite_writers == ''){
            swal({
                title: "Missing fields!",
                text: "Fill all required fileds",
                icon: "error",
                });
			return false;
        }else{

            //title, category, language, description, owner
            var csrftoken = readCookie('csrftoken');
            $.ajax({
                    url: '/writersapp/save-project-options/',
                    dataType: 'json',
                    type: 'post',
                    contentType: 'application/json',
                    data: JSON.stringify( { "project_code": project_code, "writer_level": writer_level,
                     "extra_proofreading": extra_proofreading, "priority_order": priority_order, "favourite_writers": favourite_writers} ),
                    processData: false,
                    beforeSend: function(xhr, settings) {
                        $(".loading").show();
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    complete: function() { $(".loading").hide(); },
                    success: function( data ){
                        //console.log( data );
                        var resp_data 	= JSON.parse(JSON.stringify(data));
                        var real_data = resp_data.data;
                        var status = resp_data.status;

                        if(status == "success"){

                            $('#btn-next').trigger('click');
                            $("#project-previous").css("display", "none");
                            $("#btn-save-project").css("display", "none");
                            $("#btn-save-task").css("display", "none");

                        }
                        else {
                            swal({
                            title: "Failed!",
                            text: "There seems to be a technical error. Try again later",
                            icon: "error",
                            });
                        }
                    },
                    error: function( jqXhr, textStatus, errorThrown ){
                        //console.log( errorThrown );
                    }
                });


        }

        event.preventDefault();
	 });

  });


function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}