$().ready(function() {
$("#btn-next").css("display", "none");

	$(document).on('click', '#btn-save-project', function( event ) {

		var project_title = $('#project-title').val();
        var project_language = $('#project-language').val();
        var project_category = $('#project-category').val();
        var project_description = $('#project-description').text();

        if(project_title == '' || project_language == '' || project_category == '' || project_description == ''){
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
                    url: '/writersapp/save-project/',
                    dataType: 'json',
                    type: 'post',
                    contentType: 'application/json',
                    data: JSON.stringify( { "title": project_title, "category": project_category,
                     "language": project_language, "description": project_description, "owner": readCookie("email")} ),
                    processData: false,
                    beforeSend: function(xhr, settings) {
                        $(".loading").show();
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    complete: function() { $(".loading").hide(); },
                    success: function( data ){
                        var resp_data 	= JSON.parse(JSON.stringify(data));
                        var real_data = resp_data.data;
                        var status = resp_data.status;
                        if(status == "success"){
                           $('#btn-next').trigger('click');
                           $("#project-previous").css("display", "none");
                           $("#btn-save-project").css("display", "none");
                           $("#btn-save-task").show();
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
                        console.log( errorThrown );
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