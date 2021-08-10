function daily_treasury(selected) {
    var date_list = [], close_list = []
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        date_list.push(td[0].innerHTML)
        close_list.push(td[1].innerHTML)
        td[1].innerHTML = "$" + td[1].innerHTML + "B"
        td[2].innerHTML = "$" + td[2].innerHTML + "B"
        if (td[3].innerHTML.includes("-")) {
            td[3].innerHTML = td[3].innerHTML.replace("-", "-$") + "B"
        }
        else {
            td[3].innerHTML = "$" + td[3].innerHTML + "B"
        }
        td[4].innerHTML = td[4].innerHTML + "%"
    }

    var daily_treasury_chart = document.getElementById('daily_treasury_chart');
    var daily_treasury_chart = new Chart(daily_treasury_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Close Balance',
                    type: 'bar',
                    data: close_list,
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
                            display: false
                        },
                        type: "linear",
                        scaleLabel: {
                            display: true,
                            labelString: 'Close Balance [$B]',
                            beginAtZero: true,
                        },
                    }
                    ],

                xAxes: [{
                    offset: true,
                    ticks: {
                      maxTicksLimit: 10,
                      maxRotation: 45,
                      minRotation: 0,
                    },
                    gridLines: {
                        drawOnChartArea: false
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
                        return label + ': ' + "$" + value + 'B';
                    }
                },
            },
            hover: {
                mode: 'index',
                intersect: false
            },
        },
    });

    document.getElementById(selected).classList.add("selected");
}