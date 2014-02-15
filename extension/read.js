console.log("javascript start");
$('document').ready(function(){
	console.log("doc ready");
    try{
        chrome.cookies.get({ url: 'http://localhost:8000', name: 'id_code' },
        function (cookie) {
            if (cookie) {
              doRequest(cookie.value);
            }
            else{
                $('body').append("<h2>No id cookie found. Go to <a href='http://hearts3.herokuapp.com'>http://hearts3.herokuapp.com</a> to generate one</h2>");
            }
        });
    }catch(err){
        //do nothing
    }
    function doRequest(cookie){
        $.ajax({
            type : 'POST',
            url : 'http://localhost:8000/find',
            data : {id:cookie},
            success : function(data){
                alert(data);
				console.log("requested data");
            }
        });
    }
});