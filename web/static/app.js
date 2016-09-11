$(function() {
    $("select[name=lights]").bind( "change", function(event, ui) {
      $.ajax({
            url: '/lights',
            type: 'POST',
            data: {
                'light': $(this).attr('id'),
                'mode': $(this).find('option:selected').val()
            },
            error: function() {
                console.log('error');
            }
        });
    });
});