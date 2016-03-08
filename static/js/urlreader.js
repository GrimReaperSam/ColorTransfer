$(document).ready(function() {
    $('img').hide();

    $('.upload-image').change(function() {
        var input = this;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            var name = $(input).attr('name');
            reader.onload = function(e) {
                $('#' + name + '-image')
                    .attr('src', e.target.result)
                    .width(300)
                    .show();
            };
            reader.readAsDataURL(input.files[0]);
        }
    });

    $('.transfer-button').click(function() {
        var form_data = new FormData($('.transfer-form')[0]);
        $.ajax({
            url: '/transfer',
            type: 'POST',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(response) {
                img = JSON.parse(response).img
                $('#transfer-image')
                    .attr('src', 'data:image/jpeg;base64,' + img)
                    .width(300)
                    .show()
            }
        });
    });
});