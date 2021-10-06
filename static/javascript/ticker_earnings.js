function load_graph() {
    var query = document.getElementsByTagName("table");
    date_list = [], revenue_list = [], earnings_list = []

    var earnings_table = query[0].querySelectorAll("tr");
        for (i=earnings_table.length-1; i>0; i--) {
            td = earnings_table[i].querySelectorAll("td");
            date_list.push(td[0].innerHTML)
            if (td[1].innerHTML != "N/A") {
                rev = Number(td[1].innerHTML) / 1000000
                td[1].innerHTML = rev + "M"
                revenue_list.push(rev)

                earnings = Number(td[2].innerHTML) / 1000000
                td[2].innerHTML = earnings + "M"
                earnings_list.push(earnings)
            }
        }


    var tr = query[1].querySelectorAll("tr");
    if (tr[5].querySelectorAll("td")[1].innerHTML != "N/A") {
        tr[5].querySelectorAll("td")[1].innerHTML = tr[5].querySelectorAll("td")[1].innerHTML / 1000000 + "M"
        tr[6].querySelectorAll("td")[1].innerHTML = tr[6].querySelectorAll("td")[1].innerHTML / 1000000 + "M"
        tr[7].querySelectorAll("td")[1].innerHTML = tr[7].querySelectorAll("td")[1].innerHTML / 1000000 + "M"
    }

    var earnings_chart = document.getElementById('earnings_chart');
    var earnings_chart = new Chart(earnings_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Revenue',
                    type: 'bar',
                    data: revenue_list,
                    backgroundColor: 'orange',
                },
                {
                    label: 'Earnings',
                    type: 'bar',
                    data: earnings_list,
                    backgroundColor: 'red',
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
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        type: "linear",
                        scaleLabel: {
                            display: true,
                            labelString: 'Amount [M]',
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
                        drawOnChartArea: false,
                        color: "grey"
                    },
                    stacked: false
                }],
            },

            // To show value when hover on any part of the graph
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                title: tooltipItem => date_list[tooltipItem[0].index],
                label: function(tooltipItem, data) {
                    var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                    var label = data.datasets[tooltipItem.datasetIndex].label;
                    return label + ': ' + value + 'M';
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