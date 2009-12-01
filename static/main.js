var tag_counter = 1;
var selected_tag = false;

var delayedTagCall = null;

function getTag() {
	try {
		if(selected_tag != true) {
			tag_counter++;
			$.getJSON('/tag_stream/' + parseInt(tag_counter), function(data){
				$('ul#tag_stream').prepend($(data));
				setTimeout(getTag, 1500);
			});
		} 
	} catch(err) { }
}

$(function() {
	getTag();
	$("ul#tag_stream li a").live("mouseover",function(){
		if(delayedTagCall!=null){
			clearInterval(delayedTagCall);
			delayedTagCall = null;
		}
		selected_tag = true;
	});

	$("ul#tag_stream li a").live("mouseout",function(){
		selected_tag = false;
		delayedTagCall = setTimeout(getTag,1000);
	});
});