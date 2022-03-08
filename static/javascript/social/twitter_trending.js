function trending_ticker_graph(symbol) {
    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    var date_list = [], tweet_list = [];
    for (i=1; i<tr.length; i++) {
        var td = tr[i].querySelectorAll("td")
        tweet_list.push(td[0].innerHTML)
        date_list.push(td[1].innerHTML)
    }

    var trending_ticker_chart = document.getElementById('trending_ticker_chart');
    var trending_ticker_chart = new Chart(trending_ticker_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: symbol,
                    type: 'bar',
                    data: tweet_list,
                    backgroundColor: 'rgb(38, 166, 154)',
                    borderColor: 'rgb(38, 166, 154)',
                    borderWidth: 2,
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Mentions',
                        },
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        ticks: {
                            beginAtZero: false
                        }
                    }],

                xAxes: [{
                    offset: true,
                    ticks: {
                       userCallback: function(label, index, labels) {
                         return moment(label, "YYYYMMDD").format("DD MMM YY");
                       },
                       maxTicksLimit: 12,
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