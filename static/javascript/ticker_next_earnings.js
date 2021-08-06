function load_graph() {
    revenue_list = [], earnings_list = []
    var query = document.getElementsByTagName("table");
    if (query.length != 0) {
        var tr = query[0].querySelectorAll("tr");
        earnings_list.push(tr[2].querySelectorAll("td")[1].innerHTML, tr[1].querySelectorAll("td")[1].innerHTML, tr[3].querySelectorAll("td")[1].innerHTML)
        revenue_list.push(tr[5].querySelectorAll("td")[1].innerHTML / 1000000, tr[4].querySelectorAll("td")[1].innerHTML / 1000000, tr[6].querySelectorAll("td")[1].innerHTML / 1000000)

        tr[4].querySelectorAll("td")[1].innerHTML = tr[4].querySelectorAll("td")[1].innerHTML / 1000000 + "M"
        tr[5].querySelectorAll("td")[1].innerHTML = tr[5].querySelectorAll("td")[1].innerHTML / 1000000 + "M"
        tr[6].querySelectorAll("td")[1].innerHTML = tr[6].querySelectorAll("td")[1].innerHTML / 1000000 + "M"
    }

    var earnings_chart = document.getElementById('earnings_chart');
    var earnings_chart = new Chart(earnings_chart, {
        data: {
            labels: ["Low", "Avg", "High"],
            datasets: [
                {
                    label: 'Revenue',
                    type: 'bar',
                    data: revenue_list,
                    backgroundColor: 'wheat',
                    yAxisID: 'B',
                },
                {
                    label: 'Earnings',
                    type: 'bar',
                    data: earnings_list,
                    backgroundColor: 'red',
                    yAxisID: 'A',
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
                yAxes: [{
                        id: "A",
                        position: "right",
                        gridLines: {
                            display: false
                        },
                        type: "linear",
                        scaleLabel: {
                            display: true,
                            labelString: 'Earnings [$]',
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return "$" + value;
                            },
                            beginAtZero: true,
                        },
                    },
                    {
                        id: "B",
                        position: "left",
                        gridLines: {
                            display: false
                        },
                        type: "linear",
                        scaleLabel: {
                            display: true,
                            labelString: 'Revenue [$M]',
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return "$" + value + "M";
                            },
                            beginAtZero: true,
                        },
                    }],

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
                    stacked: false
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
            hover: {
                mode: 'index',
                intersect: false
            },
        },
    })

}