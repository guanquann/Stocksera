function check_table() {
    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");

    var header_td = tr[0]
    header_td.innerHTML = `
        <th onclick="sortTable(0)" class="th-sort-desc" id='0'>Symbol</th>
        <th onclick="sortTable(1)" class="th-sort-desc" id='1'>Name</th>
        <th onclick="sortTable(2)" class="th-sort-desc" id='2'>Price</th>
        <th onclick="sortTable(3)" class="th-sort-desc" id='3'>Change</th>
        <th onclick="sortTable(4)" class="th-sort-desc" id='4'>% Change</th>
        <th onclick="sortTable(5)" class="th-sort-desc" id='5'>Volume</th>
        <th onclick="sortTable(6)" class="th-sort-desc" id='6'>Avg Volume (3 months)</th>
        <th onclick="sortTable(7)" class="th-sort-desc" id='7'>Market Cap</th>
        <th onclick="sortTable(8)" class="th-sort-desc" id='8'>PE Ratio (TTM)</th>`

    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td");
        td[2].innerHTML = "$" + td[2].innerHTML
        if (td[3].innerHTML.includes("-")) {
            td[3].style.color = "red";
            td[3].innerHTML = "-$" + td[3].innerHTML.replace("-", "");
            td[4].style.color = "red";
        }
        else {
            td[3].style.color = "green";
            td[3].innerHTML = "+$" + td[3].innerHTML;
            td[4].style.color = "green";
        }
    }
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


            // If column is volume/market cap
            if (n == 5 || n == 6 || n == 7) {
                x = rows[i].getElementsByTagName("TD")[n].innerHTML
                y = rows[i + 1].getElementsByTagName("TD")[n].innerHTML
                if (x.includes("B")) {
                    x = Number(x.replace("B", "")) * 1000000000
                }
                else if (x.includes("M")) {
                    x = Number(x.replace("M", "")) * 1000000
                }
                else {
                    x = 9999999999
                }

                if (y.includes("B")) {
                    y = Number(y.replace("B", "")) * 1000000000
                }
                else if (y.includes("M")) {
                    y = Number(y.replace("M", "")) * 1000000
                }
                else {
                    y = 9999999999
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