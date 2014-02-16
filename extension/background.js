chrome.browserAction.onClicked.addListener(function(tab) {
  // No tabs or host permissions needed!
  // chrome.tabs.executeScript({
  //   code: 'document.body.style.backgroundColor="red"'
  // });
	//chrome.tabs.executeScript(null, {file: "read.js"});
	chrome.tabs.create({
		'url': 'http://gimmehearts.com'
	}, function(tab){

	});
});
