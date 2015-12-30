jQuery(document).ready(function($){
	//create the slider
	$('.fm-testimonial-wrapper').flexslider({
		selector: ".fm-testimonial > li",
		animation: "slide",
		controlNav: false,
		slideshow: false,
		smoothHeight: true,
		start: function(){
			$('.fm-testimonial').children('li').css({
				'opacity': 1,
				'position': 'relative'
			});
		}
	});

	//open the testimonials modal page
	$('.fm-see-all').on('click', function(){
		$('.fm-testimonial-all').addClass('is-visible');
	});

	//close the testimonials modal page
	$('.fm-testimonial-all .close-btn').on('click', function(){
		$('.fm-testimonial-all').removeClass('is-visible');
	});
	$(document).keyup(function(event){
		//check if user has pressed 'Esc'
    	if(event.which=='27'){
    		$('.fm-testimonial-all').removeClass('is-visible');	
	    }
    });
    
	//build the grid for the testimonials modal page
	$('.fm-testimonial-all-wrapper').children('ul').masonry({
  		itemSelector: '.fm-testimonial-item'
	});
});
