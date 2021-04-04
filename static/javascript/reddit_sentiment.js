function check_table() {
    if (typeof(document.getElementsByTagName('td')[0].innerText) != "undefined") {
        document.getElementById("filter_section").style.removeProperty("display");
        document.getElementById("reddit_table_section").style.removeProperty("display");
    }

    var table = document.getElementById("reddit_table");
    for (i = 0; i < (table.rows.length - 1); i++) {
        var score_change = table.getElementsByTagName('tbody')[0].rows[i].cells[3]
        if (score_change.innerText.includes("-")) {
            score_change.style.color = "red";
        }
        else if (score_change.innerText == "0%") {
            score_change.style.color = "#9e9e9e";
        }
        else {
            score_change.style.color = "green";
        }

        var one_day_price = table.getElementsByTagName('tbody')[0].rows[i].cells[6];
        if (one_day_price.innerText.includes("-")) {
            one_day_price.innerText = one_day_price.innerText.replace("-", "-$");
            one_day_price.style.color = "red";
        }
        else {
            one_day_price.innerText = "$" + one_day_price.innerText;
            one_day_price.style.color = "green";
        }

        var fifty_day_price = table.getElementsByTagName('tbody')[0].rows[i].cells[7];
        if (fifty_day_price.innerText.includes("-")) {
            fifty_day_price.innerText = fifty_day_price.innerText.replace("-", "-$");
            fifty_day_price.style.color = "red";
        }
        else {
            fifty_day_price.innerText = "$" + fifty_day_price.innerText;
            fifty_day_price.style.color = "green";
        }

        var price_target = table.getElementsByTagName('tbody')[0].rows[i].cells[11];
        if (price_target.innerText != "N/A") {
            price_target.innerText = "$" + price_target.innerText;
        }

    }
}

function filter_table(elem) {
    filter_column = elem;

    var filter_column_id = filter_column["id"].split("-")[0]
    var filter_table = document.getElementById('reddit_table');
    var tr = filter_table.getElementsByTagName("tr");

    if (filter_column.innerHTML.includes("✖")) {
        filter_column.innerHTML = filter_column.innerHTML.replace("✖", "✔");
        filter_column.classList.add("filter_contents_removed");

        document.getElementById(filter_column_id.split("-")[0]).style.display = "none";
        for (i = 1; i < tr.length; i++) {
            tr[i].children[filter_column_id].style.display = "none";
        }
    }
    else {
        filter_column.innerHTML = filter_column.innerHTML.replace("✔", "✖");
        filter_column.classList.remove("filter_contents_removed");

        document.getElementById(filter_column_id.split("-")[0]).style.removeProperty("display");
        for (i = 1; i < tr.length; i++) {
            tr[i].children[filter_column_id].style.removeProperty("display");
        }
    }
}

function reset_table() {
    var filter_table = document.getElementById('reddit_table');
    var tr = filter_table.getElementsByTagName("tr");

    var filter_contents = document.getElementsByClassName("filter_contents");
    for (i = 0; i < filter_contents.length; i++) {
        filter_contents[i].innerHTML = filter_contents[i].innerHTML.replace("✔", "✖");
        filter_contents[i].classList.remove("filter_contents_removed");
    }

    for (i = 0; i < tr.length; i++) {
        for (col_name=0; col_name < 13; col_name ++) {
            tr[i].children[col_name].style.removeProperty("display");
        }
    }

    // document.getElementsByClassName("filter_contents")[1].innerHTML.replace("✔", "✖")
}

const searchTicker = () =>{
let filter = document.getElementById('search_ticker').value.toUpperCase();
let filter_table = document.getElementById('reddit_table');

let tr = filter_table.getElementsByTagName('tr');
for (var i = 0; i < tr.length; i++){
    let td = tr[i].getElementsByTagName('td')[0];
        if(td){
            let textValue = td.textContent || td.innerHTML;
            if(textValue.toUpperCase().indexOf(filter) > -1){
                tr[i].style.display="";
                }
            else {
                    tr[i].style.display="none";
                }
            }
        }

    }

function sortTable(n) {
    if (document.getElementById(n).className == "th-sort-desc")
        {
            document.getElementById(n).className = "th-sort-asc";
        }

    else
        {
        document.getElementById(n).className = "th-sort-desc";
        }

    var table = document.getElementById("reddit_table");
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

            // If column is volume/floating shares
            if (n == 5 || n == 8) {
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
                    x = 9999999999
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