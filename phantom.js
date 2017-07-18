//Render
// var page = require('webpage').create();
// page.open('https://github.com/', function() {
// 	page.render('github.png');
// 	phantom.exit();
// })


//Network
"use strict";
// var host = 'https://aminer.org';
// var start = '/profile/r-bruce-irvin/53f43868dabfaee1c0aafe1f';
// var url = host + start;
var url = 'http://www.cuiqingcai.com';
var page = require('webpage').create();
page.onResouceRequested = function(request) {
	// console.log('Request ' + JSON.stringify(request, undefined, 4));
	console.log(JSON.parse(JSON.stringify(request, undefined,4)).url);
};
// page.onResouceRequested = function(response) {
	// console.log('Receive ' + JSON.stringify(response, undefined, 4));
// };
page.open(url, function(status) {
	if (status != 'success') {
		console.log('Fail to load!');
	}
	else {
		console.log('Success!');		
	}
	phantom.exit();
});