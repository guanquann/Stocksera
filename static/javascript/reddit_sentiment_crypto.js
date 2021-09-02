function load_graph() {
    var tr = document.getElementById("reddit_table").querySelectorAll("tr")
    var list_24_48H = [], list_24H = [], ticker_list = []
    for (i=1; i<tr.length; i++) {
        var td = tr[i].querySelectorAll("td")
        ticker_list.push(td[1].querySelector("b").innerHTML)
        list_24H.push(Number(td[3].innerHTML))
        list_24_48H.push(Number(td[4].innerHTML))
    }

    subreddit_chart = document.getElementById('subreddit_chart');
    subreddit_chart = new Chart(subreddit_chart, {
        data: {
            labels: ticker_list,
            datasets: [
                {
                    label: '24H Score',
                    type: 'bar',
                    data: list_24H,
                    backgroundColor: 'rgb(38, 166, 154)',
                },
                {
                    label: '24 - 48H Score',
                    type: 'bar',
                    data: list_24_48H,
                    backgroundColor: 'orange',
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true
             },
            scales: {
                yAxes: [{
                        gridLines: {
                            display: false
                        },
                        type: "linear",
                        stacked: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Total Score',
                            beginAtZero: true,
                        },
                    }],

                xAxes: [{
                    offset: true,
                    gridLines: {
                        drawOnChartArea: false
                    },
                    stacked: true
                }],
            },

            // To show value when hover on any part of the graph
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'index',
                intersect: false
            },
            elements: {
                line: {
                    tension: 0
                },
                point:{
                    radius: 0
                }
            },
        },
    });
}

function check_table() {
    var table = document.getElementById("reddit_table");
    for (i = 0; i < (table.rows.length - 1); i++) {
        row = table.getElementsByTagName('tbody')[0].rows[i]
        var score_change = row.cells[5]
        if (!score_change.innerHTML.includes("N/A")) {
            if (score_change.innerText.includes("-")) {
                score_change.style.color = "red";
                score_change.innerText = score_change.innerText + "%";
            }
            else if (score_change.innerText == "0%") {
                score_change.style.color = "#9e9e9e";
                score_change.innerText = score_change.innerText + "%";
            }
            else {
                score_change.style.color = "green";
                score_change.innerText = score_change.innerText + "%";
            }
        }

        var prev_close = row.cells[10];
        if (prev_close.innerText != "N/A") {
            prev_close.innerText = "$" + prev_close.innerText;
        }

        var one_day_price = row.cells[13];
        if (one_day_price.innerText.includes("-")) {
            one_day_price.innerText = one_day_price.innerText + "%";
            one_day_price.style.color = "red";
        }
        else if (one_day_price.innerText != "N/A") {
            one_day_price.innerText = one_day_price.innerText + "%";
            one_day_price.style.color = "green";
        }

        var fifty_day_price = row.cells[14];
        if (fifty_day_price.innerText.includes("-")) {
            fifty_day_price.innerText = fifty_day_price.innerText + "%";
            fifty_day_price.style.color = "red";
        }
        else if (fifty_day_price.innerText != "N/A") {
            fifty_day_price.innerText = fifty_day_price.innerText + "%";
            fifty_day_price.style.color = "green";
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
        for (col_name=1; col_name <= 14; col_name ++) {
            tr[i].children[col_name].style.removeProperty("display");
        }
    }

    document.getElementById("search_ticker").value = ""

}

const searchTicker = () =>{
let filter = document.getElementById('search_ticker').value.toUpperCase();
let filter_table = document.getElementById('reddit_table');
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

function toggle_settings(elem) {
    var filter_description = document.getElementsByClassName("filter_description")[0];
    var filter_contents = document.getElementsByClassName("filter_contents");
    var search_ticker = document.getElementById("search_ticker");
    if (elem.innerHTML == "Collapse Toolkit") {
        elem.innerHTML = "Expand Toolkit";
        filter_description.style.display = "none";
        search_ticker.style.display = "none";
        for (i=0; i<filter_contents.length; i++) {
            filter_contents[i].style.display = "none";
        }
    }
    else {
        elem.innerHTML = "Collapse Toolkit";
        filter_description.style.removeProperty("display");
        search_ticker.style.removeProperty("display");
        for (i=0; i<filter_contents.length; i++) {
            filter_contents[i].style.removeProperty("display");
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

            // If column is volume/market cap/supply
            if (n == 11 || n == 12 || n == 15) {
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
