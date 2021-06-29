function rank_chart() {
    var ranking_list = [], date_list = [], price_list = [];
    var last_date = "";

    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    for (i=1; i<tr.length; i++) {
        var td = tr[i].querySelectorAll("td");

        var date_updated = td[3].innerHTML.split(" ")[0]

        if (last_date == "") {
            last_date = date_updated
            theoretical_next_day = date_updated
        }
        else {
            js_date_format = last_date.slice(3,5) + "/" + last_date.slice(0,2) + "/" + + last_date.slice(6,10)

            theoretical_next_day = new Date(new Date(js_date_format).getTime() + 24*3600*1000)
            day_num = String(theoretical_next_day.getDate())
            if (day_num.length == 1) {
                day_num = "0" + day_num
            }
            month_num = String(theoretical_next_day.getMonth() + 1)
            if (month_num.length == 1) {
                month_num = "0" + month_num
            }
            year_num = String(theoretical_next_day.getFullYear())
            theoretical_next_day = day_num + "/" + month_num + "/" + year_num

            if (theoretical_next_day != date_updated) {
                ranking_list.push(100)
                date_list.push(theoretical_next_day)
                price_list.push(price_list[price_list.length-1])
            }
            last_date = date_updated
        }
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
            },
        },
    });
}