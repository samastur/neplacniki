$(function () {
	function getBaseUrl(url) {
		var a = document.createElement("a"),
			host = "";

		a.href = url;
		host = a.protocol + "//" + a.hostname;
		if (a.port) {
			host += ":" + a.port;
		}
		return host;
	}

	$("script").each(function (i, el) {
		var target = $(el).data('shk-target'),
				url;
		if (target) {
			url = getBaseUrl(el.src) + '/embed/';
			$(target).load(url);
		}
	});
});
