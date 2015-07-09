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
        $(radio_group).find('[type="checkbox"]').removeAttr('checked');
        $(this).find('[type="checkbox"]').attr('checked','true');
    });
    
    $('[data-toggle="wizard-checkbox"]').click(function(event){
        $(this).toggleClass('active');
        checkbox = $(this).find('[type="checkbox"]')
        checkbox.attr('checked',!checkbox.attr("checked"));
    });
    
    $('[data-toggle="set-checked"]').click(function(event){
        checkbox = $(this).find('[type="checkbox"]')
        checkbox.attr('checked',!checkbox.attr("checked"));
    });

    $height = $(document).height();
    $('.set-full-height').css('height',$height);
    
    //functions for demo purpose
    $(".btn-finish").button().click(function(){
        $('form#questionnaire').serializeJSON();
    });
    
});


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
    












