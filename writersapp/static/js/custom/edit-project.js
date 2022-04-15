$().ready(function() {
	 $( "#frm-edit-project" ).submit(function( event ) {

        var project_code = $('#project-code').val();
		var project_title = $('#project-title').val();
		var project_category = $('#project-category').val();
        var project_language = $('#project-language').val();
        var project_description = $('#project-description').text();

        if(project_title === '' || project_language === '' || project_category === '' || project_description === ''){
            swal({
                title: "Missing fields!",
                text: "Fill all required fileds",
                icon: "error",
                });
			return false;
        }else{

            //title, category, language, description, owner
            var dataString =  'title=' + project_title + '&category=' + project_category + '&language='
            + project_language + '&description=' + project_description + '&project_code=' + project_code;
            var csrftoken = readCookie('csrftoken');
            $.ajax({
                    url: '/writersapp/edit-project/',
                    type: 'post',
                    data: dataString,
                    processData: false,
                    beforeSend: function(xhr, settings) {
                        $(".loading").show();
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    complete: function() { $(".loading").hide(); },
                    success: function( data ){
                        var real_data = data.data;
                        var status = data.status;
                        console.log(status);
                        if(status === "success"){

                           $('#btn-next').trigger('click');
                           $("#project-previous").css("display", "none");
                           $("#btn-save-project").css("display", "none");
                           $("#btn-save-task").show();

                           createCookie('project_code', real_data.message, '1')
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