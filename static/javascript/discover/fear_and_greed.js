var fng_chart = null;

function fear_and_greed(duration) {
    var date_threshold = get_date_difference(duration, "-")

    if (duration <= 6) {
        date_unit = "day"
    }
    else {
        date_unit = "month"
    }

    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");

    var date_list = [], value_list = [];

    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        var date_string = td[0].innerHTML;
        if (date_string >= date_threshold) {
            date_list.push(date_string)
            value_list.push(td[1].innerHTML)
        }
    }

    if (fng_chart != null){
        fng_chart.destroy();
    }

    fng_chart = document.getElementById('fng_chart');
    fng_chart = new Chart(fng_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Value',
                    type: 'line',
                    data: value_list,
                    pointRadius: 0,
                    borderWidth: 2,
                    borderColor: 'red',
                    backgroundColor: 'transparent',
                },
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
                            color: "grey",
                        },
                        type: "linear",
                        scaleLabel: {
                            display: true,
                            labelString: 'Fear and Greed Value',
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
                        color: "grey",
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
            tooltips: {
                mode: 'index',
                intersect: false
            },
            hover: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                annotation: {
                    annotations: [
                        {
                            type: 'line',
                            mode: 'vertical',
                            scaleID: 'x-axis-0',
                            value: 20,
                            borderColor: 'red',
                            borderWidth: 2,
                        }
                    ]
                }
            },    
        },
    });
}