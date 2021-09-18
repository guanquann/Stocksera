function load_table() {
    tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")[4]
        if (td.innerHTML.includes("Downgrade")) {
            td.parentElement.style.backgroundColor = "#ff000054"
        }
        else if (td.innerHTML.includes("Upgrade")){
            td.parentElement.style.backgroundColor = "#00800078"
        }
    }
}