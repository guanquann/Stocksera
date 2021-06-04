function ftd_graph() {
    var ftd = document.getElementsByTagName("table")[0].querySelectorAll("tr");

    ftd[0].innerHTML = `
        <th>Date</th>
        <th>Failure to Deliver</th>
        <th>Price</th>`

    var date_list = [], price_list = [], vol_list = []
    for (tr=ftd.length-1; tr>0; tr--) {
        var total_td = ftd[tr].querySelectorAll("td");
        date_string = total_td[0].innerHTML;
        new_date_string = `${date_string.slice(0, 4)}/${date_string.slice(4, 6)}/${date_string.slice(6, 8)}`
        date_list.push(new_date_string);
        total_td[0].innerHTML = new_date_string;

        vol_list.push(total_td[1].innerHTML)

        price_list.push(total_td[2].innerHTML);
        total_td[2].innerHTML = "$" + total_td[2].innerHTML
    }

    var ftd_chart = document.getElementById('ftd_chart');
    var ftd_chart = new Chart(ftd_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'FTD',
                    type: 'line',
                    data: vol_list,
                    borderColor: 'wheat',
                    backgroundColor: 'transparent',
                    yAxisID: 'B',
                },
                {
                    label: 'Price',
                    type: 'line',
                    data: price_list,
                    backgroundColor: 'transparent',
                    borderColor: '#505050',
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
                            display: false
                        },
                        type: "linear",
                        id: "A",
                        stacked: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Price',
                            beginAtZero: false,
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return "$" + value;
                            }
                        },
                    },
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'FTD',
                            beginAtZero: false,
                        },
                        type: "linear",
                        id: "B",
                        position:"right",
                        gridLines: {
                            display: false
                        },
                    }],

                xAxes: [{
                    ticks: {
                      maxTicksLimit: 10,
                      maxRotation: 45,
                      minRotation: 0,
                    },
                    gridLines: {
                        drawOnChartArea: false
                    },
                    stacked: true
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
}