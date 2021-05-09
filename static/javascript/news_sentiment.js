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

}