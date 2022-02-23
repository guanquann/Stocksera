function display_table() {
    var trs = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    for (tr=trs.length-1; tr>0; tr--) {
        var tds = trs[tr].querySelectorAll("td")
        tds[0].innerHTML = tds[0].innerHTML + "%"
        tds[1].innerHTML = Number(tds[1].innerHTML).toLocaleString()
    }
}

var borrowed_shares_chart = null;

function borrowed_shares_graph(duration) {
    var date_threshold = get_date_difference(duration, "-")

    if (duration <= 6) {
        date_unit = "day"
    }
    else {
        date_unit = "month"
    }

    var trs = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    var date_list = [], available_list = [], fee_list = []
    for (tr=trs.length-1; tr>0; tr--) {
        var total_td = trs[tr].querySelectorAll("td");
        date_string = total_td[2].innerHTML;

        date_list.push(date_string)
        fee_list.push(total_td[0].innerHTML)
        available_list.push(total_td[1].innerHTML)
    }

    if (borrowed_shares_chart != null) {
        borrowed_shares_chart.destroy();
    }

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
//                            max: 100,
//                            min: 0,
                            callback: function(value, index, values) {
                                return value;
                            },
                            beginAtZero: true,
                        },
                    }],

                xAxes: [{
                    type: "time",
                    distribution: 'series',
//                    time: {
//                        unit: date_unit
//                    },
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
}
