function display_table() {
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    var consecutive_num = 0
    var consecutive = true
    for (i=1; i<tr.length; i++) {
        var td = tr[i].querySelectorAll("td");
        td[1].innerHTML = "$" + td[1].innerHTML + "B"
        td[2].innerHTML = "$" + td[2].innerHTML + "B"
        if (td[3].innerHTML.includes("-")) {
            td[3].innerHTML = td[3].innerHTML.replace("-", "-$") + "B"
            if (consecutive == true) {
                consecutive_num += 1
            }
        }
        else {
            td[3].innerHTML = "$" + td[3].innerHTML + "B"
            consecutive = false
        }
        td[4].innerHTML = td[4].innerHTML + "%"
    }
    document.getElementById("consecutive_text").innerHTML =
    `As of ${tr[1].querySelector("td").innerHTML}, ${consecutive_num} consecutive days of decrease in daily treasury.`
}

var daily_treasury_chart = null;

function treasury(duration) {
    var date_threshold = get_date_difference(duration, "-")

    var date_list = [], close_list = []
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        date_string = td[0].innerHTML
        if (date_string >= date_threshold) {
            date_list.push(date_string)
            close_list.push(td[1].innerHTML.replace("$", "").replace("B", ""))
            tr[i].style.removeProperty("display")
        }
        else {
            tr[i].style.display = "none"
        }
    }

    if (daily_treasury_chart != null){
        daily_treasury_chart.destroy();
    }

    daily_treasury_chart = document.getElementById('daily_treasury_chart');
    daily_treasury_chart = new Chart(daily_treasury_chart, {
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
}