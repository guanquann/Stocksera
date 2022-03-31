function load_table(borrowed_shares, ftd, short_vol, wsb) {
    code = ""
    date_list = [], fee_list = [], available_list = []
    for (i in borrowed_shares) {
        fees = borrowed_shares[i]["fee"]
        if (fees != 0 || i == 0) {
            date = borrowed_shares[i]["date_updated"]
            available = borrowed_shares[i]["available"]

            fee_list.push(fees)
            available_list.push(available)
            date_list.push(date)
        }

        code += `
            <tr>
                <td>${fees}%</td>
                <td>${Number(available).toLocaleString()}</td>
                <td>${date}</td>
            <tr>
        `
    }
    document.getElementById("borrowed_shares").innerHTML += code

    borrowed_shares_chart = document.getElementById('borrowed_shares_chart');
    borrowed_shares_chart = new Chart(borrowed_shares_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Fee',
                    type: 'line',
                    data: fee_list,
                    borderColor: 'blue',
                    borderWidth: 2,
                    backgroundColor: 'transparent',
                    yAxisID: 'B',
                },
                {
                    label: 'Available',
                    type: 'bar',
                    data: available_list,
                    backgroundColor: 'red',
                    barThickness: 'flex',
                    yAxisID: 'A',
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
                        position: 'left',
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        type: "linear",
                        id: "A",
                        stacked: false,
                        scaleLabel: {
                            display: true,
                            labelString: 'Available',
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return value;
                            },
                            beginAtZero: true
                        }
                    },
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Fee [%]',
                        },
                        type: "linear",
                        id: "B",
                        position:"right",
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return value;
                            },
                            beginAtZero: true,
                        },
                    }],

                xAxes: [{
                    type: "time",
                    distribution: 'series',
                    time: {
                        unit: "day"
                    },
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
                callbacks: {
                    label: function(tooltipItem, data) {
                        var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        var label = data.datasets[tooltipItem.datasetIndex].label;
                        if (label.includes("Available")) {
                            return label + ': ' + Number(value).toLocaleString();
                        }
                        else {
                            return label + ': ' + value + "%";
                        }
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
            }
        }
    });

    code = ""
    date_list = [], vol_list = [], price_list = [];
    for (i in ftd) {
        date = ftd[i]["Date"]
        qty = ftd[i]["Failure to Deliver"]
        price = ftd[i]["Price"]

        date_list.push(date)
        vol_list.push(qty / 1000000)
        price_list.push(price)
        
        code += `
            <tr>
                <td>${date}</td>
                <td>${Number(qty).toLocaleString()}</td>
                <td>$${price}</td>
            <tr>
        `
    }
    document.getElementById("ftd").innerHTML += code

    ftd_chart = document.getElementById('ftd_chart');
    ftd_chart = new Chart(ftd_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'FTD',
                    type: 'line',
                    data: vol_list,
                    borderColor: 'orange',
                    borderWidth: 2,
                    backgroundColor: 'transparent',
                    yAxisID: 'B',
                },
                {
                    label: 'Price',
                    type: 'line',
                    data: price_list,
                    backgroundColor: 'transparent',
                    borderColor: 'rgb(38, 166, 154)',
                    borderWidth: 2,
                    yAxisID: 'A',
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                        position: 'left',
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        type: "linear",
                        id: "A",
                        scaleLabel: {
                            display: true,
                            labelString: 'Price [$]',
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return value;
                            }
                        },
                    },
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'FTD [M]',
                        },
                        type: "linear",
                        id: "B",
                        position:"right",
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return value;
                            }
                        },
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
                        maxTicksLimit: 10,
                        maxRotation: 30,
                        minRotation: 0,
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
                        if (label == "Price") {
                            return label + ': $' + value;
                        }
                        else {
                            return label + ': ' + Number(value*1000000).toLocaleString();
                        }
                    }
                }
            },

            elements: {
                line: {
                    tension: 0
                },
                point: {
                    radius: 0
                }
            },

            hover: {
                mode: 'index',
                intersect: false
            },
        },
    });

    code = ""
    date_list = [], short_vol_list = [], long_vol_list = [], percentage_list = []
    for (i in short_vol) {
        date = short_vol[i]["Date"]
        short_volume = short_vol[i]["Short Vol"]
        long_volume = short_vol[i]["Total Vol"] - short_volume
        percent_shorted = short_vol[i]["% Shorted"]

        date_list.push(date)
        short_vol_list.push(short_volume / 1000000)
        long_vol_list.push(long_volume / 1000000)
        percentage_list.push(percent_shorted)

        code += `
            <tr>
                <td>${date}</td>
                <td>${Number(short_volume).toLocaleString()}</td>
                <td>${Number(long_volume).toLocaleString()}</td>
                <td>${percent_shorted}%</td>
            <tr>
        `
    }
    document.getElementById("short_vol").innerHTML += code

    short_vol_chart = document.getElementById('short_vol_chart');
    short_vol_chart = new Chart(short_vol_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Short Percentage',
                    type: 'line',
                    data: percentage_list,
                    borderColor: 'blue',
                    borderWidth: 2,
                    backgroundColor: 'transparent',
                    yAxisID: 'B',
                },
                {
                    label: 'Short Volume',
                    type: 'bar',
                    data: short_vol_list,
                    backgroundColor: 'red',
                    barThickness: 'flex',
                    yAxisID: 'A',
                },
                {
                    label: 'Long Volume',
                    type: 'bar',
                    data: long_vol_list,
                    backgroundColor: 'rgb(38, 166, 154)',
                    barThickness: 'flex',
                    yAxisID: 'A',
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
                        position: 'left',
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        type: "linear",
                        id: "A",
                        stacked: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Volume [M]',
                            beginAtZero: true,
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return value;
                            },
                        }
                    },
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Short Percentage [%]',
                            beginAtZero: true,
                        },
                        type: "linear",
                        id: "B",
                        position:"right",
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        ticks: {
                            max: 100,
                            min: 0,
                            callback: function(value, index, values) {
                                return value;
                            }
                        },
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
                callbacks: {
                    label: function(tooltipItem, data) {
                        var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        var label = data.datasets[tooltipItem.datasetIndex].label;
                        if (label.includes("Volume")) {
                            return label + ': ' + Number(value * 1000000).toLocaleString();
                        }
                        else {
                            return label + ': ' + value + "%";
                        }
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
    });

    code = ""
    date_list = [], mentions_list = []
    for (i in wsb) {
        mentions = wsb[i]["mentions"]
        calls = wsb[i]["calls"]
        puts = wsb[i]["puts"]
        date = wsb[i]["date_updated"]

        mentions_list.push(mentions)
        date_list.push(date)

        code += `
            <tr>
                <td>${mentions}</td>
                <td>${calls}</td>
                <td>${puts}</td>
                <td>${date}</td>
            <tr>
        `
    }
    document.getElementById("wsb").innerHTML += code

    wsb_chart = document.getElementById('wsb_chart');
    wsb_chart = new Chart(wsb_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Mentions',
                    type: 'bar',
                    data: mentions_list,
                    backgroundColor: 'red',
                    barThickness: 'flex',
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
                        position: 'left',
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        type: "linear",
                        stacked: false,
                        scaleLabel: {
                            display: true,
                            labelString: 'Mentions',
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return value;
                            },
                            beginAtZero: true
                        }
                    }],

                xAxes: [{
                    type: "time",
                    distribution: 'series',
                    time: {
                        unit: "day"
                    },
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
            }
        }
    });
}

function show_table(id, elem) {
    document.getElementById(id).style.removeProperty("display");
    document.getElementById(id + "_chart").parentElement.style.display = "none";
    elem.children[0].style.background = "#EAE9E9";
    elem.nextElementSibling.children[0].style.background = ""
}

function show_graph(id, elem) {
    document.getElementById(id + "_chart").parentElement.style.display = "block"
    document.getElementById(id).style.display = "none";
    elem.children[0].style.background = "#EAE9E9";
    elem.previousElementSibling.children[0].style.background = ""
}
