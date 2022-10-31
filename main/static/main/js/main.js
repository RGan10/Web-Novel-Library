function showrangeval(){
    var valueofrange = document.getElementById("form_range").value;
    document.getElementById("rangeval").disabled = false;
    document.getElementById("rangeval").innerHTML = "Rate this book: "+valueofrange;

}