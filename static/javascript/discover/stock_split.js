function load_table() {
    trs = document.querySelectorAll("tr")
    trs[0].querySelectorAll("th")[4].style.display = "none"
    for (i=1; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        td[3].innerHTML = `<b><a href="/ticker?quote=${td[3].innerHTML}">${td[3].innerHTML}</a></b>`
        td[4].style.display = "none"
    }
}

function filter_table(elem) {
    elem = elem.value
    trs = document.querySelectorAll("tr")
    for (i=1; i<trs.length; i++) {
        tr = trs[i]
        td = tr.querySelectorAll("td")
        if (td[4].innerHTML == elem || elem == "All") {
            tr.classList.remove("filter")
        }
        else {
            tr.classList.add("filter")
        }
    }
}

const searchTicker = (elem) =>{
    let filter = elem.value.toUpperCase();
    let filter_table = elem.parentElement.parentElement.querySelector("table");
    let tr = filter_table.getElementsByTagName('tr');
    for (var i = 0; i < tr.length; i++){
        let td = tr[i].getElementsByTagName('td')[3];
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