function load_usa_chart(district, district_count, gov_type) {
    if (gov_type == "house") {
        usa_chart_div = document.getElementById("usa_chart_div")

        h2 = document.createElement("h2");
        h2.appendChild(document.createTextNode('Summary By State'));
        usa_chart_div.appendChild(h2)

        div = document.createElement("div");
        div.appendChild(document.createTextNode('Click on state for more information'));
        div.classList.add("state_more_info")
        usa_chart_div.appendChild(div)

        div = document.createElement("div");
        div.classList.add("usa-chart-container")
        div.setAttribute("id", "usa_chart");
        usa_chart_div.appendChild(div)

        var data = [{
            type: 'choropleth',
            showscale: false,
            showlegend: false,
            locationmode: 'USA-states',
            locations: district,
            z: district_count,
            customdata: district,
            hovertemplate:
                    "<b>%{location}</b><br>" +
                    "Count: %{z}<br>" +
                    "<extra></extra>",
            zmin: 0,
            zmax: 700,
            colorscale: [
                [0, 'rgb(242,240,247)'],
                [0.2, 'rgb(218,218,235)'],
                [0.4, 'rgb(188,189,220)'],
                [0.6, 'rgb(158,154,200)'],
                [0.8, 'rgb(117,107,177)'],
                [1, 'rgb(84,39,143)']
            ],
            marker: {
                line:{
                color: 'black',
                width: 1
                }
            }
        }];

        var layout = {
            autosize: true,
            margin: {
                t:0,
                l:0,
                r:0,
                pad: 0
            },
            automargin: true,
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            geo:{
                scope: 'usa',
                showlakes: false,
                lakecolor: 'red',
                bgcolor: '#dbeafe'
            }
        };

        Plotly.newPlot("usa_chart", data, layout, {displayModeBar: false, showTips: false, responsive: false});

        usa_chart = document.querySelector("#usa_chart")
        usa_chart.on('plotly_click', function(data){
            map_location = data.points[0]["location"]
            location.href = `?state=${map_location}`
        });
    }
}

function load_individual_table(gov_type) {
    var tr = document.querySelector("table").querySelectorAll("tr")
    total_amount = 0, type_dict = {}, amount_breakdown_dict = {}, ticker_amount_breakdown_dict = {}, transaction_date_dict = {}, ticker_dict = {}, net_amount = 0
    representative_dict = {}
    representative_trans_dict = {}
    transaction_date_list = []
    for (i=0; i<tr.length; i++) {
        td = tr[i].children
        td[1].style.display = "none"
        td[3].style.display = "none"
        td[4].style.display = "none"
        td[8].style.display = "none"
        td[10].style.display = "none"
        td[11].style.display = "none"

        if (i > 0) {
            representative = td[7].innerHTML
            if (representative_dict.hasOwnProperty(representative)) {
                representative_dict[representative] += 1
            }
            else {
                representative_dict[representative] = 1
                representative_trans_dict[representative] = {}
            }

            transaction_date = td[0].innerHTML.slice(0, 7)
            if (transaction_date == "Unknown") {
                continue
            }
            else if (! transaction_date_list.includes(transaction_date)) {
                transaction_date_list.push(transaction_date)
            }

            if (transaction_date_dict.hasOwnProperty(transaction_date)) {
                transaction_date_dict[transaction_date] += 1
            }
            else {
                transaction_date_dict[transaction_date] = 1
            }

            if (representative_trans_dict[representative].hasOwnProperty(transaction_date) && transaction_date) {
                representative_trans_dict[representative][transaction_date] += 1
            }
            else {
                representative_trans_dict[representative][transaction_date] = 1
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
                if (num_list.length == 2) {
                    formatted_amount = Math.round(Number(num_list[1].replace(/\D/g,'')) - Number(num_list[0].replace(/\D/g,'')) / 2)
                }
                else {
                    formatted_amount = Number(num_list[0].replace(/\D/g,''))
                }
            }
            else {
                formatted_amount = 0
            }

            if (amount_breakdown_dict.hasOwnProperty(representative)) {
                amount_breakdown_dict[representative] += formatted_amount
            }
            else {
                amount_breakdown_dict[representative] = formatted_amount
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

            td[2].innerHTML = `<td><a href="/${gov_type}/?quote=${td[2].innerHTML}"><b>${td[2].innerHTML}</b></td>`
            td[7].innerHTML = `<td><a href="/${gov_type}/?person=${td[7].innerHTML}"><b>${td[7].innerHTML}</b></td>`
        }
    }

    dataset_list = []
    count = 0
    for (i in representative_trans_dict) {
        data_list = []
        num_transactions_by_person = representative_trans_dict[i]
        for (date of transaction_date_list) {
            if (num_transactions_by_person.hasOwnProperty(date)) {
                data_list.push({x: date, y: num_transactions_by_person[date]})
            }
            else {
                data_list.push({x: date, y: 0})
            }
        }
        dataset_list.push({
            label: i,
            data: data_list,
            backgroundColor: backgroundColorList[count]
        })
        count += 1
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
            legend: {
                display: false
            },
            responsive: true,
            maintainAspectRatio: false,
        }
    })

    div = document.createElement("div");
    div.classList.add("chart-container")
    canvas = document.createElement("canvas")
    canvas.setAttribute("id", "representative_breakdown");
    div.appendChild(canvas)
    daily_summary_div.appendChild(div)
    var owner_breakdown = document.getElementById('representative_breakdown');
    var owner_breakdown = new Chart(owner_breakdown, {
        type: 'pie',
        data: {
            labels: Object.keys(representative_dict),
            datasets: [{
                data: Object.values(representative_dict),
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
            legend: {
                display: false
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
            legend: {
                display: false
            },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, data) {
                        var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        var label = data["labels"][tooltipItem.index]
                        return label + ': $' + Number(value).toLocaleString();
                    }
                }
            },
            responsive: true,
            maintainAspectRatio: false,
        }
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
                display: false
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

    daily_summary_big_div = document.getElementById("graph_big_div")

//    div = document.createElement("div");
//    div.classList.add("chart-container-big")
//    canvas = document.createElement("canvas")
//    canvas.setAttribute("id", "ticker_amount_breakdown");
//    div.appendChild(canvas)
//    daily_summary_big_div.appendChild(div)
//    var ticker_amount_breakdown = document.getElementById('ticker_amount_breakdown');
//    var ticker_amount_breakdown = new Chart(ticker_amount_breakdown, {
//        type: 'bar',
//        data: {
//            labels: Object.keys(ticker_amount_breakdown_dict),
//            datasets: [{
//                label: "Amount",
//                data: Object.values(ticker_amount_breakdown_dict),
//                backgroundColor: "rgb(38, 166, 154)",
//                hoverOffset: 10
//            }]
//        },
//        options: {
//            title: {
//                display: true,
//                text: "Ticker Breakdown",
//                padding: 0,
//                position: "top",
//                fontSize: 15,
//                fontStyle: "bold"
//            },
//            responsive: true,
//            maintainAspectRatio: false,
//            legend: {
//                display: false
//            },
//            scales: {
//                yAxes: [{
//                        position: 'left',
//                        gridLines: {
//                            color: "transparent",
//                            display: true,
//                            zeroLineColor: "grey",
//                            zeroLineWidth: 1
//                        },
//                        type: "linear",
//                        scaleLabel: {
//                            display: true,
//                            labelString: 'Amount [$]',
//                        },
//                        ticks: {
//                            callback: function(value, index, values) {
//                                return Number(value).toLocaleString();
//                            },
//                            beginAtZero: true,
//                        }
//                    }],
//
//                xAxes: [{
//                    offset: true,
//                    ticks: {
//                        maxTicksLimit: 10,
//                        maxRotation: 30,
//                        minRotation: 0,
//                    },
//                    gridLines: {
//                        color: "transparent",
//                        display: true,
//                        zeroLineColor: "grey",
//                        zeroLineWidth: 1
//                    },
//                }],
//            },
//            tooltips: {
//                mode: 'index',
//                intersect: false,
//                callbacks: {
//                    label: function(tooltipItem, data) {
//                        var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
//                        var label = data.datasets[tooltipItem.datasetIndex].label;
//                        return 'Amount: $' + Number(value).toLocaleString();
//                    }
//                }
//            },
//            hover: {
//                mode: 'index',
//                intersect: false
//            },
//            elements: {
//                line: {
//                    tension: 0
//                },
//                point:{
//                    radius: 0
//                }
//            },
//        },
//    })

    div = document.createElement("div");
    div.classList.add("chart-container-big")
    canvas = document.createElement("canvas")
    canvas.setAttribute("id", "transaction_breakdown");
    div.appendChild(canvas)
    daily_summary_big_div.appendChild(div)
    var transaction_breakdown = document.getElementById('transaction_breakdown');
    var transaction_breakdown = new Chart(transaction_breakdown, {
        type: 'bar',
        data: {
            labels: transaction_date_list,
            datasets: dataset_list
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

function resize_plotly_graph() {
    Plotly.Plots.resize('usa_chart')
}