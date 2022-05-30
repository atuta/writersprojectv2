$().ready(function() {
   $(document).on('click', '.assign-task', function(event) {
   //console.log('success');
   $('#modal-writers-list').modal('show')
   var id = this.id;

    var task_id = id.replace('assign-task-', '');
    var current_writer = $('#current-writer-' + task_id).val();

    if(current_writer === ''){ var current_writer = 'None'; }

    var favourite_needed = $('#favourite-needed-' + task_id).val();
    var payout = $('#payout-' + task_id).val();
    //console.log(payout);

    if(favourite_needed === 'yes'){
    $('#favourite-note-div').show();
    }

    $('#task-code-holder').val(task_id);
    $('.actual-payout').text(payout);
    $('#current-writer').text(current_writer);
    $('.admin-payout').val(payout);
    event.preventDefault();

    });






    });

