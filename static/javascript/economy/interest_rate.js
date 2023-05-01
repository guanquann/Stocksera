function display_table() {
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        td[1].innerHTML = td[2].innerHTML + "%"
    }
}

var ir_chart = null

function interest_rate(duration) {
    var date_threshold = get_date_difference(duration, "-")

    var date_list = [], amount_list = [];
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=1; i<tr.length;i++) {
        var td = tr[i].querySelectorAll("td");
        date_string = td[0].innerHTML
        if (date_string >= date_threshold) {
            date_list.push(date_string)
            amount_list.push(Number(td[1].innerHTML))
            tr[i].style.removeProperty("display")
        }
        else {
            tr[i].style.display = "none";
        }
    }

    if (ir_chart != null){
        ir_chart.destroy();
    }

    ir_chart = document.getElementById('ir_chart');
    ir_chart = new Chart(ir_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Interest Rate',
                    type: 'line',
                    data: amount_list,
                    borderColor: 'rgb(38, 166, 154)',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
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
                        position: 'left',
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        type: "linear",
                        scaleLabel: {
                            display: true,
                            labelString: 'Rate [%]',
                            beginAtZero: true,
                        },
                    }
                    ],

                xAxes: [{
                    offset: true,
                    ticks: {
                      maxTicksLimit: 10,
                      maxRotation: 30,
                      minRotation: 0,
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
                callbacks: {
                    label: function(tooltipItem, data) {
                        var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        var label = data.datasets[tooltipItem.datasetIndex].label;
                        return label + ': ' + value + "%";
                    }
                },
            },
            elements: {
                line: {
                    tension: 0
                },
                point:{
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
