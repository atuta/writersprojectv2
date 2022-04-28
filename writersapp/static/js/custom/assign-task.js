$().ready(function() {
   $(document).on('click', '.assign-task', function(event) {
   //console.log('success');
   $('#modal-writers-list').modal('show')
   var id = this.id;
   var task_id = id.replace('assign-task-', '');
   $('#task-code-holder').val(task_id);
    event.preventDefault();
    });






    });

