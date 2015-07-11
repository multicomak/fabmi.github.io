searchVisible = 0;
transparent = true;

$(document).ready(function(){
    /*  Activate the tooltips      */
    $('[rel="tooltip"]').tooltip();
    

    $('#wizard').bootstrapWizard({
        'tabClass': 'nav nav-pills',
        'nextSelector': '.btn-next',
        'previousSelector': '.btn-previous',
         onInit : function(tab, navigation,index){
         
           //check number of tabs and fill the entire row
           var $total = navigation.find('li').length;
           $width = 100/$total;
           
           $display_width = $(document).width();
           
           if($display_width < 400 && $total > 3){
               $width = 50;
           }
           navigation.find('li').css('width',$width + '%');
        },
        onNext : function(tab, navigation, index){
            var wizard = navigation.closest('.wizard-card');
            var tabpaneId = $(navigation.find('li a')[index-1]).attr('href');
            var tabPane = $(wizard).find(tabpaneId)
            var hasErrors = $(tabPane).validator('validate').has('.has-error').length;
            if (hasErrors > 0) {
                $('html, body').animate({ scrollTop: $(".has-error:first :input").offset().top - 100 }, 600);
                $(".has-error:first :input").focus();
                return false;
            } else {
                return true;
            }
/*            // Disable the posibility to click on tabs
            return false;
*/        },        
        onTabClick : function(tab, navigation, index){
            // Disable the posibility to click on tabs
            return false;
        }, 
        onTabShow: function(tab, navigation, index) {
            var $total = navigation.find('li').length;
            var $current = index+1;
            
            var wizard = navigation.closest('.wizard-card');
            
            // If it's the last tab then hide the last button and show the finish instead
            if($current >= $total) {
                $(wizard).find('.btn-next').hide();
                $(wizard).find('.btn-finish').show();
            } else {
                $(wizard).find('.btn-next').show();
                $(wizard).find('.btn-finish').hide();
            }
            $('html, body').animate({
            'scrollTop': 0
            }, 1200);
        }
    });

    // Prepare the preview for profile picture
    $("#wizard-picture").change(function(){
        readURL(this);
    });
    
    
    $('[data-toggle="wizard-radio"]').click(function(event){
        radio_group = $(this).closest('.radio-group');
        radio_group.find('[data-toggle="wizard-radio"]').removeClass('active');
        $(this).addClass('active');
        $(radio_group).find('[type="radio"]').prop('checked', false);
        $(this).find('[type="radio"]').prop('checked','true');
    });
    
    $('[data-toggle="wizard-checkbox"]').click(function(event){
        $(this).toggleClass('active');
        checkbox = $(this).find('[type="checkbox"]')
        checkbox.prop('checked',!checkbox.prop("checked"));
    });
    
    $('[data-toggle="set-checked"]').click(function(event){
        checkbox = $(this).find('[type="checkbox"]')
        checkbox.prop('checked',!checkbox.prop("checked"));
    });

    $height = $(document).height();
    $('.set-full-height').css('height',$height);


    $(".btn-finish").button().click(function(){
        waitingDialog.show("Please wait...");
        var data = JSON.stringify($('form#questionnaire').serializeJSON({useIntKeysAsArrayIndex: true}));
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
    
});

    //functions for demo purpose



 //Function to show image before upload

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
        }
        reader.readAsDataURL(input.files[0]);
    }
}
    












