function get_date() {
    var date = new Date().toLocaleString();
    document.getElementById("date").innerText = "Published On: " + date;
}