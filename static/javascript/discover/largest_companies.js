function load_companies() {
    trs = document.querySelector("table").querySelectorAll("tr")
    for (i=1; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        symbol = td[0].innerHTML
        img_url = `https://g.foolcdn.com/art/companylogos/mark/${symbol}.png`
        td[0].innerHTML = `<a href="/ticker/?quote=${symbol}" target="_blank"><img src=${img_url} class="table_ticker_logo" onerror="this.error=null;load_table_error_img(this, '${symbol}')"><b>${symbol}</b></a>`;

        td[1].innerHTML = "$" + td[1].innerHTML
        td[2].innerHTML = td[2].innerHTML + "%";
        if (td[2].innerHTML.includes("-")) {
            td[2].style.color = "red"
        }
        else {
            td[2].style.color = "green"
        }
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