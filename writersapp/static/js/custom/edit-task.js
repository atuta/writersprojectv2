$(document).ready(function (e) {

  if ($('#priority-order').is(':checked')) {
     $('#deadline-div').fadeIn('3000');
  } else {
     $('#deadline-div').hide();
     $('#deadline').val('')
  }
$('#priority-order').change(function() {
  if ($(this).is(':checked')) {
     $('#deadline-div').fadeIn('3000');
  } else {
     $('#deadline-div').hide();
     $('#deadline').val('')
  }
});

$(document).on('click', '#btn-edit-task', function( event ) {

		var task_code = $('#task-code').val();
		var task_doc = $('#task-doc').val();
        var task_title = $('#task-title').val();
        var word_count = $('#word-count').val();
        var word_count_description = $('input[name="wc-description"]:checked').val();
        var deadline = $('#deadline').val().replace(/.*(\/|\\)/, '');
        var keywords = $('#keywords').val();
        var keyword_repetition = $('select#keyword-repetition').val();
        //var task_instructions = $('#task-instructions').val();
        var task_instructions = tinymce.get("task-instructions").getContent();
        var doc = $('input[type=file]').val().replace(/.*(\/|\\)/, '')

        var writer_level = $('input[name="writer-level"]:checked').val();

        if($('#extra-proofreading').is(':checked')){
            var extra_proofreading = $('#extra-proofreading:checked').val();
        }else{
            var extra_proofreading = 'no';
        }

        if($('#priority-order').is(':checked')){
            var priority_order = $('#priority-order:checked').val();
            if(deadline === ''){
                swal({
                    title: "Hold on!",
                    text: "You chose a priority order. You must specify the deadline",
                    icon: "error",
                    });
                return false;
            }
        }else{
            var priority_order = 'no';
        }

        if($('#favorite-writers').is(':checked')){
            var favourite_writers = $('#favorite-writers:checked').val();
        }else{
            var favourite_writers = 'no';
        }


        if(task_title === '' || word_count === '' || word_count_description === ''
        || keywords === '' || keyword_repetition === '' || task_instructions === ''
        || writer_level == ''){
            swal({
                title: "Missing fields!",
                text: "Fill all required fileds",
                icon: "error",
                });
			return false;
        }else{

            var csrftoken = readCookie('csrftoken');
            var dataString =  'task_code=' + task_code + '&task_title=' + task_title + '&word_count=' + word_count
             + '&word_count_description=' + word_count_description + '&keywords=' + keywords + '&keyword_repetition=' + keyword_repetition
              + '&task_instructions=' + encodeURIComponent(task_instructions) + '&doc=' + doc + '&writer_level='
                + writer_level + '&extra_proofreading=' + extra_proofreading
                + '&priority_order=' + priority_order + '&favourite_writers=' + favourite_writers + '&deadline=' + encodeURIComponent(deadline);

                //console.log(dataString);
            $.ajax({
                    url: '/writersapp/edit-task/',
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
                    console.log(data);
                        var real_data = data.data;
                        var status = data.status;

                        if(status === "success"){
                        var additional_message = "Task has been created successfully.";

                        if(task_doc != '' & doc === ''){
                            var additional_message2 = " However you did not choose a help document. What was existing has been removed. You may want to upload it again."
                        }else{
                            var additional_message2 = ''
                        }

                        if(additional_message != ''){
                        additional_message = additional_message + additional_message2
                        }
                           swal({
                            title: "Success!",
                            text: additional_message,
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



        $('#btn-edit-task').on('click', function () {
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