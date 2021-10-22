function update_table() {
    var rows = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    var header_td = rows[0]
    header_td.innerHTML = `
        <th onclick="sortTable(0)" class="th-sort-desc" id='0'>Rank</th>
        <th onclick="sortTable(1)" class="th-sort-desc" id='1'>Ticker</th>
        <th onclick="sortTable(2)" class="th-sort-desc" id='2'>Date</th>
        <th onclick="sortTable(3)" class="th-sort-desc" id='3'>Short Interest</th>
        <th onclick="sortTable(4)" class="th-sort-desc" id='4'>Average Volume</th>
        <th onclick="sortTable(5)" class="th-sort-desc" id='5'>Days to Cover</th>
        <th onclick="sortTable(6)" class="th-sort-desc" id='6'>%Float Short</th>`

    for (i=1; i<rows.length; i++) {
        var td = rows[i].querySelectorAll("td");
        img_url = `https://g.foolcdn.com/art/companylogos/mark/${td[1].innerHTML}.png`
        td[1].innerHTML = `<a href="/ticker/?quote=${td[1].innerHTML}" target="_blank"><img src=${img_url} class="table_ticker_logo" onerror="this.error=null;load_table_error_img(this, '${td[1].innerHTML}')"><b>${td[1].innerHTML}</b></a>`;
        td[3].innerHTML = Number(td[3].innerHTML).toLocaleString()
        td[4].innerHTML = Number(td[4].innerHTML).toLocaleString()
    }
    document.getElementsByClassName("table_div")[0].style.removeProperty("display");
}

function sortTable(n) {
    if (document.getElementById(n).className == "th-sort-desc") {
        document.getElementById(n).className = "th-sort-asc";
    }
    else {
        document.getElementById(n).className = "th-sort-desc";
    }

    var table = document.getElementsByTagName("table")[0];
    var rows, i, x, y, count = 0;
    var switching = true;

    // Order is set as ascending
    var direction = "ascending";

    // Run loop until no switching is needed
    while (switching) {
        switching = false;
        var rows = table.rows;

        //Loop to go through all rows
        for (i = 1; i < (rows.length - 1); i++) {
            var Switch = false;

            // Fetch 2 elements that need to be compared
            x = rows[i].getElementsByTagName("TD")[n].innerHTML;
            y = rows[i + 1].getElementsByTagName("TD")[n].innerHTML;

            if (n == 3 || n == 4) {
                x = Number(x.replace(/\D/g,''))
                y = Number(y.replace(/\D/g,''))
            }

            // Check the direction of order
            if (direction == "ascending") {
                if (isNaN(x)) {
                    // Check if 2 rows need to be switched
                    if (x.toLowerCase() > y.toLowerCase()) {
                        // If yes, mark Switch as needed and break loop
                        Switch = true;
                        break;
                    }
                }
                else {
                    if (Number(x) > Number(y)) {
                        Switch = true;
                        break;
                    }
                }
            }

            else if (direction == "descending") {
                if (isNaN(x)) {
                if (x.toLowerCase() < y.toLowerCase())
                    {
                        // If yes, mark Switch as needed and break loop
                        Switch = true;
                        break;
                    }
                }

                else {
                    if (Number(x) < Number(y)) {
                        Switch = true;
                        break;
                    }
                }
            }
        }
        if (Switch) {
            // Function to switch rows and mark switch as completed
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;

            // Increase count for each switch
            count++;
        } else {
            // Run while loop again for descending order
            if (count == 0 && direction == "ascending") {
                direction = "descending";
                switching = true;
            }
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