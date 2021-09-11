function load_table() {
    tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        if (td[3].innerHTML.includes("Sale")) {
            td[3].parentElement.style.backgroundColor = "#ff000054"
        }
        else if (td[3].innerHTML.includes("Buy")){
            td[3].parentElement.style.backgroundColor = "#00800078"
        }
        if (! isNaN(td[4].innerHTML)) {
            td[4].innerHTML = "$" + td[4].innerHTML
            td[5].innerHTML = Number(td[5].innerHTML).toLocaleString()
            td[6].innerHTML = "$" + Number(td[6].innerHTML).toLocaleString()
            td[7].innerHTML = Number(td[7].innerHTML).toLocaleString()
        }
    }
}