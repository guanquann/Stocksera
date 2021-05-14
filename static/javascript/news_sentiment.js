function display_data() {
    var main_content = document.getElementsByClassName("ticker_news");
    main_content[0].style.removeProperty("display");
    var tr = main_content[0].querySelector("table").getElementsByTagName("tr")

    var bearish_count = 0; bullish_count = 0; neutral_count = 0
    for (row=1; row<tr.length; row++) {
        if (tr[row].children[2].innerHTML == "Bearish") {
            tr[row].style.color = "red";
            bearish_count += 1;
        }
        else if (tr[row].children[2].innerHTML == "Bullish") {
            tr[row].style.color = "rgb(38, 166, 154)";
            bullish_count +=1
        }
        else {
            neutral_count +=1
        }
    }

    var latest_date = tr[tr.length-1].children[0].innerHTML
    var latest_date_list = [latest_date]
    var current_neu_num = 0, current_pos_num = 0, current_neg_num = 0
    var current_neu_list = [], current_pos_list = [], current_neg_list = []

    for (row=tr.length-1; row>=0; row--) {
        if (tr[row].children[0].innerHTML != latest_date) {
            latest_date = tr[row].children[0].innerHTML
            latest_date_list.push(latest_date)

            current_neu_list.push(current_neu_num)
            current_pos_list.push(current_pos_num)
            current_neg_list.push(current_neg_num)
            current_neu_num = 0, current_pos_num = 0, current_neg_num = 0
        }
        if (tr[row].children[2].innerHTML == "Bearish") {
            current_neg_num += 1
        }
        else if (tr[row].children[2].innerHTML == "Bullish") {
            current_pos_num += 1
        }
        else {
            current_neu_num += 1
        }

    }
    latest_date_list.pop()

    var personal_sentiment_chart = document.getElementById('personal_sentiment_chart');
    var myChart = new Chart(personal_sentiment_chart, {
        type: 'pie',
        data: {
            labels: ["Bearish", "Neutral", "Bullish"],
            datasets: [{
                data: [bearish_count, neutral_count, bullish_count],
                backgroundColor: [
                    'red',
                    'rgb(255, 205, 86)',
                    'rgb(38, 166, 154)',
                ],
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    })


    var personal_sentiment_trending = document.getElementById('personal_sentiment_trending');
    var myChart = new Chart(personal_sentiment_trending, {
        type: 'bar',
        data: {
            labels: latest_date_list,
            datasets: [{
                label: 'Positive',
                data: current_pos_list,
                backgroundColor: 'rgb(38, 166, 154)',
            },
            {
                label: 'Neutral',
                data: current_neu_list,
                backgroundColor: 'rgb(255, 205, 86)',
            },
            {
                label: 'Negative',
                data: current_neg_list,
                backgroundColor: 'red',
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: false
             },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function(value) {if (value % 1 === 0) {return value;}}
                    },
                    gridLines: {
                        drawOnChartArea: false
                    },
                    stacked: true
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
            hover: {
                mode: 'index',
                intersect: false
            },
        },
    });
}