$(function() {
    $("select[name=lights]").bind( "change", function(event, ui) {
        $.ajax({
            url: '/lights',
            type: 'POST',
            data: {
                'light': $(this).attr('id'),
                'mode': $(this).val()
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR.responseText);
            }
        });
    });
});