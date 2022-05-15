$().ready(function() {

	 $(document).on('click', '.submit-appraisal-task', function( event ) {
        var task_code = $('#task-code').val()
        var application_article = tinymce.get("article").getContent();

        // get word count
        theEditor = tinymce.activeEditor;
        var article_words = theEditor.plugins.wordcount.getCount();

        if(application_article == ''){
            swal({
                title: "Missing fields!",
                text: "You cannot submit a blank article",
                icon: "error",
                });
			return false;
        }else{

            var csrftoken = readCookie('csrftoken');
            var dataString =  'article=' + encodeURIComponent(application_article)
            + '&article_words=' + article_words
            $.ajax({
                    url: '/writersapp/writer-submit-appraisal-task/',
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

                    //console.log(data);
                        var real_data = data.data;
                        var status = data.status;

                        if(status === "success"){
                            swal({
                                title: "Thank you for your application!",
                                text: "You will receive an email notifying you of the application status",
                                icon: "success",
                            });

                            $('#card-' + task_code).hide();
                        return false;
                        }
                        else {

                        if(real_data.message === 'application_exists'){
                         swal({
                            title: "Failed!",
                            text: "You have a pending application. Kindly wait for a status notification",
                            icon: "error",
                            });

                            return false;
                           } else{
                            swal({
                            title: "Failed!",
                            text: "There seems to be a technical error. Try again later",
                            icon: "error",
                            });
                            }
                            return false;
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