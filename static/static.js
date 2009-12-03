var cleanWord = String.replace();

$(function() {
	if($('h1 span').html().length > 1) {
		var word = $('h1 span').html().replace(/((\/)|(\[)|(\])|(\\)|(\?)|(\.)|(\:)|(;)|(,)|(\!)|(\*)|(\+)|(\=)|({)|(})|(\f)|(\r)|(\n)|(\t)){1,}/, '');
		var re = new RegExp("^" + word, "i")
		$('ul.messages li a').each(function(el) {
			if($(this).html().toLowerCase().match(re)) {
				$(this).addClass('highlight');
			}
		});
	}
});
