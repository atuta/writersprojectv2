$(document).ready(function (e) {

    $(document).on('click', '.task-show-more', function( event ) {

    $('#' + (this.id).replace('id-more-', '')).fadeIn('5000');
    $('#id-less-' + (this.id).replace('id-more-', '')).fadeIn('5000');
    $('#' + this.id).hide();
    event.preventDefault();
	});

	$(document).on('click', '.task-show-less', function( event ) {
    $('#' + (this.id).replace('id-less-', '')).hide();
    $('#id-more-' + (this.id).replace('id-less-', '')).fadeIn('5000');
    $('#' + this.id).hide();
    event.preventDefault();
	});


    });