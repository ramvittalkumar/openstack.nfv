function Initialload() {
  
}

function ImageSourceChange() {
    var val = $('#ddlImageSource option:selected').val();
    if (val == 1) {
        $("#ImageLocation").css("display", "block");
        $("#ImageFile").css("display", "none");
    } else if (val == 2) {
        $("#ImageLocation").css("display", "none");
        $("#ImageFile").css("display", "block");
    }
}

function onFileSelected(event) {
    var selectedFile = event.target.files[0];
    var reader = new FileReader();

    var imgtag = document.getElementById("imageview");
    imgtag.title = selectedFile.name;

    reader.onload = function (event) {
        imgtag.src = event.target.result;
    };
    reader.readAsDataURL(selectedFile);
}



function saveUserImage(mID) {
    var imagedata = new FormData();
    fileUpload = $("[id$='ImageFile']").get(0);
    files = fileUpload.files;
    if (files.length != 0) {
        imagedata.append("memberId", mID)
        imagedata.append("file", files[0]);

        $.ajax({
            type: "POST",
            url: JavaAPI + sservice_uploadMemberImage,
            contentType: false,
            processData: false,
            data: imagedata,
            success: function (data) {
                return true;
            },
            error: OnFail
        });
    }
}


