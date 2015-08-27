$(document).ready(function(){
    $("#connect").button().click(function(){
        var hasErrors = $('#form').validator('validate').has('.has-error').length;
        if (hasErrors > 0) {
            $(".has-error:first :input").focus();
            return false;
        }        
        waitingDialog.show("Please wait...");
        var data = JSON.stringify($('form#connect_form').serializeJSON({useIntKeysAsArrayIndex: true}));
        $.ajax({
            url: "https://docs.google.com/forms/d/1F41Hvu-lKT996Fj_UF78GBL0Xax026gHnR4Feydjic4/formResponse",
            data: { "entry.1378759943": data
             },
            type: "POST",
            dataType: "json",
        }).always(function () {
            waitingDialog.hide()
            window.location.replace("connect_thankyou.html");
        });
    });

    $(window).on('scroll', function () {
        var windowTop = $(window).scrollTop(),
            scrollTop = $('#scroll-top');

        if (windowTop >= 300) {
            scrollTop.addClass('fixed');
        } else {
            scrollTop.removeClass('fixed');
        }
    });


    $('#scroll-top').on('click', function (e) {
        $('html, body').animate({
            'scrollTop': 0
        }, 1200);
        e.preventDefault();
    });
    
});
