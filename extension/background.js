chrome.browserAction.onClicked.addListener(function(tab) {
  // No tabs or host permissions needed!
  // chrome.tabs.executeScript({
  //   code: 'document.body.style.backgroundColor="red"'
  // });
	//chrome.tabs.executeScript(null, {file: "read.js"});
	chrome.tabs.create({
		'url': 'https://gimmehearts.herokuapp.com'
	}, function(tab){

	});
});
