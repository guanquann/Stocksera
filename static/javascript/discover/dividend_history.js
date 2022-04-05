function load_table() {
    trs = document.querySelectorAll("tr")
    for (i=1; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        td[0].innerHTML = `<b><a href="/ticker?quote=${td[0].innerHTML}">${td[0].innerHTML}</a></b>`
    }
}

const searchTicker = (elem) =>{
    let filter = elem.value.toUpperCase();
    let filter_table = elem.parentElement.parentElement.querySelector("table");
    let tr = filter_table.getElementsByTagName('tr');
    for (var i = 0; i < tr.length; i++){
        let td = tr[i].getElementsByTagName('td')[0];
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