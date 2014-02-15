$('document').ready(function(){
    console.log("start");
    try{
        console.log("try");
        chrome.cookies.get({ url: 'http://localhost:8000', name: 'id_code' },
        function (cookie) {
            if (cookie) {
              console.log("found cookie");
              doRequest(cookie.value);
            }
            else{
                $('body').append("<h2>No id cookie found. Go to <a href='http://hearts3.herokuapp.com'>http://hearts3.herokuapp.com</a> to generate one</h2>");
                console.log("No cookie found");
            }
        });
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