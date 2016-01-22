function ASPvalidate() {
    if ((document.getElementById("userName").value).length == 0) {
        alert("UserName is Required");
        document.getElementById("userName").focus();
        return false;
    } else if ((document.getElementById("Password").value).length == 0) {
        alert("Password is Required");
        document.getElementById("Password").focus();
        return false;
    }
    else { window.location = "Developer.html"; return true; }
}

function redirect() {
    window.location = "Developer.html";
    return false;
}
