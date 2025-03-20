$(document).ready(function() {
    $(".menu-item").click(function() {
        $(".section").hide();
        var target = $(this).attr("data-target");
        if ($(target).length) {
            $(target).show();
        }
    });

    $("#logoUpload").change(function(event) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $("#siteLogo").attr("src", e.target.result);
        };
        reader.readAsDataURL(event.target.files[0]);
    });
});
