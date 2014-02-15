$('document').ready(function(){
    if (localStorage.accessToken) {
        var graphUrl = "https://graph.facebook.com/me?" + localStorage.accessToken + "&callback=displayUser";
        console.log(graphUrl);

        var script = document.createElement("script");
        script.src = graphUrl;
        document.body.appendChild(script);

        function displayUser(user) {
            console.log(user);
        }
    }
    $.ajax({
        type : 'GET',
        url: "http://graph.facebook.com/me/photos",
        success: function(data){
            alert(data);
        }
    });
});