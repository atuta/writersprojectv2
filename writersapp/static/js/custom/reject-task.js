$().ready(function() {
   $(document).on('click', '.reject-task', function(event) {
   //console.log('success');
   $('#modal-reject-task').modal('show')
   var id = this.id;
   var task_id = id.replace('reject-task-', '');
   $('#task-code-holder').val(task_id);
    event.preventDefault();
    });






    });

