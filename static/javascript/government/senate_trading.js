const searchSenator = (elem, index) =>{
let filter = elem.value.toUpperCase();
let filter_table = elem.parentElement.parentElement.querySelector("table");
let tr = filter_table.getElementsByTagName('tr');
for (var i = 0; i < tr.length; i++){
    let td = tr[i].getElementsByTagName('td')[index];
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

// Adapted from https://github.com/niinpatel/calendarHTML-Javascript/blob/master/scripts.js
today = new Date();
//currentMonth = today.getMonth();
//currentYear = today.getFullYear();
selectYear = document.getElementById("year");
selectMonth = document.getElementById("month");

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
backgroundColorList = ['rgb(38, 166, 154)', 'red', 'orange', 'yellow', 'blue', 'purple', 'pink', 'grey', 'green']

monthAndYear = document.getElementById("monthAndYear");
dates_available = document.getElementById("dates_available").innerHTML;

original_date_selected = document.getElementById("date_selected").innerHTML;
original_date_selected_split = original_date_selected.split("-")
original_date_split = original_date_selected.split("-")
originalMonth = Number(original_date_split[1]) - 1;
originalYear = Number(original_date_split[0]);
originalDate = Number(original_date_split[2]);

date_selected = document.getElementById("date_selected").innerHTML;
date_split = date_selected.split("-")
currentMonth = Number(date_split[1]) - 1;
currentYear = Number(date_split[0]);
showCalendar(currentMonth, currentYear);


function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear);
}

function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear);
}

function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    showCalendar(currentMonth, currentYear);
}

function showCalendar(month, year) {
    let firstDay = (new Date(year, month)).getDay();

    tbl = document.getElementById("calendar-body"); // body of the calendar

    // clearing all previous cells
    tbl.innerHTML = "";

    // filing data about month and in the page via DOM.
    monthAndYear.innerHTML = months[month] + " " + year;
    selectYear.value = year;
    selectMonth.value = month;

    // creating all cells
    let date = 1;
    for (let i = 0; i < 6; i++) {
        // creates a table row
        let row = document.createElement("tr");

        //creating individual cells, filing them up with data.
        for (let j = 0; j < 7; j++) {
            if (i === 0 && j < firstDay) {
                cell = document.createElement("td");
                cellText = document.createTextNode("");
                cell.appendChild(cellText);
                row.appendChild(cell);
            }
            else if (date > daysInMonth(month, year)) {
                break;
            }

            else {
                cell = document.createElement("td");
                cellText = document.createTextNode(date);
                if (date === today.getDate() && year === today.getFullYear() && month === today.getMonth()) {
                    cell.classList.add("bg-today");
                }
                if (date === originalDate && month === originalMonth && year === originalYear) {
                    cell.classList.add("bg-selected");
                }

                date_ = (date <= 9) ? "0" + date : date;
                month_ = (month <= 8) ? "0" + (month+1) : month+1;
                actual_date = `${year}-${month_}-${date_}`

                if (dates_available.includes(actual_date)) {
                    cell.classList.add("bg-info");
                }
                cell.classList.add("hoverable");
                cell.setAttribute("onclick",`get_clicked_date('${actual_date}')`);
                cell.appendChild(cellText);

                row.appendChild(cell);
                date++;
            }
        }
        tbl.appendChild(row); // appending each row into calendar body.
    }
}

// check how many days in a month code from https://dzone.com/articles/determining-number-days-month
function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}
// End of https://github.com/niinpatel/calendarHTML-Javascript/blob/master/scripts.js


function get_clicked_date(elem) {
    document.getElementById("date_selected_from_calendar").value = elem
    document.getElementById("form").submit()
}

function load_overview_table() {
    var tr = document.querySelectorAll("table")[1].querySelectorAll("tr")
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        td[0].innerHTML = `<td><a href="/senate/?senator=${td[0].innerHTML}"><b>${td[0].innerHTML}</b></td>`
    }
}

function load_ticker_stats() {
    var tr = document.querySelectorAll("table")[2].querySelectorAll("tr")
    ticker_list = [], count_list = []
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        if (i < 50) {
            ticker_list.push(td[0].innerHTML)
            count_list.push(td[1].innerHTML)
        }
        td[0].innerHTML = `<a href="/senate?quote=${td[0].innerHTML}"><b>${td[0].innerHTML}</b></a>`
    }

    ticker_stats_div = document.getElementById("ticker_stats_div")
    div = document.createElement("div");
    div.classList.add("chart-container-summary")
    canvas = document.createElement("canvas")
    canvas.setAttribute("id", "ticker_stats");
    div.appendChild(canvas)
    ticker_stats_div.appendChild(div)
    var ticker_stats = document.getElementById('ticker_stats');
    var ticker_stats = new Chart(ticker_stats, {
        type: 'bar',
        data: {
            labels: ticker_list,
            datasets: [{
                label: "Count",
                data: count_list,
                backgroundColor: "rgb(38, 166, 154)",
                hoverOffset: 10
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
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        type: "linear",
                        scaleLabel: {
                            display: true,
                            labelString: 'Num of Transactions',
                            beginAtZero: true,
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return value;
                            },
                        }
                    }],

                xAxes: [{
                    offset: true,
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                }],
            },
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
    })
}

function load_daily_summary() {
    var tr = document.querySelectorAll("table")[3].querySelectorAll("tr")
    senator_dict = {}, type_dict = {}, ticker_list = [], net_amount = 0, total_amount = 0, transaction_dict = {}
    for (i=0; i<tr.length; i++) {
        td = tr[i].children
        td[1].style.display = "none"
        td[3].style.display = "none"
        td[4].style.display = "none"
        td[8].style.display = "none"
//        td[9].style.display = "none"
        if (i > 0) {
            type = td[5].innerHTML
            if (td[6].innerHTML.includes("$")) {
                num_list = td[6].innerHTML.split("- $")
                amount = Math.round(Number(num_list[1].replace(/\D/g,'')) - Number(num_list[0].replace(/\D/g,'')) / 2)
            }
            else {
                amount = 0
            }
            total_amount += amount
            if (type.includes("Sale")) {
                amount *= -1
            }
            net_amount += amount

            senator_name = td[7].innerHTML
            ticker = td[2].innerHTML
            if (! ticker_list.includes(ticker)) {
                ticker_list.push(ticker)
            }

            if (senator_dict.hasOwnProperty(senator_name)) {
                if (senator_dict[senator_name].hasOwnProperty(ticker)) {
                    senator_dict[senator_name][ticker] += amount
                }
                else {
                    senator_dict[senator_name][ticker] = amount
                }
            }
            else {
                senator_dict[senator_name] = {}
                senator_dict[senator_name][ticker] = amount
            }

            if (type_dict.hasOwnProperty(type)) {
                type_dict[type] += 1
                transaction_dict[type] += amount
            }
            else {
                type_dict[type] = 1
                transaction_dict[type] = amount
            }

            td[2].innerHTML = `<a href="/senate/?quote=${td[2].innerHTML}"><b>${td[2].innerHTML}</b></a>`
            td[7].innerHTML = `<a href="/senate/?senator=${senator_name}"><b>${senator_name}</b></a>`
        }
    }

    daily_summary_div = document.getElementById("graph_div")
    div = document.createElement("div");
    div.classList.add("chart-container")

    canvas = document.createElement("canvas")
    canvas.setAttribute("id", "type_breakdown");
    div.appendChild(canvas)

    daily_summary_div.appendChild(div)

    var type_breakdown = document.getElementById('type_breakdown');
    var type_breakdown = new Chart(type_breakdown, {
        type: 'pie',
        data: {
            labels: Object.keys(type_dict),
            datasets: [{
                data: Object.values(type_dict),
                backgroundColor: backgroundColorList,
                hoverOffset: 10
            }]
        },
        options: {
            title: {
                display: true,
                text: "Types of Trade",
                padding: 0,
                position: "top",
                fontSize: 15,
                fontStyle: "bold"
            },
            responsive: true,
            maintainAspectRatio: false,
        }
    })

    bg_count = 0
    dataset_list = []
    for (i in senator_dict) {
        data_list = []
        for (s in ticker_list) {
            looking_at = ticker_list[s]
            if (senator_dict[i].hasOwnProperty(looking_at)) {
                data_list.push({x: looking_at, y: senator_dict[i][looking_at]})
            }
            else {
                data_list.push({x: looking_at, y: 0})
            }
        }

        dataset_list.push({
            label: i,
            data: data_list,
            backgroundColor: backgroundColorList[bg_count]
        })
        bg_count += 1
    }

    if (Object.keys(senator_dict).length != 0) {
            senate_id = "senator_breakdown"

            div = document.createElement("div");
            div.classList.add("chart-container")

            canvas = document.createElement("canvas")
            canvas.setAttribute("id", senate_id);
            div.appendChild(canvas)

            daily_summary_div.appendChild(div)

            var senator_breakdown = document.getElementById(senate_id);
            var senator_breakdown = new Chart(senator_breakdown, {
            type: 'bar',
            data: {
                labels: ticker_list,
                datasets: dataset_list
            },
            options: {
                title: {
                    display: true,
                    text: "Breakdown by Ticker",
                    padding: 0,
                position: "top",
                    fontSize: 15,
                    fontStyle: "bold"
                },
                scaleShowValues: true,
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: true
                },
                scales: {
                    yAxes: [{
                            position: 'left',
                            gridLines: {
                                color: "transparent",
                                display: true,
                                drawBorder: false,
                                zeroLineColor: "grey",
                                zeroLineWidth: 1
                            },
                            type: "linear",
                            scaleLabel: {
                                display: true,
                                labelString: 'Amount [$]',
                            },
                            ticks: {
                                callback: function(value) {if (value% 1 === 0) {return Number(value).toLocaleString();}},
                                maxTicksLimit: 5,
                                beginAtZero: true,
                            },
                        }],

                    xAxes: [{
                        offset: true,
                        gridLines: {
                            color: "transparent",
                            display: true,
                            zeroLineColor: "grey",
                            zeroLineWidth: 1
                        },
                    }],
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(tooltipItem, data) {
                            var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                            return "Amount: ~$" + Number(value["y"]).toLocaleString()
                        }
                    }
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
        })

        num_senators = Object.keys(senator_dict).length
        num_transactions = tr.length - 1
        if (type_dict.hasOwnProperty("Purchase")) {
            num_purchases = type_dict["Purchase"]
            percent_purchases = Math.round((num_purchases / num_transactions) * 10000) / 100
        }
        else {
            percent_purchases = 0
        }

        document.getElementById("daily_statistics").innerHTML = `
            <div class="in_a_nutshell">
                <h2>${num_transactions}</h2>
                <div>Transaction(s)</div>
            </div>
            <div class="in_a_nutshell">
                <h2>${percent_purchases}</h2>
                <div>% Purchase</div>
            </div>
            <div class="in_a_nutshell">
                <h2>${Number(total_amount).toLocaleString()}</h2>
                <div>~ Total $ Traded</div>
            </div>
            <div class="in_a_nutshell">
                <h2>${Number(net_amount).toLocaleString()}</h2>
                <div>~ Net $ Traded</div>
            </div>
            <div class="in_a_nutshell">
                <h2>${ticker_list.length}</h2>
                <div>Companies</div>
            </div>
            <div class="in_a_nutshell">
                <h2>${num_senators}</h2>
                <div>Senator(s)</div>
            </div>
        `
    }
    else {
        document.getElementById("daily_summary_div").innerHTML = `
            <div style="text-align: center">
                <h2>No Trades Disclosed on <span id="date_selected">${date_selected}</span></h2>
                <br><br>
                <div>Not Found!</div>
                <br><br>
            </div>
            `
    }
}

function open_calendar() {
    calendar_class = document.querySelector(".calendar_div").classList
    calendar_btn = document.querySelector("#open_calendar")
    if (calendar_class.contains("hide_calendar")) {
        calendar_class.remove("hide_calendar")
        calendar_btn.innerHTML = "Hide Calendar"
    }
    else {
        calendar_class.add("hide_calendar")
        calendar_btn.innerHTML = "Open Calendar"
    }
}