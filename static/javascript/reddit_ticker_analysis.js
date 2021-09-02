function rank_chart() {
    var ranking_list = [], date_list = [], price_list = [];
    var last_date = "";

    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=1; i<tr.length; i++) {
        var td = tr[i].querySelectorAll("td");
        var date_updated = td[3].innerHTML.split(" ")[0]
        ranking_list.push(td[0].innerHTML)
        price_list.push(td[2].innerHTML)
        date_list.push(date_updated)
    }

    var rank_chart = document.getElementById('rank_chart');
    var rank_chart = new Chart(rank_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Ranking',
                    type: 'line',
                    data: ranking_list,
                    borderColor: 'wheat',
                    backgroundColor: 'transparent',
                    yAxisID: 'A',
                },
                {
                    label: 'Price',
                    type: 'line',
                    data: price_list,
                    borderColor: 'rgb(38, 166, 154)',
                    backgroundColor: 'transparent',
                    yAxisID: 'B',
                }
                ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true
            },
            elements: {
                point:{
                    radius: 0
                },
                line: {
                    tension: 0
                },
            },
            scales: {
                yAxes: [
                    {
                        position: 'left',
                        gridLines: {
                            display: false
                        },
                        type: "linear",
                        id: "A",
                        scaleLabel: {
                            display: true,
                            labelString: 'Ranking',
                            beginAtZero: true,
                        },
                        ticks: {
//                            max: 100,
//                            min: 1,
                        },
                    },
                    {
                        position: 'right',
                        gridLines: {
                            display: false
                        },
                        type: "linear",
                        id: "B",
                        scaleLabel: {
                            display: true,
                            labelString: 'Price',
                            beginAtZero: false,
                        },
                    }
                    ],

                xAxes: [{
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
            },
            hover: {
                mode: 'index',
                intersect: false
            }
        },
    });
}