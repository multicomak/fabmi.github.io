$("document").ready(function(){
	i = 1;
	$(".form-text").focusin
	(
		function()
			{			
				// if($(this).val() == '')
				// {	
				$(this).attr('clicktimes', parseInt($(this).attr('clicktimes'))+1);
				// }
				if(parseInt($(this).attr('clicktimes')) < 2)
				{					
					$(this).parent().removeClass("filled mature invalid");
					$(this).parent().addClass("focussed");
					// if($(this).val() == '')
					// {
						// i++;
					// }
				}
				else
				{
					if($(this).val() == '')
					{
						$(this).parent().removeClass("filled");
						$(this).parent().addClass("invalid mature focussed");
					}
				}
			}	    
	);	
	
	$(".form-text").focusout
	(
		function()
		{
			if($(this).val() == '')
			{
				$(this).parent().removeClass("focussed filled");
				$(this).parent().addClass("invalid mature");
			}
			else
			{
				if(parseInt($(this).attr('clicktimes')) < 2)
				{	
					if($(this).attr('id') == 'edit-ss-email')
					{
						if(validateEmail($(this).val()))
						{
							$(this).parent().removeClass("focussed mature invalid");
							$(this).parent().addClass("filled");
						}
						else
						{
							$(this).parent().removeClass("focussed");
							$(this).parent().addClass("invalid mature filled");
						}
					}
					else
					{						
						$(this).parent().removeClass("focussed mature invalid");
						$(this).parent().addClass("filled");
					}
				}
				else
				{
					if($(this).attr('id') == 'edit-ss-email')
					{
						if(validateEmail($(this).val()))
						{
							$(this).parent().removeClass("focussed invalid");
							$(this).parent().addClass("mature filled");
						}
						else
						{
							$(this).parent().removeClass("focussed");
							$(this).parent().addClass("invalid mature filled");
						}
					}
					else
					{
						$(this).parent().removeClass("focussed invalid");
						$(this).parent().addClass("mature filled");
					}
				}
			}
			if($("#ssdatepicker").parent().hasClass("disabled"))
			{
				$("#ssdatepicker").parent().removeClass('invalid mature focussed filled');
			}
		}
	);
	
	$(".form-text").keypress
	(
		function()
		{	
			if(parseInt($(this).attr('clicktimes')) < 2)
			{
				$(this).parent().removeClass("mature invalid");
				$(this).parent().addClass("focussed filled");
			}
			else
			{
				if($(this).val() == '')
				{
					$(this).parent().addClass("invalid mature focussed filled");
				}
			}
		}
	);
	
	$("select").change
	(
		function()
			{	
				if($(this).val() == '')
				{
					$(this).parent().removeClass("filled");
					$(this).parent().addClass("invalid");	
				}
				else
				{
					$(this).parent().removeClass("invalid");
					$(this).parent().addClass("filled");
				}				
			}	    
	);
	
	$("input[type=checkbox]").click
	(
		function()
		{
			if($(this).is(":checked"))
			{
				$(this).parent().removeClass("invalid");
				$(this).parent().addClass("filled");
			}
			else
			{
				$(this).parent().removeClass("filled");
				$(this).parent().addClass("invalid");
			}
		}	
	)
	
	$("#ssdatepicker").focusin
	(
		function()
		{
			if($("input[type=radio]").is(":checked"))
			{
			
			}
			else
			{				
				$(this).parent().addClass('disabled');
				$(this).parent().removeClass('invalid mature focussed filled');
			}
		}
	)
	
	$("input[type=radio]").click
	(
		function()
		{
			$(this).parents('.form-radios').addClass("filled");
			$("#ssdatepicker").parent().removeClass("disabled");
			if(i == 1)
			{
				i++;				
				$("#"+$(this).attr('id')).parent().addClass('active');
				id = $(this).attr('id');
			}
			else
			{
				$("#"+$(this).attr('id')).parent().addClass('active');
				$("#"+id).parent().removeClass('active');
				id = $(this).attr('id');
			}
		}
	)	
});	

function bd1_button_click()
{	
	if($("#edit-ss-email").val() == '')
	{
		$("#edit-ss-email").parent().addClass("invalid");
		flag = false;
	}
	if($("#edit-ss-looking-for").val() == '')
	{
		$("#edit-ss-looking-for").parent().addClass("invalid");
		flag = false;
	}
	if($("#edit-ss-fname").val() == '')
	{
		$("#edit-ss-fname").parent().addClass("invalid");
		flag = false;
	}
	if($("#edit-ss-lname").val() == '')
	{
		$("#edit-ss-lname").parent().addClass("invalid");
		flag = false;
	}
	if(!$("input[type=radio]").is(":checked"))
	{
		$("input[type=radio]").parents(".form-radios").addClass("invalid");
		flag = false;
	}
	if($("#ssdatepicker").val() == '')
	{
		$("#ssdatepicker").parent().addClass("invalid");
		flag = false;
	}	
	if($("#edit-ss-religion").val() == '')
	{
		$("#edit-ss-religion").parent().addClass("invalid");
		flag = false;
	}
	if($("#edit-ss-mother-tongue").val() == '')
	{
		$("#edit-ss-mother-tongue").parent().addClass("invalid");
		flag = false;
	}
	if($("#edit-ss-living-in").val() == '')
	{
		$("#edit-ss-living-in").parent().addClass("invalid");
		flag = false;
	}
	if($("#edit-ss-mobile").val() == '')
	{
		$("#edit-ss-mobile").parent().addClass("invalid");
		flag = false;
	}
	if(!$("input[type=checkbox]").is(":checked"))
	{
		$("input[type=checkbox]").parent().addClass("invalid");
		flag = false;
	}
	if(flag == false)
	{
		return false;
	}
	else
	{
		return true;
	}	
}

function validateEmail(sEmail) 
{
    var filter =/^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
    if(filter.test(sEmail)) 
	{
        return true;
    }
    else 
	{
        return false;
    }
}