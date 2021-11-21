function amd_xlnx_ratio_graph() {
    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    var date_list = [], deal_exr_list = [], ratio_list = [], amd_price_list = [], xlnx_price_list = [], upside_list = [];
    var upside = ""
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td")
        date_list.push(td[0].innerHTML)
        amd_price_list.push(td[1].innerHTML)
        xlnx_price_list.push(td[2].innerHTML)
        upside = td[3].innerHTML
        upside_list.push(upside)
        ratio_list.push(td[4].innerHTML)
        deal_exr_list.push(1.7234)

        td[1].innerHTML = "$" + td[1].innerHTML
        td[2].innerHTML = "$" + td[2].innerHTML
        td[3].innerHTML = td[3].innerHTML + "%"
    }

    document.getElementsByClassName("instructions")[0].querySelector("p").innerHTML = `
        AMD CEO Lisa Su said its takeover of Xilinx is expected to be completed by the end of 2021.
        When the merger goes through, each XLNX share is converted into 1.7234 AMD share.
        <br>
        The percentage upside [100 * (1.7234 * AMD / XLNX - 1)] when buying XLNX is currently: <b>${upside}%</b>
    `

    var ratio_chart = document.getElementById('ratio_chart');
    var ratio_chart = new Chart(ratio_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Current Ratio',
                    type: 'line',
                    data: ratio_list,
                    backgroundColor: 'transparent',
                    borderColor: 'red',
                    borderWidth: 2,
                },
                {
                    label: 'Deal Exchange Ratio',
                    type: 'line',
                    data: deal_exr_list,
                    backgroundColor: 'transparent',
                    borderColor: '#39a6a6',
                    borderWidth: 2,
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Current Ratio',
                            beginAtZero: false,
                        },
                        type: "linear",
                        position:"left",
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                    }],

                xAxes: [{
                    ticks: {
                      maxTicksLimit: 12,
                      maxRotation: 30,
                      minRotation: 0,
                    },
                    type: "time",
                        distribution: 'series',
                        time: {
                            unit: "month"
                    },
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                }],
            },

            // To show value when hover on any part of the graph
            tooltips: {
                mode: 'index',
                intersect: false,
            },

            // To remove the point of each label
            elements: {
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

    var upside_chart = document.getElementById('percentage_upside_chart');
    var upside_chart = new Chart(upside_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: '% Upside if Buying XLNX',
                    type: 'line',
                    data: upside_list,
                    backgroundColor: 'transparent',
                    borderColor: 'blue',
                    borderWidth: 2,
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Percentage [%]',
                            beginAtZero: false,
                        },
                        type: "linear",
                        position:"left",
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                    }],

                xAxes: [{
                    ticks: {
                        maxTicksLimit: 12,
                        maxRotation: 30,
                        minRotation: 0,
                    },
                    type: "time",
                    distribution: 'series',
                    time: {
                        unit: "month"
                    },
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                    stacked: true
                }],
            },

            // To show value when hover on any part of the graph
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItem, data) {
                        var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        var label = data.datasets[tooltipItem.datasetIndex].label;
                        return label + ': ' + value + '%';
                    }
                },
            },

            // To remove the point of each label
            elements: {
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


    var price_chart = document.getElementById('price_chart');
    var price_chart = new Chart(price_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'AMD',
                    type: 'line',
                    data: amd_price_list,
                    backgroundColor: 'transparent',
                    borderColor: 'green',
                    borderWidth: 2,
                },
                {
                    label: 'XLNX',
                    type: 'line',
                    data: xlnx_price_list,
                    backgroundColor: 'transparent',
                    borderColor: 'orange',
                    borderWidth: 2,
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Price [$]',
                            beginAtZero: false,
                        },
                        type: "linear",
                        position:"left",
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                    }],

                xAxes: [{
                    ticks: {
                        maxTicksLimit: 12,
                        maxRotation: 30,
                        minRotation: 0,
                    },
                    type: "time",
                    distribution: 'series',
                    time: {
                        unit: "month"
                    },
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                    stacked: true
                }],
            },

            // To show value when hover on any part of the graph
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItem, data) {
                        var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        var label = data.datasets[tooltipItem.datasetIndex].label;
                        return label + ': ' + "$" + value;
                    }
                },
            },

            // To remove the point of each label
            elements: {
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
}