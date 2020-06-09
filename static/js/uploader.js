$("#uploader").submit(function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: "/upload",
        enctype: 'multipart/form-data',
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function (data) {
            $("#successful-upload").removeAttr("hidden");
            $("#successful-upload").html("Your file was uploaded successfully:<br><a href='" + data + "'>" + data + "</a><br>");
        },
        error: function (xhr, status, error) {
            $("#failed-upload").removeAttr("hidden");
            $("#failed-upload").text(xhr.responseText);
        }
    }
    );
});
