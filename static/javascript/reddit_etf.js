function sortTable(n) {
    if (document.getElementById(n).className == "th-sort-desc") {
        document.getElementById(n).className = "th-sort-asc";
    }
    else {
        document.getElementById(n).className = "th-sort-desc";
    }

    var table = document.getElementById("previous_trades");
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
                }}

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
let filter_table = elem.parentElement.querySelector("table");
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

function check_table() {
    var current_trade_tr = document.getElementById("current_trade").querySelectorAll("tr");
    for (i=1; i<current_trade_tr.length; i++) {
        var td = current_trade_tr[i].querySelectorAll("td");
        if (td[5].innerHTML.includes("-")) {
            td[5].innerHTML = td[5].innerHTML.replace("-", "-$");
            td[5].style.color = "red";
            td[6].style.color = "red";
        }
        else {
            td[5].innerHTML = "$" + td[5].innerHTML;
            td[6].innerHTML = "+" + td[6].innerHTML;
            td[5].style.color = "green";
            td[6].style.color = "green";
        }
    }

    var previous_trades_tr = document.getElementById("previous_trades").querySelectorAll("tr");
    var positive_trade = 0, negative_trade = 0
    for (i=1; i<previous_trades_tr.length; i++) {
        var td = previous_trades_tr[i].querySelectorAll("td");
        if (td[6].innerHTML.includes("-")) {
            td[6].innerHTML = td[6].innerHTML.replace("-", "-$");
            td[6].style.color = "red";
            td[7].style.color = "red";
            negative_trade += 1;
        }
        else {
            td[6].innerHTML = "+$" + td[6].innerHTML;
            td[7].innerHTML = "+" + td[7].innerHTML;
            td[6].style.color = "green";
            td[7].style.color = "green";
            positive_trade += 1;
        }
    }

    var win_rate = Math.round(10000 * (positive_trade / (positive_trade + negative_trade))) / 100
    document.getElementsByClassName("previous_trades_stats")[0].innerHTML = `<div class="previous_stats_div"><div>Profit: ${positive_trade}</div><div>Lose: ${negative_trade}</div><div>Win Rate: ${win_rate}%</div></div>`

    table_titles = document.getElementsByClassName("table_title");
    for (i=0; i<table_titles.length; i++) {
        table_title = table_titles[i].querySelector("span");
        if (table_title.innerHTML.includes("-")) {
            table_title.style.color = "red";
            table_title.innerHTML = table_title.innerHTML.replace("-", "-$");
        }
        else {
            table_title.style.color = "green";
            table_title.innerHTML = "+$" + table_title.innerHTML;
        }
    }
}