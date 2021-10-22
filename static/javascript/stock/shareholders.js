function load_table() {
    tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        if ( ! isNaN(td[1].innerHTML)) {
            td[1].innerHTML = Number(td[1].innerHTML).toLocaleString()
        }
        if ( ! isNaN(td[4].innerHTML)) {
            td[4].innerHTML = "$" + Number(td[4].innerHTML).toLocaleString()
        }
    }
}