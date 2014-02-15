<<<<<<< HEAD
function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i=0; i<ca.length; i++) 
	  {
	  var c = ca[i].trim();
	  if (c.indexOf(name)==0) return c.substring(name.length,c.length);
	  }
	return "";
}

$(window).load(function(){
=======
document.body.style.backgroundColor="red";


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
document.head.appendChild(btn);

$('document').ready(function(){
    console.log("start");
>>>>>>> b24edc509e6194de7aab7bb3ac45e121f8e99660
    try{
		console.log(document.cookie);
        /*document.cookie.get({ url: 'http://localhost:8000', name: 'id_code' },
        function (cookie) {
            if (cookie) {
				console.log("found cookie");
              doRequest(cookie.value);
            }
            else{
                $('body').append("<h2>No id cookie found. Go to <a href='http://hearts3.herokuapp.com'>http://hearts3.herokuapp.com</a> to generate one</h2>");
				console.log("No cookie found");
            }
        });*/
		doRequest(getCookie('id_code'));
    }catch(err){
		console.log("Error getting id code from localhost");
		console.log(err);
    }
    function doRequest(cookie){
        $.ajax({
            type : 'POST',
            url : 'http://localhost:8000/find',
            data : {id:cookie},
            success : function(data){
                console.log(data);

            }
        });
    }
});