$().ready(function() {
   $(document).on('keyup change', '#article', function(event) {
    $('#set-word-count').show();
    $('.writer-submit-task').hide();
    var text = $('#article').text();

            // Initialize the word counter
            var numWords = 0;

            // Loop through the text
            // and count spaces in it
            for (var i = 1; i < text.length; i++) {
                var currentCharacter = text[i];

                // Check if the character is a space
                if (currentCharacter == " ") {
                    numWords += 1;
                }
            }

            // Add 1 to make the count equal to
            // the number of words
            // (count of words = count of spaces + 1)
            numWords += 1;

            // Display it as output
            $('#word-count').text(numWords)

    event.preventDefault();
    });
    });

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


	function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }
