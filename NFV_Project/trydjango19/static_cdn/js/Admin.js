function Initialload() {
    var jsonstr = "template_name: OpenWRT \n";
    jsonstr = jsonstr + "description: Virtual WRT opensource router \n";
    jsonstr = jsonstr + "service_properties: \n";
    jsonstr = jsonstr + "vendor: tacker \n";
    jsonstr = jsonstr + "version: 1 \n";
    jsonstr = jsonstr + "type: \n";
    jsonstr = jsonstr + " - router \n";
    jsonstr = jsonstr + "- firewall \n";
    jsonstr = jsonstr + "vdus: \n";
    jsonstr = jsonstr + "vdu1: \n";
    jsonstr = jsonstr + "id: vdu1 \n";
    jsonstr = jsonstr + "vm_image: OpenWRT \n";
    jsonstr = jsonstr + "instance_type: m1.tiny \n";
    jsonstr = jsonstr + "service_type: firewall \n";
    jsonstr = jsonstr + "mgmt_driver: openwrt \n";
    jsonstr = jsonstr + "network_interfaces: \n";
    jsonstr = jsonstr + "management: \n";
    jsonstr = jsonstr + "network: net_mgmt \n";
    jsonstr = jsonstr + "management: True \n";
    jsonstr = jsonstr + "pkt_in: \n";
    jsonstr = jsonstr + "network: net0 \n";
    jsonstr = jsonstr + "pkt_out: \n";
    jsonstr = jsonstr + "network: net1 \n";
    jsonstr = jsonstr + "placement_policy: \n";
    jsonstr = jsonstr + "availability_zone: nova \n";
    jsonstr = jsonstr + "auto-scaling: noop \n";
    jsonstr = jsonstr + "monitoring_policy: ping \n";
    jsonstr = jsonstr + "failure_policy: respawn \n";
    jsonstr = jsonstr + "monitoring_parameter: \n";
    jsonstr = jsonstr + "a: \n";
    jsonstr = jsonstr + "config: \n";   
    jsonstr = jsonstr + "param0: key0 \n";
    jsonstr = jsonstr + "param1: key1 \n";
    $("[id$='txtContent']").val(jsonstr);  
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


