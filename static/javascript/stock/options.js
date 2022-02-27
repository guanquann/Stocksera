var oi_chart = null;
var vol_chart = null;
var max_pain_chart = null;

function show_table(response, date_index) {
    date_dropdown = document.getElementById("expiry_date")

    puts_json = response["putExpDateMap"]
    calls_json = response["callExpDateMap"]

    all_dates_list = Object.keys(puts_json)
    for (i=0; i<all_dates_list.length; i++) {
        date_dropdown.innerHTML += `<option value=${i}>${all_dates_list[i].split(":")[0]}</option>`
    }

    if (!date_index) {
        date_index = 0
    }

    interested_date = all_dates_list[date_index]
    document.getElementById("expiry_date").value = date_index

    calls_json = calls_json[interested_date];
    puts_json = puts_json[interested_date];

    var calls_oi_list = [], puts_oi_list = [];
    var calls_vol_list = [], puts_vol_list = [];
    var strike_list = [];
    var calls_itm = 0, calls_otm = 0, puts_itm = 0, puts_otm = 0;
    var calls_vol = 0, puts_vol = 0
    var next_itm_call_oi = 0, next_itm_call_strike = 0;
    var table_code = `
        <table id="options_chain">
            <tr>
                <th>Strike</th>
                <th>Type</th>
                <th>Last</th>
                <th>Change</th>
                <th>% Change</th>
                <th>Bid</th>
                <th>Ask</th>
                <th>High</th>
                <th>Low</th>
                <th>Vol</th>
                <th>OI</th>
                <th>Volatility</th>
                <th>Intrinsic</th>
                <th>Time Value</th>
                <th>Delta</th>
                <th>Gamma</th>
                <th>Theta</th>
                <th>Vega</th>
                <th>Rho</th>
            </tr>
    `

    for (i in puts_json) {
        calls_data = calls_json[i][0]
        puts_data = puts_json[i][0]

        if (calls_data["inTheMoney"]) {
            calls_itm += calls_data["openInterest"]
        }
        else {
            calls_otm += calls_data["openInterest"]
            if (next_itm_call_oi == 0) {
                next_itm_call_oi = calls_data["openInterest"]
                next_itm_call_strike = calls_data["strikePrice"]
            }
        }
        if (puts_data["inTheMoney"]) {
            puts_itm += puts_data["openInterest"]
        }
        else {
            puts_otm += puts_data["openInterest"]
        }

        strike_list.push(calls_data["strikePrice"])
        calls_oi_list.push(calls_data["openInterest"])
        calls_vol_list.push(calls_data["totalVolume"])
        puts_oi_list.push(puts_data["openInterest"])
        puts_vol_list.push(puts_data["totalVolume"])

        calls_price_style = calls_data["percentChange"]<0 ? "red" : "green"
        puts_price_style = puts_data["percentChange"]<0 ? "red" : "green"

        table_code += `
            <tr>
                <td rowspan="2">${calls_data["strikePrice"]}</td>
                <td>${calls_data["putCall"]}</td>
                <td style="color: ${calls_price_style}">${calls_data["last"]}</td>
                <td style="color: ${calls_price_style}">${calls_data["netChange"]}</td>
                <td style="color: ${calls_price_style}">${calls_data["percentChange"]}%</td>
                <td>${calls_data["bid"]}<br><div style="font-size: smaller">x ${calls_data["bidSize"]}</div></td>
                <td>${calls_data["ask"]}<br><div style="font-size: smaller">x ${calls_data["askSize"]}</div></td>
                <td>${calls_data["highPrice"]}</td>
                <td>${calls_data["lowPrice"]}</td>
                <td>${calls_data["totalVolume"]}</td>
                <td>${calls_data["openInterest"]}</td>
                <td rowspan="2">${calls_data["volatility"]}</td>
                <td>${calls_data["intrinsicValue"]}</td>
                <td>${calls_data["timeValue"]}</td>
                <td>${calls_data["delta"]}</td>
                <td>${calls_data["gamma"]}</td>
                <td>${calls_data["theta"]}</td>
                <td>${calls_data["vega"]}</td>
                <td>${calls_data["rho"]}</td>
            </tr>
            <tr>
                <td>${puts_data["putCall"]}</td>
                <td style="color: ${puts_price_style}">${puts_data["last"]}</td>
                <td style="color: ${puts_price_style}">${puts_data["netChange"]}</td>
                <td style="color: ${puts_price_style}">${puts_data["percentChange"]}%</td>
                <td>${puts_data["bid"]}<br><div style="font-size: smaller">x ${puts_data["bidSize"]}</div></td>
                <td>${puts_data["ask"]}<br><div style="font-size: smaller">x ${puts_data["askSize"]}</div></td>
                <td>${puts_data["highPrice"]}</td>
                <td>${puts_data["lowPrice"]}</td>
                <td>${puts_data["totalVolume"]}</td>
                <td>${puts_data["openInterest"]}</td>
                <td>${puts_data["intrinsicValue"]}</td>
                <td>${puts_data["timeValue"]}</td>
                <td>${puts_data["delta"]}</td>
                <td>${puts_data["gamma"]}</td>
                <td>${puts_data["theta"]}</td>
                <td>${puts_data["vega"]}</td>
                <td>${puts_data["rho"]}</td>
            </tr>
        `
    }
    document.getElementById("table_div").innerHTML = table_code + "</table>";

    c_p_ratio = Math.round(100 * (calls_itm / puts_itm)) / 100
    percentage_diff_next_itm = Math.round(((next_itm_call_oi / calls_itm) * 100))
    options_summary_code = `
        <div class="header">${interested_date.split(":")[0]}</div>
        <div class="options_summary_sub_div">
            <div class="options_summary_sub"><span>${calls_itm}<br></span>Calls ITM</div>
            <div class="options_summary_sub"><span>${calls_otm}<br></span>Calls OTM</div>
            <div class="options_summary_sub"><span>${puts_itm}<br></span>Puts ITM</div>
            <div class="options_summary_sub"><span>${puts_otm}<br></span>Puts OTM</div>
            <div class="options_summary_sub"><span>${c_p_ratio}<br></span>C/P Ratio</div>
            <div class="options_summary_sub"><span>+${next_itm_call_oi}(${percentage_diff_next_itm}%)<br></span>Calls ITM @ ${next_itm_call_strike}</div>
        </div>`
    document.getElementsByClassName("options_summary")[0].innerHTML = options_summary_code;

    if (max_pain_chart != null){
        max_pain_chart.destroy();
        volume_chart.destroy();
        oi_chart.destroy();
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

    volume_chart = document.getElementById('volume_chart');
    volume_chart = new Chart(volume_chart, {
        type: 'line',
        data: {
            labels: strike_list,
            datasets: [{
                label: 'Calls',
                lineTension: 0,
                data: calls_vol_list,
                borderColor: "green",
                borderWidth: 2,
                backgroundColor: 'transparent',
                tension: 0.1,
            },
            {
                label: 'Puts',
                lineTension: 0,
                data: puts_vol_list,
                borderColor: "red",
                borderWidth: 2,
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict,
    });

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
}

function show_max_pain() {
    strike_list = [];
    call_loss_list = [];
    put_loss_list = [];
    max_pain = 0;
    min_loss = 9999999999999;
    trs = document.getElementById("options_chain").querySelectorAll("tr");
    for (i=1; i<trs.length;i++) {
        td = trs[i].querySelectorAll("td");
        // calls row
        if (i % 2 == 1) {
            strike_price = Number(td[0].innerHTML)
            strike_list.push(strike_price);
            call_loss = 0
            for (k=i; k>0; k-=2) {
                td_iter = trs[k].querySelectorAll("td")
                current_price = Number(td_iter[0].innerHTML);
                oi = Number(td_iter[10].innerHTML)
                call_loss += Number(strike_price-current_price) * oi
            }
            call_loss_list.push(call_loss/10000)
        }
        // puts row
        else {
            put_loss = 0
            for (k=i; k<trs.length; k+=2) {
                td_iter = trs[k].querySelectorAll("td")
                current_price = Number(trs[k-1].querySelector("td").innerHTML);
                oi = Number(td_iter[9].innerHTML)
                put_loss += Number(strike_price-current_price) * oi
            }
            put_loss_list.push(-put_loss/10000)
            if (call_loss - put_loss < min_loss) {
                max_pain = strike_price
                min_loss = call_loss - put_loss
            }
        }
    }

    document.getElementById("max_pain").innerHTML = `Max Pain ($${max_pain})`

    max_pain_chart = document.getElementById('max_pain_chart');
    max_pain_chart = new Chart(max_pain_chart, {
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