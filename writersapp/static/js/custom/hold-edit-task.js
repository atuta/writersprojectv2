$(document).ready(function (e) {

  $( "#frm-edit-task-description" ).submit(function( event ) {
    //console.log('debug');

        var project_code = readCookie('project_code');
        var task_title = $('#task-title').val();
        var word_count = $('#word-count').val();
        var word_count_description = $('input[name="wc-description"]:checked').val();

        var keywords = $('#keywords').val();
        var keyword_repetition = $('select#keyword-repetition').val();
        //var task_instructions = $('#task-instructions').val();
        var task_instructions = tinymce.get("task-instructions").getContent();
        var doc = $('input[type=file]').val().replace(/.*(\/|\\)/, '')

        //console.log(task_title+'#'+word_count+'#'+word_count_description+'#'+keywords+'#'+keyword_repetition+'#'+task_instructions);

        if(task_title === '' || word_count === '' || word_count_description === ''
        || keywords === '' || keyword_repetition === '' || task_instructions === ''){
            swal({
                title: "Missing fields!",
                text: "Fill all required fileds",
                icon: "error",
                });
			return false;
        }else{
            $('#task-description').hide();
            $('#task-options').fadeIn('5000');
        }
        event.preventDefault();
	 });


	 $(document).on('click', '#back-to-edit-task-description', function(event) {
            $('#task-description').fadeIn('5000');
            $('#task-options').hide();

        event.preventDefault();
	 });

    });