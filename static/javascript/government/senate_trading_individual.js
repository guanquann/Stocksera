function load_individual_table() {
    var tr = document.querySelector("table").querySelectorAll("tr")
    total_amount = 0, owner_dict = {}, type_dict = {}, amount_breakdown_dict = {}, ticker_amount_breakdown_dict = {}, transaction_date_dict = {}, ticker_dict = {}, net_amount = 0
    for (i=0; i<tr.length; i++) {
        td = tr[i].children
        td[1].style.display = "none"
        td[3].style.display = "none"
        td[4].style.display = "none"
        td[7].style.display = "none"
        if (i > 0) {
            transaction_date = td[0].innerHTML.slice(0, 7)
            if (transaction_date_dict.hasOwnProperty(transaction_date)) {
                transaction_date_dict[transaction_date] += 1
            }
            else {
                transaction_date_dict[transaction_date] = 1
            }

            owner = td[1].innerHTML
            if (owner_dict.hasOwnProperty(owner)) {
                owner_dict[owner] += 1
            }
            else {
                owner_dict[owner] = 1
            }

            purchase_type = td[5].innerHTML
            if (type_dict.hasOwnProperty(purchase_type)) {
                type_dict[purchase_type] += 1
            }
            else {
                type_dict[purchase_type] = 1
            }

            raw_amount = td[6].innerHTML

            if (raw_amount != "Unknown") {
                num_list = raw_amount.split("- $")
                formatted_amount = Math.round(Number(num_list[1].replace(/\D/g,'')) - Number(num_list[0].replace(/\D/g,'')) / 2)
            }
            else {
                formatted_amount = 0
            }

            if (amount_breakdown_dict.hasOwnProperty(raw_amount)) {
                amount_breakdown_dict[raw_amount] += 1
            }
            else {
                amount_breakdown_dict[raw_amount] = 1
            }
            total_amount += formatted_amount

            if (purchase_type.includes("Sale")) {
                formatted_amount *= -1
            }
            net_amount += formatted_amount

            ticker = td[2].innerHTML
            if (ticker_dict.hasOwnProperty(ticker)) {
                ticker_dict[ticker] += 1
                ticker_amount_breakdown_dict[ticker] += formatted_amount
            }
            else {
                ticker_dict[ticker] = 1
                ticker_amount_breakdown_dict[ticker] = formatted_amount
            }
        }
        td[2].innerHTML = `<td><a href="/senate/?quote=${td[2].innerHTML}"><b>${td[2].innerHTML}</b></td>`
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

    div = document.createElement("div");
    div.classList.add("chart-container")
    canvas = document.createElement("canvas")
    canvas.setAttribute("id", "owner_breakdown");
    div.appendChild(canvas)
    daily_summary_div.appendChild(div)
    var owner_breakdown = document.getElementById('owner_breakdown');
    var owner_breakdown = new Chart(owner_breakdown, {
        type: 'pie',
        data: {
            labels: Object.keys(owner_dict),
            datasets: [{
                data: Object.values(owner_dict),
                backgroundColor: backgroundColorList,
                hoverOffset: 10
            }]
        },
        options: {
            title: {
                display: true,
                text: "Traded By",
                padding: 0,
                position: "top",
                fontSize: 15,
                fontStyle: "bold"
            },
            responsive: true,
            maintainAspectRatio: false,
        }
    })

    div = document.createElement("div");
    div.classList.add("chart-container")
    canvas = document.createElement("canvas")
    canvas.setAttribute("id", "amount_breakdown");
    div.appendChild(canvas)
    daily_summary_div.appendChild(div)
    var amount_breakdown = document.getElementById('amount_breakdown');
    var amount_breakdown = new Chart(amount_breakdown, {
        type: 'pie',
        data: {
            labels: Object.keys(amount_breakdown_dict),
            datasets: [{
                data: Object.values(amount_breakdown_dict),
                backgroundColor: backgroundColorList,
                hoverOffset: 10
            }]
        },
        options: {
            title: {
                display: true,
                text: "Amount Breakdown",
                padding: 0,
                position: "top",
                fontSize: 15,
                fontStyle: "bold"
            },
            responsive: true,
            maintainAspectRatio: false,
        }
    })

    div = document.createElement("div");
    div.classList.add("chart-container")
    canvas = document.createElement("canvas")
    canvas.setAttribute("id", "ticker_amount_breakdown");
    div.appendChild(canvas)
    daily_summary_div.appendChild(div)
    var ticker_amount_breakdown = document.getElementById('ticker_amount_breakdown');
    var ticker_amount_breakdown = new Chart(ticker_amount_breakdown, {
        type: 'bar',
        data: {
            labels: Object.keys(ticker_amount_breakdown_dict),
            datasets: [{
                label: "Amount",
                data: Object.values(ticker_amount_breakdown_dict),
                backgroundColor: "rgb(38, 166, 154)",
                hoverOffset: 10
            }]
        },
        options: {
            title: {
                display: true,
                text: "Ticker Breakdown",
                padding: 0,
                position: "top",
                fontSize: 15,
                fontStyle: "bold"
            },
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
                            zeroLineColor: "grey",
                            zeroLineWidth: 1
                        },
                        type: "linear",
                        scaleLabel: {
                            display: true,
                            labelString: 'Amount [$]',
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return Number(value).toLocaleString();
                            },
                            beginAtZero: true,
                        }
                    }],

                xAxes: [{
                    offset: true,
                    ticks: {
                        maxTicksLimit: 10,
                        maxRotation: 30,
                        minRotation: 0,
                    },
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
                        var label = data.datasets[tooltipItem.datasetIndex].label;
                        return 'Amount: $' + Number(value).toLocaleString();
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

    div = document.createElement("div");
    div.classList.add("chart-container")
    canvas = document.createElement("canvas")
    canvas.setAttribute("id", "transaction_breakdown");
    div.appendChild(canvas)
    daily_summary_div.appendChild(div)
    var transaction_breakdown = document.getElementById('transaction_breakdown');
    var transaction_breakdown = new Chart(transaction_breakdown, {
        type: 'bar',
        data: {
            labels: Object.keys(transaction_date_dict),
            datasets: [{
                label: "Count",
                data: Object.values(transaction_date_dict),
                backgroundColor: "rgb(38, 166, 154)",
                hoverOffset: 10
            }]
        },
        options: {
             title: {
                display: true,
                text: "Number Transactions (By Month)",
                padding: 0,
                position: "top",
                fontSize: 15,
                fontStyle: "bold"
            },
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
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return value;
                            },
                            beginAtZero: true,
                        }
                    }],

                xAxes: [{
                    type: "time",
                    distribution: 'series',
                    time: {
                        unit: "month"
                    },
                    offset: true,
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                    ticks: {
                        maxTicksLimit: 6,
                        maxRotation: 30,
                        minRotation: 0,
                    },
                    stacked: true
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

    div = document.createElement("div");
    div.classList.add("chart-container")
    canvas = document.createElement("canvas")
    canvas.setAttribute("id", "ticker_breakdown");
    div.appendChild(canvas)
    daily_summary_div.appendChild(div)
    var ticker_breakdown = document.getElementById('ticker_breakdown');
    var ticker_breakdown = new Chart(ticker_breakdown, {
        type: 'bar',
        data: {
            labels: Object.keys(ticker_dict),
            datasets: [{
                label: "Count",
                data: Object.values(ticker_dict),
                backgroundColor: "rgb(38, 166, 154)",
                hoverOffset: 10
            }]
        },
        options: {
             title: {
                display: true,
                text: "Number Transactions (By Ticker)",
                padding: 0,
                position: "top",
                fontSize: 15,
                fontStyle: "bold"
            },
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
                        },
                        ticks: {
                            beginAtZero: true,
                        }
                    }],

                xAxes: [{
                    offset: true,
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                    ticks: {
                        maxTicksLimit: 10,
                        maxRotation: 30,
                        minRotation: 0,
                    },
                    stacked: true
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
            <h2>${Object.keys(ticker_dict).length}</h2>
            <div>Companies</div>
        </div>
    `
}