function display_table() {
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        td[1].innerHTML = Number(td[1].innerHTML).toLocaleString()
        td[2].innerHTML = td[2].innerHTML + "%"
    }
}

var ijc_chart = null

function initial_jobless_claims(duration) {
    var date_threshold = get_date_difference(duration, "-")

    var date_list = [], amount_list = [];
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        date_string = td[0].innerHTML
        if (date_string >= date_threshold) {
            date_list.push(date_string)
            amount_list.push(td[1].innerHTML.replace(/\D/g,'') / 1000)
            tr[i].style.removeProperty("display")
        }
        else {
            tr[i].style.display = "none"
        }
    }

    if (ijc_chart != null){
        ijc_chart.destroy();
    }

    ijc_chart = document.getElementById('ijc_chart');
    ijc_chart = new Chart(ijc_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Initial Jobless Claims',
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
                            labelString: 'Number [K]',
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
                        return label + ': ' + Number(value * 1000).toLocaleString();
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
