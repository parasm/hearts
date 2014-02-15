var btn = document.createElement("BUTTON")
    var t = document.createTextNode("CLICK ME");
    btn.appendChild(t);
    document.body.appendChild(btn);
    var chat = $(document.getElementById("Paras Modi")); //change name
    var top = parseInt(chat.style.top.split('px')[0]);