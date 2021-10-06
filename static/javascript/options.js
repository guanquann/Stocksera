function reset_dropdown() {
    document.getElementsByName("date")[0].value = "";
}

function update_table() {
    var table = document.getElementsByTagName("table")[0]
    table.querySelector("thead").innerHTML = "<th colspan='2'>Call</th><th>Strike</th><th colspan='2'>Put</th>" + table.querySelector("thead").innerHTML
    var tr = table.querySelectorAll("tr");
    for (i=2; i<tr.length; i++) {
        var td = tr[row].querySelectorAll("td");
        td[0].innerHTML = Number(td[0].innerHTML)
        td[1].innerHTML = Number(td[1].innerHTML)
        td[3].innerHTML = Number(td[3].innerHTML)
        td[4].innerHTML = Number(td[4].innerHTML)
    }
}

function options_summary(latest_price) {
    latest_price = latest_price.replace(",", "")
    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");

    var calls_itm = 0, calls_otm = 0, puts_itm = 0, puts_otm = 0;
    var next_itm_call_oi = 0, next_itm_call_strike = 0;

    for (i=2; i<tr.length;i++) {
        td = tr[i].querySelectorAll("td")
        strike_price = Number(td[2].innerHTML.replace("$", ""))
        if (latest_price >= strike_price) {
            calls_itm += Number(td[0].innerHTML)
            td[0].classList.add("itm")
            td[1].classList.add("itm")
        }
        else {
            calls_otm += Number(td[0].innerHTML)
            if (next_itm_call_oi == 0) {
                next_itm_call_oi = Number(td[0].innerHTML);
                next_itm_call_strike = td[2].innerHTML
            }
        }
        if (latest_price <= strike_price) {
            puts_itm += Number(td[3].innerHTML)
            td[3].classList.add("itm")
            td[4].classList.add("itm")
        }
        else {
            puts_otm += Number(td[3].innerHTML)
        }
    }

    c_p_ratio = Math.round(100 * (calls_itm / puts_itm)) / 100
    percentage_diff_next_itm = Math.round(((next_itm_call_oi / calls_itm) * 100))

    options_summary_code = `
        <div class="options_summary_sub_div">
            <div class="options_summary_sub"><span>${calls_itm}<br></span>Calls ITM</div>
            <div class="options_summary_sub"><span>${calls_otm}<br></span>Calls OTM</div>
            <div class="options_summary_sub"><span>${puts_itm}<br></span>Puts ITM</div>
            <div class="options_summary_sub"><span>${puts_otm}<br></span>Puts OTM</div>
            <div class="options_summary_sub"><span>${c_p_ratio}<br></span>C/P Ratio</div>
            <div class="options_summary_sub"><span>+${next_itm_call_oi}(${percentage_diff_next_itm}%)<br></span>Calls ITM @ ${next_itm_call_strike}</div>
        </div>`
    document.getElementsByClassName("options_summary")[0].innerHTML += options_summary_code;
}

function draw_open_interest_and_volume() {
    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");

    var calls_oi_list = [], puts_oi_list = []
    var calls_vol_list = [], puts_vol_list = []
    var strike_list = [];

    for (row=2; row<tr.length; row++) {
        var td = tr[row].querySelectorAll("td");
        calls_oi_list.push(td[0].innerHTML);
        calls_vol_list.push(td[1].innerHTML);

        strike_list.push(td[2].innerHTML.replace("$", ""));

        puts_oi_list.push(td[3].innerHTML);
        puts_vol_list.push(td[4].innerHTML);
    }

    options_dict = {
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

    var volume_chart = document.getElementById('volume_chart');
    var volume_chart = new Chart(volume_chart, {
        type: 'line',
        data: {
            labels: strike_list,
            datasets: [{
                label: 'Calls',
                lineTension: 0,
                data: calls_vol_list,
                borderColor: "green",
                backgroundColor: 'transparent',
                tension: 0.1,
            },
            {
                label: 'Puts',
                lineTension: 0,
                data: puts_vol_list,
                borderColor: "red",
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict,
    });

    var oi_chart = document.getElementById('oi_chart');
    var oi_chart = new Chart(oi_chart, {
        type: 'line',
        data: {
            labels: strike_list,
            datasets: [{
                label: 'Calls',
                lineTension: 0,
                data: calls_oi_list,
                borderColor: "green",
                backgroundColor: 'transparent',
                tension: 0.1,
            },
            {
                label: 'Puts',
                lineTension: 0,
                data: puts_oi_list,
                borderColor: "red",
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict,
    });
}

function draw_max_pain(strike_list, call_loss_list, put_loss_list) {
    var max_pain_chart = document.getElementById('max_pain_chart');
    var max_pain_chart = new Chart(max_pain_chart, {
        type: 'bar',
        data: {
            labels: strike_list,
            datasets: [{
                label: 'Calls',
                data: call_loss_list,
                borderColor: "green",
                backgroundColor: 'green',
            },
            {
                label: 'Puts',
                data: put_loss_list,
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
                        labelString: 'Amount [$B]',
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