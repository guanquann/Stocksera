function load_table() {
    tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
//    date_list = [], close_list = [];
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
//        date_list.push(td[0].innerHTML)
//        close_list.push(td[1].innerHTML)
        td[0].innerHTML = `<a href="/jim_cramer/?quote=${td[0].innerHTML}"><b>${td[0].innerHTML}</b></a>`
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