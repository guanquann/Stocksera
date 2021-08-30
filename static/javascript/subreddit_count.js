var wsb_chart = null;

function find_day_gain(list_name, id) {
    list_length = list_name.length;
    var diff = list_name[list_length-1] - list_name[list_length-2];
    var percentage_diff = Math.round(diff / list_name[list_length-2] * 10000) / 100
    document.getElementById(id).innerHTML = "+" + diff + "<br> +" + percentage_diff + "%";
}

function subreddit_count(duration) {
    var date_threshold = get_date_difference(duration, "-")
    var wsb_date = [], wsb_count = [], wsb_active = [] , wsb_growth = []
    stocks_date = [], stocks_active = [] , stocks_count = [], stocks_growth = []
    superstonk_date = [], superstonk_count = [], superstonk_active = [], superstonk_growth = []
    amc_date = [], amc_count = [], amc_active = [], amc_growth = []
    options_date = [], options_count = [], options_active = [], options_growth = []
    pennystocks_date = [], pennystocks_count = [], pennystocks_active = [], pennystocks_growth = []
    crypto_date = [], crypto_count = [], crypto_active = [], crypto_growth = []

    for (subscribers of subscribers_list) {
        if (subscribers[0] >= date_threshold) {
            if (subscribers[2] == "wallstreetbets") {
                wsb_count.push(subscribers[3])
                wsb_active.push(subscribers[5])
                wsb_growth.push(subscribers[6])
                wsb_date.push(subscribers[0])
            }
            else if (subscribers[2] == "stocks") {
                stocks_count.push(subscribers[3])
                stocks_active.push(subscribers[5])
                stocks_growth.push(subscribers[6])
                stocks_date.push(subscribers[0])
            }
            else if (subscribers[2] == "Superstonk") {
                superstonk_count.push(subscribers[3])
                superstonk_active.push(subscribers[5])
                superstonk_growth.push(subscribers[6])
                superstonk_date.push(subscribers[0])
            }
            else if (subscribers[2] == "options") {
                options_count.push(subscribers[3])
                options_active.push(subscribers[5])
                options_growth.push(subscribers[6])
                options_date.push(subscribers[0])
            }
            else if (subscribers[2] == "amcstock") {
                amc_count.push(subscribers[3])
                amc_active.push(subscribers[5])
                amc_growth.push(subscribers[6])
                amc_date.push(subscribers[0])
            }
            else if (subscribers[2] == "pennystocks") {
                pennystocks_count.push(subscribers[3])
                pennystocks_active.push(subscribers[5])
                pennystocks_growth.push(subscribers[6])
                pennystocks_date.push(subscribers[0])
            }
            else if (subscribers[2] == "cryptocurrency") {
                crypto_count.push(subscribers[3])
                crypto_active.push(subscribers[5])
                crypto_growth.push(subscribers[6])
                crypto_date.push(subscribers[0])
            }
        }
    }

    var options_dict = {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
            display: false
         },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: false,
                    maxTicksLimit: 6,
                },
                gridLines: {
                    drawOnChartArea: false
                }
            }],
            xAxes: [{
                ticks: {
                  maxTicksLimit: 10,
                  maxRotation: 45,
                  minRotation: 0,
                },
                gridLines: {
                    drawOnChartArea: false
                }
            }]
        },
        // To remove the point of each label
        elements: {
            point: {
                radius: 0
            }
        },
        // To show value when hover on any part of the graph
        tooltips: {
            mode: 'index',
            intersect: false,
            callbacks: {
                label: (item) => `${item.yLabel} subscribers`,
            },
        },
        hover: {
            mode: 'index',
            intersect: false
        },
    };

    if (wsb_chart != null){
        wsb_chart.destroy();
        stocks_chart.destroy();
        options_chart.destroy();
        superstonk_chart.destroy();
        amc_chart.destroy();
        pennystocks_chart.destroy();
        crypto_chart.destroy();
        growth_chart.destroy();
        active_chart.destroy();
    }

    wsb_chart = document.getElementById('wsb_chart');
    wsb_chart = new Chart(wsb_chart, {
        type: 'line',
        data: {
            labels: wsb_date,
            datasets: [{
                data: wsb_count,
                borderColor: '#f1c40f',
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict
    });

    stocks_chart = document.getElementById('stocks_chart');
    stocks_chart = new Chart(stocks_chart, {
        type: 'line',
        data: {
            labels: stocks_date,
            datasets: [{
                data: stocks_count,
                borderColor: '#c39889',
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict
    });

    options_chart = document.getElementById('options_chart');
    options_chart = new Chart(options_chart, {
        type: 'line',
        data: {
            labels: options_date,
            datasets: [{
                data: options_count,
                borderColor: '#4affff',
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict
    });

    superstonk_chart = document.getElementById('superstonk_chart');
    superstonk_chart = new Chart(superstonk_chart, {
        type: 'line',
        data: {
            labels: superstonk_date,
            datasets: [{
                data: superstonk_count,
                borderColor: 'grey',
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict
    });

    amc_chart = document.getElementById('amc_chart');
    amc_chart = new Chart(amc_chart, {
        type: 'line',
        data: {
            labels: amc_date,
            datasets: [{
                data: amc_count,
                borderColor: '#ad001d',
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict
    });

    pennystocks_chart = document.getElementById('pennystocks_chart');
    pennystocks_chart = new Chart(pennystocks_chart, {
        type: 'line',
        data: {
            labels: pennystocks_date,
            datasets: [{
                data: pennystocks_count,
                borderColor: '#192a8a',
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict
    });

    crypto_chart = document.getElementById('crypto_chart');
    crypto_chart = new Chart(crypto_chart, {
        type: 'line',
        data: {
            labels: crypto_date,
            datasets: [{
                data: crypto_count,
                borderColor: 'green',
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },
        options: options_dict
    });

    growth_chart = document.getElementById('growth_chart');
    growth_chart = new Chart(growth_chart, {
        type: 'line',
        data: {
            labels: wsb_date,
            datasets: [
                {
                    label: "Wallstreetbets",
                    data: wsb_growth,
                    borderColor: '#f1c40f',
                    backgroundColor: 'transparent',
                    tension: 0.1,
                },
                {
                    label: "Stocks",
                    data: stocks_growth,
                    borderColor: '#c39889',
                    backgroundColor: 'transparent',
                    tension: 0.1,
                },
                {
                    label: "Superstonk",
                    data: superstonk_growth,
                    borderColor: 'grey',
                    backgroundColor: 'transparent',
                    tension: 0.1,
                },
                {
                    label: "amcstock",
                    data: amc_growth,
                    borderColor: '#ad001d',
                    backgroundColor: 'transparent',
                    tension: 0.1,
                },
                {
                    label: "cryptocurrency",
                    data: crypto_growth,
                    borderColor: 'green',
                    backgroundColor: 'transparent',
                    tension: 0.1,
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
                ticks: {
                    beginAtZero: false,
                    maxTicksLimit: 6,
                },
                gridLines: {
                    drawOnChartArea: false
                }
            }],
            xAxes: [{
                ticks: {
                  maxTicksLimit: 10,
                  maxRotation: 45,
                  minRotation: 0,
                },
                gridLines: {
                    drawOnChartArea: false
                }
            }]
        },
        // To remove the point of each label
        elements: {
            point: {
                radius: 0
            }
        },
        // To show value when hover on any part of the graph
        tooltips: {
            mode: 'index',
            intersect: false,
            callbacks: {
                label: function(tooltipItem, data) {
                    var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                    var label = data.datasets[tooltipItem.datasetIndex].label;
                    return "r/" + label + ': ' + value + '%';
                }
            }
        },
        hover: {
            mode: 'index',
            intersect: false
        },
    }
    });

    active_chart = document.getElementById('active_chart');
    active_chart = new Chart(active_chart, {
        type: 'line',
        data: {
            labels: wsb_date,
            datasets: [
                {
                    label: "Wallstreetbets",
                    data: wsb_active,
                    borderColor: '#f1c40f',
                    backgroundColor: 'transparent',
                    tension: 0.1,
                },
                {
                    label: "Stocks",
                    data: stocks_active,
                    borderColor: '#c39889',
                    backgroundColor: 'transparent',
                    tension: 0.1,
                },
                {
                    label: "Superstonk",
                    data: superstonk_active,
                    borderColor: 'grey',
                    backgroundColor: 'transparent',
                    tension: 0.1,
                },
                {
                    label: "amcstock",
                    data: amc_active,
                    borderColor: '#ad001d',
                    backgroundColor: 'transparent',
                    tension: 0.1,
                },
                {
                    label: "cryptocurrency",
                    data: crypto_active,
                    borderColor: 'green',
                    backgroundColor: 'transparent',
                    tension: 0.1,
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
                ticks: {
                    beginAtZero: false,
                    maxTicksLimit: 6,
                },
                gridLines: {
                    drawOnChartArea: false
                }
            }],
            xAxes: [{
                ticks: {
                  maxTicksLimit: 10,
                  maxRotation: 45,
                  minRotation: 0,
                },
                gridLines: {
                    drawOnChartArea: false
                }
            }]
        },
        // To remove the point of each label
        elements: {
            point: {
                radius: 0
            }
        },
        // To show value when hover on any part of the graph
        tooltips: {
            mode: 'index',
            intersect: false,
            callbacks: {
                label: function(tooltipItem, data) {
                    var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                    var label = data.datasets[tooltipItem.datasetIndex].label;
                    return "r/" + label + ': ' + value + '%';
                }
            }
        },
        hover: {
            mode: 'index',
            intersect: false
        },
    }
    });

    find_day_gain(wsb_count, "wsb_diff")
    find_day_gain(stocks_count, "stocks_diff")
    find_day_gain(options_count, "options_diff")
    find_day_gain(superstonk_count, "superstonk_diff")
    find_day_gain(amc_count, "amc_diff")
    find_day_gain(pennystocks_count, "pennystocks_diff")
    find_day_gain(crypto_count, "crypto_diff")
}

function subreddit_individual(duration) {
    var date_threshold = get_date_difference(duration, "-")
    var subreddit_date = [], subreddit_count = [], subreddit_active = [] , subreddit_growth = []
    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr")
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td")
        subreddit_date.push(td[0].innerHTML)
        subreddit_count.push(td[1].innerHTML)
        subreddit_active.push(td[3].innerHTML)
        subreddit_growth.push(td[4].innerHTML)
    }

//    subreddit_chart = document.getElementById('subreddit_chart');
//    subreddit_chart = new Chart(subreddit_chart, {
//        data: {
//            labels: subreddit_date,
//            datasets: [
//                {
//                    label: 'Num Redditors',
//                    type: 'line',
//                    data: subreddit_count,
//                    borderColor: 'rgb(38, 166, 154)',
//                    backgroundColor: 'transparent',
//                    yAxisID: 'A',
//                },
//                {
//                    label: '% Active',
//                    type: 'bar',
//                    data: subreddit_active,
//                    borderColor: 'wheat',
//                    backgroundColor: 'wheat',
//                    yAxisID: 'B',
//                },
//                {
//                    label: '% Growth',
//                    type: 'bar',
//                    data: subreddit_growth,
//                    borderColor: 'blue',
//                    backgroundColor: 'blue',
//                    yAxisID: 'B',
//                }]
//        },
//
//        options: {
//            responsive: true,
//            maintainAspectRatio: false,
//            legend: {
//                display: true
//            },
//            scales: {
//                yAxes: [
//                    {
//                        position: 'left',
//                        gridLines: {
//                            display: false
//                        },
//                        type: "linear",
//                        id: "A",
//                        scaleLabel: {
//                            display: true,
//                            labelString: 'Num Redditors',
//                            beginAtZero: false,
//                        }
//                    },
//                    {
//                        scaleLabel: {
//                            display: true,
//                            labelString: 'Percentage',
//                            beginAtZero: true,
//                        },
//                        type: "linear",
//                        id: "B",
//                        position:"right",
//                        gridLines: {
//                            display: false
//                        },
//                        ticks: {
//                            callback: function(value, index, values) {
//                                return value + "%";
//                            }
//                        },
//                    }],
//
//                xAxes: [{
//                    offset: true,
//                    ticks: {
//                      maxTicksLimit: 10,
//                      maxRotation: 45,
//                      minRotation: 0,
//                    },
//                    gridLines: {
//                        drawOnChartArea: false
//                    },
//                    stacked: false
//                }],
//            },
//            pan: {
//                enabled: true,
//                mode: "x",
//                speed: 10,
//                threshold: 10
//            },
//            zoom: {
//                enabled: true,
//                drag: false,
//                mode: "xy",
//                speed: 1
//            },
//
//            // To show value when hover on any part of the graph
//            tooltips: {
//                mode: 'index',
//                intersect: false,
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
//    });

    var trace1 = {
        x: subreddit_date,
        y: subreddit_count,
        name: "Num Redditors",
        line: {'color': 'rgb(38, 166, 154)'},
        hovertemplate:
                "Num Redditors: %{y}<br>" +
                "<extra></extra>",
        type: 'scatter'
    };

    var trace2 = {
        x: subreddit_date,
        y: subreddit_growth,
        yaxis: 'y2',
        name: "% Growth",
        hovertemplate:
                "% Growth: %{y}%<br>" +
                "<extra></extra>",
        type: 'bar',
        marker: {
            color: 'orange',
        }
    };

    var trace3 = {
        x: subreddit_date,
        y: subreddit_active,
        yaxis: 'y2',
        name: "% Active",
        hovertemplate:
                "% Active: %{y}%<br>" +
                "<extra></extra>",
        type: 'bar',
        marker: {
            color: 'rgb(158,202,225)',
            opacity: 0.6,
            line: {
                color: 'rgb(8,48,107)',
                width: 1.5
            }
        }
    };

    var layout = {
        autosize: true,
        margin: {
            t:30,
            l:50,
            r:50,
            pad: 0
        },
        automargin: true,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        xaxis: {
            showgrid: false,
            showline: true,
            color: "gray",
            title: {
                text: 'Date',
                font: {
                      size: 12,
                }
            },
        },
        yaxis: {
            showgrid: false,
            showline: true,
            color: "gray",
            title: {
                text: 'Num Redditors',
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
                text: 'Percentage',
                font: {
                      size: 11,
                }
            },
            overlaying: 'y',
            side: 'right',
        },
        hovermode:'x',
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h'
        }
    };

    var data = [trace1, trace2, trace3];
    Plotly.newPlot('chart', data, layout, {displayModeBar: false, showTips: true, responsive: true});

}