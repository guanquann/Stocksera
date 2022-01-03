function load_ticker_table(gov_type) {
    tr = document.getElementsByTagName("table")[1].querySelectorAll("tr");
    date_list = [], close_list = [];
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        date_list.push(td[0].innerHTML)
        close_list.push(td[1].innerHTML)
    }

    var tr = document.querySelector("table").querySelectorAll("tr")
    type_dict = {}, amount_breakdown_dict = {}, transaction_date_dict = {}, senator_dict = {}, individual_amount_dict = {}
    buy_date_list = [], buy_price_list = [], sell_date_list = [], sell_price_list = []
    total_amount = 0, net_amount = 0

    for (i=0; i<tr.length; i++) {
        td = tr[i].children
        td[1].style.display = "none"
        td[2].style.display = "none"
        td[6].style.display = "none"
        if (i > 0) {
            purchase_type = td[3].innerHTML
            if (type_dict.hasOwnProperty(purchase_type)) {
                type_dict[purchase_type] += 1
            }
            else {
                type_dict[purchase_type] = 1
            }

            raw_amount = td[4].innerHTML
            num_list = raw_amount.split("- $")
            formatted_amount = Math.round(Number(num_list[1].replace(/\D/g,'')) - Number(num_list[0].replace(/\D/g,'')) / 2)
            if (amount_breakdown_dict.hasOwnProperty(raw_amount)) {
                amount_breakdown_dict[raw_amount] += 1
            }
            else {
                amount_breakdown_dict[raw_amount] = 1
            }

            transaction_date = td[0].innerHTML
            individual_amount_dict[transaction_date] = formatted_amount

            total_amount += formatted_amount
            if (purchase_type.includes("Sale")) {
                formatted_amount *= -1
            }
            net_amount += formatted_amount

            senator_name = td[5].innerHTML
            if (senator_dict.hasOwnProperty(senator_name)) {
                senator_dict[senator_name] += 1
            }
            else {
                senator_dict[senator_name] = 1
            }

            transaction_date_price = close_list[date_list.indexOf(transaction_date)]
            var d = new Date(transaction_date);
            disclosure_date_price = close_list[date_list.indexOf(d.toISOString().split('T')[0])]
            if (purchase_type.includes("Sale")) {
                color = "red"
                sell_date_list.push(transaction_date)
                sell_price_list.push(transaction_date_price)
            }
            else {
                color = "rgb(38, 166, 154)"
                buy_date_list.push(transaction_date)
                buy_price_list.push(transaction_date_price)
            }

            transaction_date = transaction_date.slice(0, 7)
            if (transaction_date_dict.hasOwnProperty(transaction_date)) {
                transaction_date_dict[transaction_date] += 1
            }
            else {
                transaction_date_dict[transaction_date] = 1
            }

            td[5].innerHTML = `<a href="/${gov_type}?person=${td[5].innerHTML}"><b>${td[5].innerHTML}</b></a>`
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

    var items = Object.keys(senator_dict).map(function(key) {
        return [key, senator_dict[key]];
    });

    items.sort(function(first, second) {
        return second[1] - first[1];
    });

    top_8_senator = [], top_8_amount = []
    others_amount = 0
    for (i in items) {
        if (top_8_amount.length < 7) {
            top_8_senator.push(items[i][0])
            top_8_amount.push(items[i][1])
        }
        else {
            others_amount += items[i][1]
        }
    }

    if (others_amount != 0) {
        top_8_senator.push("Others")
        top_8_amount.push(others_amount)
    }

    div = document.createElement("div");
    div.classList.add("chart-container")
    canvas = document.createElement("canvas")
    canvas.setAttribute("id", "senator_breakdown");
    div.appendChild(canvas)
    daily_summary_div.appendChild(div)
    var senator_breakdown = document.getElementById('senator_breakdown');
    var senator_breakdown = new Chart(senator_breakdown, {
        type: 'pie',
        data: {
            labels: top_8_senator,
            datasets: [{
                data: top_8_amount,
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

    var trace = {
        x: date_list,
        y: close_list,
        name: "Price",
        line: {'color': 'orange'},
        hovertemplate:
                "Price: $%{y}<br>" +
                "Date: %{x|%Y-%m-%d}" +
                "<extra></extra>",
        type: 'scatter'
    };

    var trace2 = {
        x: buy_date_list,
        y: buy_price_list,
        name: "Buy",
        mode: 'markers',
        line: {'color': 'rgb(38, 166, 154)'},
        hovertemplate:
                "Buy Price: ~$%{y}<br>" +
                "Date: %{x|%Y-%m-%d}" +
                "<extra></extra>",
        type: 'scatter'
    };

    var trace3 = {
        x: sell_date_list,
        y: sell_price_list,
        name: "Sell",
        mode: 'markers',
        line: {'color': 'red'},
        hovertemplate:
                "Sell Price: ~$%{y}<br>" +
                "Date: %{x|%Y-%m-%d}" +
                "<extra></extra>",
        type: 'scatter'
    };

    var trace4 = {
        x: Object.keys(individual_amount_dict),
        y: Object.values(individual_amount_dict),
        name: "Amount",
        hovertemplate:
                "Amount: ~$%{y}<br>" +
                "Date: %{x|%Y-%m-%d}" +
                "<extra></extra>",
        marker: {
            color: 'purple',
            opacity: 0.6,
            line: {
                color: 'purple'
            }
        },
        width: 10,
        type: 'bar',
        yaxis: 'y2',
    };

    var data = [trace, trace2, trace3, trace4];
    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:50,
            r:50,
            b: 40,
            pad: 0
        },
        automargin: true,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        xaxis: {
            showgrid: false,
            showline: true,
            color: "gray",
            rangemode: 'tozero',
            title: {
                text: "Date",
                font: {
                    size: 12
                }
            }
        },
        yaxis: {
            showgrid: false,
            showline: true,
            autorange: true,
            fixedrange: false,
            color: "gray",
            title: {
                text: 'Price [$]',
                font: {
                    size: 11,
                }
            },
        },
        yaxis2: {
            showgrid: false,
            showline: true,
            color: "gray",
            title: {
                text: 'Amount',
                font: {
                      size: 11,
                }
            },
            overlaying: 'y',
            side: 'right',
        },
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
            font: {
                size: 10,
            }
        },
    };

    Plotly.newPlot('price_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});

    num_transactions = tr.length - 1
    if (type_dict.hasOwnProperty("Purchase")) {
        num_purchases = type_dict["Purchase"]
        percent_purchases = Math.round((num_purchases / num_transactions) * 10000) / 100
    }
    else {
        percent_purchases = 0
    }
    last_transaction = Math.round((new Date() - new Date(tr[1].querySelector("td").innerHTML)) / (1000 * 60 * 60 * 24))
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
            <h2>${Object.keys(senator_dict).length}</h2>
            <div>Senator(s)</div>
        </div>
        <div class="in_a_nutshell">
            <h2>${last_transaction} days</h2>
            <div>Since Last Transaction</div>
        </div>
    `
}

function resize_plotly_graph() {
    Plotly.Plots.resize('price_chart')
}