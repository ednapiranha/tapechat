var tag_counter = 1;
var selected_tag = false;

var delayedTagCall = null;

function getTag() {
	try {
		if(selected_tag != true) {
			console.log("getTag body is running");
			tag_counter++;
			$.getJSON('/tag_stream/' + parseInt(tag_counter), function(data){
				$('ul#tag_stream').prepend($(data));
				setTimeout(getTag, 1500);
			});
		} else {
			console.log("getTag body saw a flag it didn't like");
		}
	} catch(err) { }
}

$(function() {
	getTag();

	$("ul#tag_stream li a").live("mouseover",function(){
		console.log("hover in");
		if(delayedTagCall!=null){
			console.log("cancelling delayedTagCall..");
			clearInterval(delayedTagCall);
			delayedTagCall = null;
		}
		selected_tag = true;
	});

	$("ul#tag_stream li a").live("mouseout",function(){
		console.log("hover out");
		selected_tag = false;
		delayedTagCall = setTimeout(getTag,1000);
	});
});