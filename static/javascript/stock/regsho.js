function display_data() {
    var regsho = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    for (tr=regsho.length-1; tr>0; tr--) {
        var total_td = regsho[tr].querySelectorAll("td");
        total_td[1].innerHTML = "$" + total_td[1].innerHTML
    }
}

searchDate = () =>{
    let filter = document.getElementById('date_selector').value;
    let filter_table = document.getElementsByTagName('table')[0];
    let tr = filter_table.getElementsByTagName('tr');

    for (var i = 1; i < tr.length; i++) {
        current_date = tr[i].getElementsByTagName('td')[1].innerHTML;
        if (current_date == filter) {
            tr[i].style.display="";
        }
        else {
            tr[i].style.display="none";
        }
    }
}
