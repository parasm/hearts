
var chats = $(document.getElementsByClassName("titlebarTextWrapper")); //change name
var chat = chats[0];

var viewportOffset = chat.getBoundingClientRect();

var offsetLeft = viewportOffset.left + ((window.pageXOffset !== undefined) ? window.pageXOffset : (document.documentElement || document.body.parentNode || document.body).scrollLeft);
var offsetTop = viewportOffset.top + ((window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop);
var btn = document.createElement("BUTTON")
var t = document.createTextNode("Test Button");
btn.appendChild(t);
btn.offsetTop = offsetTop;
btn.offsetLeft = offsetLeft;
document.body.appendChild(btn);