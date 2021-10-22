function display_table() {
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    tr[0].querySelectorAll("th")[4].style.display = "none"
    var consecutive_num = 0
    var consecutive = true
    for (i=1; i<tr.length; i++) {
        var td = tr[i].querySelectorAll("td");
        if (td[1].innerHTML >= 1000 && consecutive == true) {
            consecutive_num += 1
        }
        else {
            consecutive = false
        }
        td[1].innerHTML = "$" + td[1].innerHTML + "B"
        td[3].innerHTML = "$" + td[3].innerHTML + "B"
        td[4].style.display = "none"
    }
    document.getElementById("consecutive_text").innerHTML =
    `As of ${tr[1].querySelector("td").innerHTML}, ${consecutive_num} consecutive days of RRP >= $1T.`
}

var reverse_repo_chart = null;
var avg_participants_chart = null;

function reverse_repo(duration) {
    var date_threshold = get_date_difference(duration, "-")

    if (duration <= 6) {
        date_unit = "day"
    }
    else {
        date_unit = "month"
    }

    var date_list = [], amount_list = [], parties_list = [], avg_list = [], moving_avg_list = [];
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        date_string = td[0].innerHTML
        if (date_string >= date_threshold) {
            date_list.push(date_string)
            amount_list.push(td[1].innerHTML.replace("$", "").replace("B", ""))
            parties_list.push(td[2].innerHTML)
            avg_list.push(td[3].innerHTML.replace("$", "").replace("B", ""))
            moving_avg_list.push(td[4].innerHTML)
            tr[i].style.removeProperty("display")
        }
        else {
            tr[i].style.display = "none"
        }
    }

    if (reverse_repo_chart != null){
        reverse_repo_chart.destroy();
        avg_participants_chart.destroy();
    }

    reverse_repo_chart = document.getElementById('reverse_repo_chart');
    reverse_repo_chart = new Chart(reverse_repo_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Moving Avg (7D)',
                    type: 'line',
                    data: moving_avg_list,
                    pointRadius: 0,
                    borderWidth: 2,
                    borderColor: 'red',
                    backgroundColor: 'transparent',
                },
                {
                    label: 'Amount',
                    type: 'bar',
                    data: amount_list,
                    borderColor: 'rgb(38, 166, 154)',
                    backgroundColor: 'rgb(38, 166, 154)',
                }
                ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true
             },
            scales: {
                yAxes: [
                    {
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey"
                        },
                        type: "linear",
                        scaleLabel: {
                            display: true,
                            labelString: 'Amount [$B]',
                            beginAtZero: true,
                        },
                    }
                    ],
                xAxes: [{
                    type: "time",
                    distribution: 'series',
                    time: {
                        unit: date_unit
                    },
                    offset: true,
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey"
                    },
                    ticks: {
                        maxTicksLimit: 10,
                        maxRotation: 30,
                        minRotation: 0,
                    },
                }],
            },
            elements: {
                line: {
                    tension: 0
                }
            },
            hover: {
                mode: 'index',
                intersect: false
            },
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItem, data) {
                        var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        var label = data.datasets[tooltipItem.datasetIndex].label;
                        return label + ': ' + value + 'B';
                    }
                }
            },
        },
    });


    avg_participants_chart = document.getElementById('avg_participants_chart');
    avg_participants_chart = new Chart(avg_participants_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'No. Parties',
                    type: 'line',
                    data: parties_list,
                    pointRadius: 0,
                    borderWidth: 2,
                    borderColor: 'orange',
                    backgroundColor: 'transparent',
                    yAxisID: 'B',
                },
                {
                    label: 'Avg / Party',
                    type: 'bar',
                    data: avg_list,
                    borderColor: 'purple',
                    backgroundColor: 'purple',
                    yAxisID: 'A',
                }
                ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true
            },
            scales: {
                yAxes: [
                    {
                        position: 'right',
                        gridLines: {
                            display: false
                        },
                        ticks: {
                            display: false
                        },
                        type: "linear",
                        id: "A",
                        scaleLabel: {
                            display: false,
                            beginAtZero: true,
                        },
                    },
                    {
                        position: 'left',
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey"
                        },
                        ticks: {
                            display: true
                        },
                        type: "linear",
                        id: "B",
                        scaleLabel: {
                            display: true,
                            labelString: 'No. Parties',
                            beginAtZero: true,
                        },

                    }
                    ],

                xAxes: [{
                    type: "time",
                    distribution: 'series',
                    time: {
                        unit: date_unit
                    },
                    offset: true,
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey"
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
                        if (label == "No. Parties") {
                            return label + ': ' + value;
                        }
                        else {
                            return label + ': ' + value + 'B';
                        }
                    }
                }
            },
            elements: {
                line: {
                    tension: 0
                }
            },
            hover: {
                mode: 'index',
                intersect: false
            },
        },
    });
}