function display_table() {
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        td[1].innerHTML = "$" + td[1].innerHTML + "B"
        td[2].innerHTML = td[2].innerHTML + "%"
    }
}

var retail_sales_chart = null

function retail_sales(duration) {
    var date_threshold = get_date_difference(duration, "-")

    var date_list = [], amount_list = [];
    var month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        date_string = td[0].innerHTML
        if (date_string >= date_threshold) {
            year = date_string.slice(0,4)
            month = month_list[Number(date_string.slice(5,7)) - 1]
            date_list.push(month + " " + year)
            amount_list.push(td[1].innerHTML.replace("$", "").replace("B", ""))
            tr[i].style.removeProperty("display")
        }
        else {
            tr[i].style.display = "none"
        }
    }

    if (retail_sales_chart != null){
        retail_sales_chart.destroy();
    }

    retail_sales_chart = document.getElementById('retail_sales_chart');
    retail_sales_chart = new Chart(retail_sales_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Retail Sales',
                    type: 'line',
                    data: amount_list,
                    borderColor: 'rgb(38, 166, 154)',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
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
                        position: 'left',
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        type: "linear",
                        id: "A",
                        scaleLabel: {
                            display: true,
                            labelString: 'Amount [$B]',
                            beginAtZero: true,
                        },
                    },
                    {
                        position: 'right',
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        type: "linear",
                        id: "B",
                        scaleLabel: {
                            display: true,
                            labelString: 'Covid Monthly Avg [K]',
                            beginAtZero: true,
                        },
                    },
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
                        if (label.includes("Sales")) {
                            return label + ': ' + value + 'B';
                        }
                        else {
                            return label + ': ' + Number(value).toLocaleString() + "K";
                        }
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
