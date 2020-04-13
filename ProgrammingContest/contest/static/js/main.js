var someVar = document.getElementById("senddata").textContent;
function loadlink(){
    $('#refreshdiv').load(someVar+'/test2.html',function () {
         $(this).unwrap();
    });
}

loadlink(); // This will run on page load
setInterval(function(){
    loadlink() // this will run after every 5 seconds
}, 1000);
