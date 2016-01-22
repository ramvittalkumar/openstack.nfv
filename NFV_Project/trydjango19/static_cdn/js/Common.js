var JavaAPI = "http://localhost:8080/connectedhome/";
var sservice_getvideoslist = "services/getVideosList";
var sservice_getVideoMetaData = "services/getVideoMetaData?fileName=";
var sservice_getviewUserMember = "services/viewUserMember";
var sservice_createUserMember = "services/createUserMember/1";
var sservice_updateUserMember = "services/updateUserMember/";
var sservice_deleteUserMember = "services/deleteUserMember/";
var sservice_updateUnknownToKnown = "services/updateUnknownToKnown";
var sservice_uploadMemberImage = "services/uploadMemberImage";
var sservice_performFrameAnalysis = "services/performFrameAnalysis";
var sservice_scheduler="services/scheduler";
var sservice_Videos = "Videos/";
var sservice_Images = "Images/";
var sservice_croptype = ".png?type=CROP";
var sservice_poitype = "?type=POI";
var sservice_updateConfig = "services/updateConfig";
var sservice_getConfig = "services/getConfig";
var Edit = "Edit";
var AddNew = "AddNew";
var sdefaultImage = "../App_Themes/Default/Images/Cognizant.png";
var AddMember = "Member Added and Trained Successfully";
var DeleteMember = "Member Deleted and Trained Successfully";
var UpdateMember = "Member Updated and Trained Successfully";
var TrainMember = "Trained Successfully";
var Threshold = "Threshold Saved Successfully";
var Thresholdrequired = "Threshold is Required";
var ThresholdName = "MATCH_PCT";


function customZoom() {
    $('.img-zoom').hover(function () {
        $(this).addClass('transition');

    }, function () {
        $(this).removeClass('transition');
    });

    $('.img-zoomlarge').hover(function () {
        $(this).addClass('transitionlarge');

    }, function () {
        $(this).removeClass('transitionlarge');
    });
}


function OnFail(result) {
    myApp.hidePleaseWait();
    alert('Request Failed');
}

var myApp;
myApp = myApp || (function () {
    var pleaseWaitDiv = $('<div class="modal fade bs-example-modal-lg" id="pleaseWaitDialog" tabindex="-1" aria-hidden="true" data-backdrop="static" role="dialog" ><div class="vertical-alignment-helper"><div class="modal-dialog modal-lg vertical-align-center" style="width: 15%;Height: 15%;" ><div class="modal-content"><div class="modal-body" ><div id="gifLoad" ><img style="width: 99%;Height: 99%;" id="loading-image" src="../App_Themes/Default/Images/ajax-loader.gif" alt="Loading..." /> </div></div></div></div></div></div>');
    return {
        showPleaseWait: function () {
            pleaseWaitDiv.modal();
        },
        hidePleaseWait: function () {
            pleaseWaitDiv.modal('hide');
        },

    };
})();

function trainMembers(msg) {
    $.ajax({
        url: JavaAPI + sservice_performFrameAnalysis,
        success: function (result) {
            alert(msg);
            return false;
        },
        error: OnFail
    }).done(function () {
        myApp.hidePleaseWait();
        return false;
    });
}


