var btn = document.createElement("BUTTON")
var t = document.createTextNode("CLICK ME");
btn.appendChild(t);
document.body.appendChild(btn);


var chat = $(document.getElementById("Paras Modi")); //change name
var top = parseInt(chat.style.top.split('px')[0]);
var left = parseInt(chat.style.top.split('px')[0]);
var newdiv = document.createElement("div");
newdiv.id = "HeartsMonitor";
newdiv.style.top = top;


document.body.appendChild(newdiv);