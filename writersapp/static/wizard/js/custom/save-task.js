$(document).ready(function (e) {

$(document).on('click', '#btn-save-task', function( event ) {

		var project_code = readCookie('project_code');
        var task_title = $('#task-title').val();
        var word_count = $('#word-count').val();
        var word_count_description = $('input[name="wc-description"]:checked').val();

        var keywords = $('#keywords').val();
        var keyword_repetition = $('select#keyword-repetition').val();
        var task_instructions = $('#task-instructions').val();

        if(task_title == '' || word_count == '' || word_count_description == ''
        || keywords == '' || keyword_repetition == '' || task_instructions == ''){
            swal({
                title: "Missing fields!",
                text: "Fill all required fileds",
                icon: "error",
                });
			return false;
        }else{

            var csrftoken = readCookie('csrftoken');
            $.ajax({
                    url: '/writersapp/save-task/',
                    dataType: 'json',
                    type: 'post',
                    contentType: 'application/json',
                    data: JSON.stringify( { "project_code": project_code, "task_title": task_title, "word_count": word_count,
                     "word_count_description": word_count_description, "keywords": keywords, "keyword_repetition": keyword_repetition,
                     "task_instructions": task_instructions} ),
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



        $('#btn-save-task').on('click', function () {
            var form_data = new FormData();
            var ins = document.getElementById('help-doc').files.length;

            if(ins == 0) {
                $('#msg').html('<span style="color:red">Select at least one file</span>');
                return;
            }

            for (var x = 0; x < ins; x++) {
                form_data.append("files[]", document.getElementById('help-doc').files[x]);
            }

            var csrf_token = readCookie('csrftoken');

            //console.log(csrf_token);

            form_data.append("csrfmiddlewaretoken", csrf_token);

            $.ajax({
                url: '/writersapp/upload-file/', // point to server-side URL
                dataType: 'json', // what to expect back from server
                cache: false,
                contentType: false,
                processData: false,
                beforeSend: function(xhr, settings) {
                $(".loading").show();
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
                },
                //data: {'data': form_data, 'csrfmiddlewaretoken': csrf_token},
                data: form_data,
                type: 'post',
                complete: function() { $(".loading").hide(); },
                success: function (data) { // display success response
                    //console.log(data);
                    //$('#msg').html(data.msg);
                },
                error: function (data) {
                    //console.log(data);
                    //$('#msg').html(data.message); // display error response
                }
            });
        });
    });