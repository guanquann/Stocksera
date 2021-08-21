var wsb_chart = null;

function subreddit_count(duration) {
    var date_threshold = get_date_difference(duration, "-")
    var wsb_date = [], wsb_count = [], wsb_active = [] , wsb_growth = []
    stocks_date = [], stocks_active = [] , stocks_count = [], stocks_growth = []
    StockMarket_date = [], StockMarket_count = [], StockMarket_active = [], StockMarket_growth = []
    gme_date = [], gme_count = [], gme_active = [], gme_growth = []
    superstonk_date = [], superstonk_count = [], superstonk_active = [], superstonk_growth = []
    amc_date = [], amc_count = [], amc_active = [], amc_growth = []
    options_date = [], options_count = [], options_active = [], options_growth = []
    pennystocks_date = [], pennystocks_count = [], pennystocks_active = [], pennystocks_growth = []
    investing_date = [], investing_count = [], investing_active = [], investing_growth = []
    crypto_date = [], crypto_count = [], crypto_active = [], crypto_growth = []

    for (subscribers of subscribers_list) {
        if (subscribers[4] >= date_threshold) {
            if (subscribers[1] == "wallstreetbets") {
                wsb_count.push(subscribers[2])
                wsb_active.push(subscribers[5])
                wsb_growth.push(subscribers[6])
                wsb_date.push(subscribers[4])
            }
            else if (subscribers[1] == "stocks") {
                stocks_count.push(subscribers[2])
                stocks_active.push(subscribers[5])
                stocks_growth.push(subscribers[6])
                stocks_date.push(subscribers[4])
            }
            else if (subscribers[1] == "StockMarket") {
                StockMarket_count.push(subscribers[2])
                StockMarket_active.push(subscribers[5])
                StockMarket_growth.push(subscribers[6])
                StockMarket_date.push(subscribers[4])
            }
            else if (subscribers[1] == "Superstonk") {
                superstonk_count.push(subscribers[2])
                superstonk_active.push(subscribers[5])
                superstonk_growth.push(subscribers[6])
                superstonk_date.push(subscribers[4])
            }
            else if (subscribers[1] == "options") {
                options_count.push(subscribers[2])
                options_active.push(subscribers[5])
                options_growth.push(subscribers[6])
                options_date.push(subscribers[4])
            }
            else if (subscribers[1] == "amcstock") {
                amc_count.push(subscribers[2])
                amc_active.push(subscribers[5])
                amc_growth.push(subscribers[6])
                amc_date.push(subscribers[4])
            }
            else if (subscribers[1] == "GME") {
                gme_count.push(subscribers[2])
                gme_active.push(subscribers[5])
                gme_growth.push(subscribers[6])
                gme_date.push(subscribers[4])
            }
            else if (subscribers[1] == "pennystocks") {
                pennystocks_count.push(subscribers[2])
                pennystocks_active.push(subscribers[5])
                pennystocks_growth.push(subscribers[6])
                pennystocks_date.push(subscribers[4])
            }
            else if (subscribers[1] == "investing") {
                investing_count.push(subscribers[2])
                investing_active.push(subscribers[5])
                investing_growth.push(subscribers[6])
                investing_date.push(subscribers[4])
            }
            else if (subscribers[1] == "cryptocurrency") {
                crypto_count.push(subscribers[2])
                crypto_active.push(subscribers[5])
                crypto_growth.push(subscribers[6])
                crypto_date.push(subscribers[4])
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
        StockMarket_chart.destroy();
        options_chart.destroy();
        gme_chart.destroy();
        superstonk_chart.destroy();
        amc_chart.destroy();
        pennystocks_chart.destroy();
        investing_chart.destroy();
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

    StockMarket_chart = document.getElementById('StockMarket_chart');
    StockMarket_chart = new Chart(StockMarket_chart, {
        type: 'line',
        data: {
            labels: StockMarket_date,
            datasets: [{
                data: StockMarket_count,
                borderColor: 'rgb(38, 166, 154)',
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

    gme_chart = document.getElementById('gme_chart');
    gme_chart = new Chart(gme_chart, {
        type: 'line',
        data: {
            labels: gme_date,
            datasets: [{
                data: gme_count,
                borderColor: '#00b0ff',
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

    investing_chart = document.getElementById('investing_chart');
    investing_chart = new Chart(investing_chart, {
        type: 'line',
        data: {
            labels: investing_date,
            datasets: [{
                data: investing_count,
                borderColor: '#64a913',
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
                borderColor: '#d73d08',
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
                    label: "StockMarket",
                    data: StockMarket_growth,
                    borderColor: 'rgb(38, 166, 154)',
                    backgroundColor: 'transparent',
                    tension: 0.1,
                },
                {
                    label: "GME",
                    data: gme_growth,
                    borderColor: '#00b0ff',
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
                    label: "StockMarket",
                    data: StockMarket_active,
                    borderColor: 'rgb(38, 166, 154)',
                    backgroundColor: 'transparent',
                    tension: 0.1,
                },
                {
                    label: "GME",
                    data: gme_active,
                    borderColor: '#00b0ff',
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

    function find_day_gain(list_name, id) {
        list_length = list_name.length;
        var diff = list_name[list_length-1] - list_name[list_length-2];
        var percentage_diff = Math.round(diff / list_name[list_length-2] * 10000) / 100
        document.getElementById(id).innerHTML = "+" + diff + "<br> +" + percentage_diff + "%";
    }

    find_day_gain(wsb_count, "wsb_diff")
    find_day_gain(stocks_count, "stocks_diff")
    find_day_gain(StockMarket_count, "stockmarket_diff")
    find_day_gain(options_count, "options_diff")
    find_day_gain(gme_count, "gamestop_diff")
    find_day_gain(superstonk_count, "superstonk_diff")
    find_day_gain(amc_count, "amc_diff")
    find_day_gain(pennystocks_count, "pennystocks_diff")
    find_day_gain(investing_count, "investing_diff")
    find_day_gain(crypto_count, "crypto_diff")
}