$(document).ready(function (e) {
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
                url: '/writersapp/save-task/', // point to server-side URL
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
                    console.log(data);
                    //$('#msg').html(data.msg);
                },
                error: function (data) {
                    console.log(data);
                    //$('#msg').html(data.message); // display error response
                }
            });
        });
    });