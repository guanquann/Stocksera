var oi_chart = null;
var max_pain_chart = null;
var historical_chart = null;

var expiry_date_global = null;
var options_data_global = null;
var current_price_global = null;

var options_dict = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        yAxes: [{
            gridLines: {
                drawOnChartArea: false,
                color: "grey",
            },
            scaleLabel: {
                display: true,
                labelString: 'Volume',
                beginAtZero: false,
            },
        }],
        xAxes: [{
            ticks: {
                maxTicksLimit: 20,
                maxRotation: 45,
                minRotation: 0,
            },
            gridLines: {
                drawOnChartArea: false,
                color: "grey",
            },
            scaleLabel: {
                display: true,
                labelString: 'Strike [$]',
                beginAtZero: true,
            },
        }]
    },
    elements: {
        point: {
            radius: 0
        }
    },
    tooltips: {
        mode: 'index',
        intersect: false,
        callbacks: {
            label: function(tooltipItem, data) {
                var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                var label = data.datasets[tooltipItem.datasetIndex].label;
                return label + ': ' + Number(value).toLocaleString();
            }
        }
    },
    hover: {
        mode: 'index',
        intersect: false
    },
}

function generate_chart(new_date) {
    filtered_data = options_data_global.filter(x => x["expiration_date"] == new_date)

    var calls_oi_list = [], puts_oi_list = [];
    var strike_list = [];
    var calls_loss_list = [], puts_loss_list = [];

    var calls_itm = 0, calls_otm = 0, puts_itm = 0, puts_otm = 0, calls_oi = 0, puts_oi = 0;
    var next_itm_call_oi = 0, next_itm_call_strike = 0;

    var max_pain = 0;
    var min_loss = 9999999999999;

    for (var i=0; i<filtered_data.length; i++) {
        strike = filtered_data[i]["strike_price"]
        oi = filtered_data[i]["open_interest"]
        premium = filtered_data[i]["cumulative_premium"] / 1000000
        if (filtered_data[i]["option_side"] == "CALL") {
            strike_list.push(strike)
            calls_oi_list.push(oi)
            calls_loss_list.push(premium)

            if (strike >= current_price_global) {
                calls_itm += oi
            } else {
                calls_otm += oi
            }

        } else {
            puts_oi_list.push(oi)
            puts_loss_list.push(premium)

            if (strike <= current_price_global) {
                puts_itm += oi
            } else {
                puts_otm += oi
            }
        }
    }


    c_p_ratio = Math.round(100 * (calls_itm / puts_itm)) / 100
    options_summary_code = `
        <div class="header">${new_date.split("T")[0]}</div>
        <div class="options_summary_sub_div">
            <div class="options_summary_sub"><span>${calls_itm}<br></span>Calls ITM</div>
            <div class="options_summary_sub"><span>${calls_otm}<br></span>Calls OTM</div>
            <div class="options_summary_sub"><span>${puts_itm}<br></span>Puts ITM</div>
            <div class="options_summary_sub"><span>${puts_otm}<br></span>Puts OTM</div>
            <div class="options_summary_sub"><span>${c_p_ratio}<br></span>C/P Ratio</div>
        </div>`

    document.getElementsByClassName("options_summary")[0].innerHTML = options_summary_code;



    for (var i=0; i<calls_loss_list.length; i++) {
        if (calls_loss_list[i] + puts_loss_list[i] < min_loss) {
            min_loss = calls_loss_list[i] + puts_loss_list[i]
            max_pain = strike_list[i]
        }
    }
    document.getElementById("max_pain").innerHTML = `Max Pain ($${max_pain})`

    if (oi_chart != null) {
        max_pain_chart.destroy();
        oi_chart.destroy();
    }

    oi_chart = document.getElementById('oi_chart');
    oi_chart = new Chart(oi_chart, {
        type: 'line',
        data: {
            labels: strike_list,
            datasets: [{
                label: 'Calls',
                lineTension: 0,
                data: calls_oi_list,
                borderColor: "green",
                borderWidth: 2,
                backgroundColor: 'transparent',
                tension: 0.1,
            },
            {
                label: 'Puts',
                lineTension: 0,
                data: puts_oi_list,
                borderColor: "red",
                borderWidth: 2,
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict,
    });

    max_pain_chart = document.getElementById('max_pain_chart');
    max_pain_chart = new Chart(max_pain_chart, {
        type: 'bar',
        data: {
            labels: strike_list,
            datasets: [{
                label: 'Calls',
                data: calls_loss_list,
                borderColor: "green",
                backgroundColor: 'green',
            },
            {
                label: 'Puts',
                data: puts_loss_list,
                borderColor: "red",
                backgroundColor: 'red',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    },
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Amount [$M]',
                        beginAtZero: false,
                    },
                }],

                xAxes: [{
                    ticks: {
                        maxTicksLimit: 20,
                        maxRotation: 45,
                        minRotation: 0,
                    },
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Strike [$]',
                        beginAtZero: false,
                    },
                    stacked: true
                }]
            },
            // To show value when hover on any part of the graph
            tooltips: {
                enabled: true,
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItems, data) {
                        return tooltipItems.yLabel + ' M';
                    }
                }
            },
            hover: {
                mode: 'index',
                intersect: false
            },
        },
    });
}

function show_table(options_data, expiry_date, historical_options_data, current_price, date_index) {
    date_dropdown = document.getElementById("expiry_date")

    expiry_date_global = expiry_date
    options_data_global = options_data
    current_price_global = current_price

    if (!date_index) {
        date_index = 0
    }

    generate_chart(expiry_date[date_index])

    date_list = [];
    max_pain_list = [];
    prev_close_list = [];
    for (var i=0; i<historical_options_data.length;i++) {
        date_list.push(historical_options_data[i]["date"].split("T")[0])
        max_pain_list.push(historical_options_data[i]["max_pain"])
        prev_close_list.push(historical_options_data[i]["stock_price_closed"])
    }

    historical_chart = document.getElementById('historical_chart');
    historical_chart = new Chart(historical_chart, {
        type: 'line',
        data: {
            labels: date_list,
            datasets: [{
                label: 'Max Pain',
                lineTension: 0,
                data: max_pain_list,
                borderColor: "green",
                borderWidth: 2,
                backgroundColor: 'transparent',
                tension: 0.1,
            },
            {
                label: 'Prev Close',
                lineTension: 0,
                data: prev_close_list,
                borderColor: "blue",
                borderWidth: 2,
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Price [$]',
                        beginAtZero: false,
                    },
                }],
                xAxes: [{
                    ticks: {
                        maxTicksLimit: 20,
                        maxRotation: 45,
                        minRotation: 0,
                    },
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Date',
                        beginAtZero: true,
                    },
                }]
            },
            elements: {
                point: {
                    radius: 0
                }
            },
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItem, data) {
                        var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        var label = data.datasets[tooltipItem.datasetIndex].label;
                        return label + ': $' + Number(value).toLocaleString();
                    }
                }
            },
            hover: {
                mode: 'index',
                intersect: false
            },
        },
    });
}

function reload_graph(new_date) {
    generate_chart(new_date)
}