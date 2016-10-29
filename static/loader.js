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
		var target = $(el).data('podc-target'),
				url;
		if (target) {
      url = getBaseUrl(el.src) + '/embed/';
      if (target === "after") {
        $.get(url, function (result) {
          $(el).after(result);
        });
      } else {
        $(target).load(url);
      }
		}
	});
});
