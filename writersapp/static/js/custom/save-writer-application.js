$().ready(function() {

	 $( "#frm-writer-application" ).submit(function( event ) {
        var preferred_language = $('#preferred-language').val();
        var application_article = $('#application-article').text();

        if(preferred_language == '' || application_article == ''){
            swal({
                title: "Missing fields!",
                text: "Fill all required fileds",
                icon: "error",
                });
			return false;
        }else{

            var csrftoken = readCookie('csrftoken');
            var dataString =  'language=' + preferred_language
            + '&article=' + application_article
            $.ajax({
                    url: '/writersapp/save-writer-application/',
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

                            $('#application-form').hide();
                            $('#application-response').fadeIn('5000');
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