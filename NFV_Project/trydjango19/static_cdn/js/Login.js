function ASPvalidate() {
    if ((document.getElementById("username").value).length == 0) {
        alert("UserName is Required");
        document.getElementById("username").focus();
        return false;
    } else if ((document.getElementById("password").value).length == 0) {
        alert("Password is Required");
        document.getElementById("password").focus();
        return false;
    }
    else
    /*var JSONonj = {"name": "James", "age": "25"};*/
        $.post($("#frmlogin").attr("action"),
            $("#frmlogin :input").serializeArray(),
            function (data) {
                if (data == "Developer") {
                    alert("Dev hi");
                    window.location = "Developer.html";
                    return true;
                }
                else if (data == "admin") {
                    alert("Admin hi");
                    window.location = "/nfv/admin/";
                    alert(window.location.pathname);
                    return true;
                }
                else if (data == "Enterprise") {
                    window.location = "Enterprise.html";
                    return true;
                }
                else {
                    window.location = "Invalid.html";
                    return true;
                }

            });
}

     /* $.getJSON('test.json', function(jd){

     $('#divlogin').html('<p> Name: ' + jd.name + '</p>');
     $('#divlogin').append('<p>Age : ' + jd.age+ '</p>');
     });*/

  /*  $.ajax({
        url: "/nfv/admin/",
        type: "POST",
        data: JSONonj,
        dataType: "json",
        success: function (data) {
            alert('success');
            alert(data);
            /!*window.location.href = "/nfv/admin/";*!/
        }


    });
}*/


function redirect() {
    window.location = "Developer.html";
    return false;
}
