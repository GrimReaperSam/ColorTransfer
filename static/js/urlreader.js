$(document).ready(function() {
    $('.upload-image').change(function() {
        var input = this;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            var name = $(input).attr('name');
            reader.onload = function(e) {
                $('#' + name + '-image')
                    .attr('src', e.target.result)
                    .width(300);
            };
            reader.readAsDataURL(input.files[0]);
        }
    })
});