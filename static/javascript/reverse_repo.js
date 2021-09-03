function display_table() {
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
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
    }
    document.getElementById("consecutive_text").innerHTML =
    `As of ${tr[1].querySelector("td").innerHTML}, ${consecutive_num} consecutive days of RRP >= $1T.`
}

var reverse_repo_chart = null;

function reverse_repo(duration) {
    var date_threshold = get_date_difference(duration, "-")

    var date_list = [], amount_list = [], parties_list = [];
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        date_string = td[0].innerHTML
        if (date_string >= date_threshold) {
            date_list.push(date_string)
            amount_list.push(td[1].innerHTML.replace("$", "").replace("B", ""))
            parties_list.push(td[2].innerHTML)
            tr[i].style.removeProperty("display")
        }
        else {
            tr[i].style.display = "none"
        }
    }

    if (reverse_repo_chart != null){
        reverse_repo_chart.destroy();
    }

    reverse_repo_chart = document.getElementById('reverse_repo_chart');
    reverse_repo_chart = new Chart(reverse_repo_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Num Parties',
                    type: 'line',
                    data: parties_list,
                    pointRadius: 0,
                    borderWidth: 2,
                    borderColor: 'orange',
                    backgroundColor: 'transparent',
                    yAxisID: 'B',
                },
                {
                    label: 'Amount',
                    type: 'bar',
                    data: amount_list,
                    borderColor: 'rgb(38, 166, 154)',
                    backgroundColor: 'rgb(38, 166, 154)',
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
                            display: false
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
                            display: false
                        },
                        type: "linear",
                        id: "B",
                        scaleLabel: {
                            display: true,
                            labelString: 'Num Parties',
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