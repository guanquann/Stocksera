function load_ipo() {
    trs = document.querySelector("table").querySelectorAll("tr")
    for (i=1; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        if (td[1].innerHTML != "-") {
            td[1].innerHTML = `<a href="/ticker/?quote=${td[1].innerHTML}" target="_blank"><b>${td[1].innerHTML}</b></a>`
        }
        if (td[4].innerHTML != "-") {
            td[4].innerHTML = Number(td[4].innerHTML).toLocaleString()
        }
        if (td[5].innerHTML != "-") {
            td[5].innerHTML = Number(td[5].innerHTML).toLocaleString()
        }
    }
}

const searchTicker = (elem) =>{
let filter = elem.value.toUpperCase();
let filter_table = elem.parentElement.parentElement.querySelector("table");
let tr = filter_table.getElementsByTagName('tr');
for (var i = 0; i < tr.length; i++){
    let td = tr[i].getElementsByTagName('td')[1];
    if(td) {
            let textValue = td.textContent || td.innerHTML;
            if (textValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display="";
            }
            else {
                tr[i].style.display="none";
            }
        }
    }
}