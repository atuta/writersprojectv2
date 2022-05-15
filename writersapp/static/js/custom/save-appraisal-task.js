$(document).ready(function (e) {
$(document).on('click', '#btn-save-appraisal-task', function( event ) {

		var task_code = $('#task-code').val();
        var task_title = $('#task-title').val();
        var task_category = $('select#task-category').val();
        var word_count = $('#word-count').val();
        var word_count_description = $('input[name="wc-description"]:checked').val();
        var keywords = $('#keywords').val();
        var keyword_repetition = $('select#keyword-repetition').val();
        var task_instructions = tinymce.get("task-instructions").getContent();

        if(task_title === '' || word_count === '' || task_category === '' || word_count_description === ''
        || keywords === '' || keyword_repetition === '' || task_instructions === ''){
            swal({
                title: "Missing fields!",
                text: "Fill all required fileds",
                icon: "error",
                });
			return false;
        }else{

            var csrftoken = readCookie('csrftoken');
            var dataString =  'task_code=' + task_code + '&task_title=' + task_title + '&task_category=' + task_category
             + '&word_count=' + word_count + '&word_count_description=' + word_count_description + '&keywords=' + keywords
              + '&keyword_repetition=' + keyword_repetition + '&task_instructions=' + encodeURIComponent(task_instructions);

               //console.log(dataString); return false;
            $.ajax({
                    url: '/writersapp/save-appraisal-task/',
                    type: 'post',
                    data: dataString,
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
                        console.log(data)
                        if(status === "success"){

                           swal({
                            title: "Success!",
                            text: "Task has been created successfully",
                            icon: "success",
                            });

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