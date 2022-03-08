function load_table() {
    trs = document.querySelectorAll("table tr");
    for (i=1; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        td[2].innerHTML = `<b><a href="/ticker?quote=${td[2].innerHTML}">${td[2].innerHTML}</a></b>`
    }
}

function filter_table(elem) {
    trs = document.querySelectorAll("table tr");
    to_filter = elem.value
    for (i=1; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        if (td[4].innerHTML == to_filter || to_filter == "all") {
            trs[i].classList.remove("filtered_by_dropdown")
        }
        else {
            trs[i].classList.add("filtered_by_dropdown")
        }
    }
}

const searchTicker = (elem) =>{
    let filter = elem.value.toUpperCase();
    let tr = document.querySelectorAll("table tr");
    for (var i = 1; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName('td')[2];
        if(td) {
            let textValue = td.textContent || td.innerHTML;
            if (textValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].classList.remove("filtered_by_ticker_search")
            }
            else {
                tr[i].classList.add("filtered_by_ticker_search")
            }
        }
    }
}