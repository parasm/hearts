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