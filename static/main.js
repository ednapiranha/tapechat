var tag_counter = 1;
var selected_tag = false;
var delayedTagCall = null;
var timeout = 1200;
var holdDelay = false;

function getTag() {
	try {
		if(selected_tag != true) {
			tag_counter++;
			$.getJSON('/tag_stream/' + parseInt(tag_counter), function(data){
				if(data!='') {
					$('ul#tag_stream').prepend($(data));
					$('ul#tag_stream li div.content ul li').hide();
					setTimeout(getTag, timeout);
					if($("ul#tag_stream > li").length > 30) {
						$("ul#tag_stream > li:last-child").fadeOut(function(){
							$("ul#tag_stream > li:last-child").remove();
						});
					}
				}
			});
		} 
	} catch(err) { }
}

function setDelay() {
	if(delayedTagCall!=null){
		clearInterval(delayedTagCall);
		delayedTagCall = null;
	}
	selected_tag = true;
}

function releaseDelay() {
	selected_tag = false;
	$("ul#tag_stream li ul li").fadeOut('fast');
	delayedTagCall = setTimeout(getTag,timeout);
}

$(function() {
	getTag();
	$("ul#tag_stream li span").live("mouseover",function(){
		if(!holdDelay) {
			setDelay();
			$(this).parent().find('ul li').fadeIn('fast');
		}
	});
	
	$("ul#tag_stream li span").live("click",function(){
		holdDelay = true;
		setDelay();
		$(this).parent().find('ul li').fadeIn('fast');
	});

	$("ul#tag_stream li span").live("mouseout",function(){
		if(!holdDelay) {
			releaseDelay();
		}
	});
	
	$("ul#tag_stream li ul li.close").live("click",function(){
		holdDelay = false;
		releaseDelay();
	});
});