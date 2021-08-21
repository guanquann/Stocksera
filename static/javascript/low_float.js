function update_table() {
    var rows = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    var header_td = rows[0]
    header_td.innerHTML = `
        <th onclick="sortTable(0)" class="th-sort-desc" id='0'>Rank</th>
        <th onclick="sortTable(1)" class="th-sort-desc" id='1'>Ticker</th>
        <th onclick="sortTable(2)" class="th-sort-desc" id='2'>Company</th>
        <th onclick="sortTable(3)" class="th-sort-desc" id='3'>Exchange</th>
        <th onclick="sortTable(4)" class="th-sort-desc" id='4'>Previous Close</th>
        <th onclick="sortTable(5)" class="th-sort-desc" id='5'>1 Day Change %</th>
        <th onclick="sortTable(6)" class="th-sort-desc" id='6'>Floating Shares</th>
        <th onclick="sortTable(7)" class="th-sort-desc" id='7'>Outstanding Shares</th>
        <th onclick="sortTable(8)" class="th-sort-desc" id='8'>Short Interest</th>
        <th onclick="sortTable(9)" class="th-sort-desc" id='9'>Market Cap</th>
        <th onclick="sortTable(10)" class="th-sort-desc" id='10'>Industry</th>`

    for (i=1; i<rows.length; i++) {
        var td = rows[i].querySelectorAll("td");
        img_url = `https://g.foolcdn.com/art/companylogos/mark/${td[1].innerHTML}.png`
        td[1].innerHTML = `<a href="/ticker/?quote=${td[1].innerHTML}" target="_blank"><img src=${img_url} class="table_ticker_logo" onerror="this.error=null;load_table_error_img(this, '${td[1].innerHTML}')"><b>${td[1].innerHTML}</b></a>`;
        td[4].innerHTML = "$" + td[4].innerHTML;
        td[5].innerHTML = td[5].innerHTML + "%";
        if (td[5].innerHTML.includes("-")) {
            td[5].style.color = "red"
        }
        else {
            td[5].style.color = "green"
        }
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
            x = rows[i].getElementsByTagName("TD")[n].innerHTML.replace("$", "").replace("%", "");
            y = rows[i + 1].getElementsByTagName("TD")[n].innerHTML.replace("$", "").replace("%", "");


            // If column is floating/outstanding shares
            if (n == 6 || n == 7 || n == 9) {
                x = rows[i].getElementsByTagName("TD")[n].innerHTML
                y = rows[i + 1].getElementsByTagName("TD")[n].innerHTML
                if (x.includes("B")) {
                    x = Number(x.replace("B", "")) * 1000000000
                }
                else if (x.includes("M")) {
                    x = Number(x.replace("M", "")) * 1000000
                }
                else if (x.includes("K")) {
                    x = Number(x.replace("K", "")) * 1000
                }
                else {
                    x = Number(x)
                }

                if (y.includes("B")) {
                    y = Number(y.replace("B", "")) * 1000000000
                }
                else if (y.includes("M")) {
                    y = Number(y.replace("M", "")) * 1000000
                }
                else if (y.includes("K")) {
                    y = Number(y.replace("K", "")) * 1000
                }
                else {
                    y = Number(y)
                }
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