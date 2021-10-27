function load_trending_over_time_chart(trending_list, period) {
    date_1_list = [], ticker_1_list = []
    for (ticker in trending_list[0]) {
        mentions = trending_list[0][ticker]
        date_1_list.push(mentions[1])
        ticker_1_list.push(mentions[2])
    }

    hovertemplate = "Mentions: %{y}<br>%{x|%d/%m (%H:%M)}<br><extra></extra>"

    var trace1 = {
        x: date_1_list,
        y: ticker_1_list,
        name: trending_list[0][0][0],
        line: {'color': 'rgb(38, 166, 154)'},
        hovertemplate:`<b>$${trending_list[0][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines',
    };

    date_2_list = [], ticker_2_list = []
    for (ticker in trending_list[1]) {
        mentions = trending_list[1][ticker]
        date_2_list.push(mentions[1])
        ticker_2_list.push(mentions[2])
    }

    var trace2 = {
        x: date_2_list,
        y: ticker_2_list,
        name: trending_list[1][0][0],
        line: {'color': 'blue'},
        hovertemplate: `<b>$${trending_list[1][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    date_3_list = [], ticker_3_list = []
    for (ticker in trending_list[2]) {
        mentions = trending_list[2][ticker]
        date_3_list.push(mentions[1])
        ticker_3_list.push(mentions[2])
    }

    var trace3 = {
        x: date_3_list,
        y: ticker_3_list,
        name: trending_list[2][0][0],
        line: {'color': 'purple'},
        hovertemplate: `<b>$${trending_list[2][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    date_4_list = [], ticker_4_list = []
    for (ticker in trending_list[3]) {
        mentions = trending_list[3][ticker]
        date_4_list.push(mentions[1])
        ticker_4_list.push(mentions[2])
    }

    var trace4 = {
        x: date_4_list,
        y: ticker_4_list,
        name: trending_list[3][0][0],
        line: {'color': 'grey'},
        hovertemplate: `<b>$${trending_list[3][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    date_5_list = [], ticker_5_list = []
    for (ticker in trending_list[4]) {
        mentions = trending_list[4][ticker]
        date_5_list.push(mentions[1])
        ticker_5_list.push(mentions[2])
    }

    var trace5 = {
        x: date_5_list,
        y: ticker_5_list,
        name: trending_list[4][0][0],
        line: {'color': 'yellow'},
        hovertemplate: `<b>$${trending_list[4][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    date_6_list = [], ticker_6_list = []
    for (ticker in trending_list[5]) {
        mentions = trending_list[5][ticker]
        date_6_list.push(mentions[1])
        ticker_6_list.push(mentions[2])
    }

    var trace6 = {
        x: date_6_list,
        y: ticker_6_list,
        name: trending_list[5][0][0],
        line: {'color': 'brown'},
        hovertemplate: `<b>$${trending_list[5][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    date_7_list = [], ticker_7_list = []
    for (ticker in trending_list[6]) {
        mentions = trending_list[6][ticker]
        date_7_list.push(mentions[1])
        ticker_7_list.push(mentions[2])
    }

    var trace7 = {
        x: date_7_list,
        y: ticker_7_list,
        name: trending_list[6][0][0],
        line: {'color': 'orange'},
        hovertemplate: `<b>$${trending_list[6][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    date_8_list = [], ticker_8_list = []
    for (ticker in trending_list[7]) {
        mentions = trending_list[7][ticker]
        date_8_list.push(mentions[1])
        ticker_8_list.push(mentions[2])
    }

    var trace8 = {
        x: date_8_list,
        y: ticker_8_list,
        name: trending_list[7][0][0],
        line: {'color': '#9c6679'},
        hovertemplate: `<b>$${trending_list[7][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    date_9_list = [], ticker_9_list = []
    for (ticker in trending_list[8]) {
        mentions = trending_list[8][ticker]
        date_9_list.push(mentions[1])
        ticker_9_list.push(mentions[2])
    }

    var trace9 = {
        x: date_9_list,
        y: ticker_9_list,
        name: trending_list[8][0][0],
        line: {'color': 'wheat'},
        hovertemplate: `<b>$${trending_list[8][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    date_10_list = [], ticker_10_list = []
    for (ticker in trending_list[9]) {
        mentions = trending_list[9][ticker]
        date_10_list.push(mentions[1])
        ticker_10_list.push(mentions[2])
    }

    var trace10 = {
        x: date_10_list,
        y: ticker_10_list,
        name: trending_list[9][0][0],
        line: {'color': 'red'},
        hovertemplate: `<b>$${trending_list[9][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    date_11_list = [], ticker_11_list = []
    for (ticker in trending_list[10]) {
        mentions = trending_list[10][ticker]
        date_11_list.push(mentions[1])
        ticker_11_list.push(mentions[2])
    }

    var trace11 = {
        x: date_11_list,
        y: ticker_11_list,
        name: trending_list[10][0][0],
        line: {'color': 'green'},
        hovertemplate: `<b>$${trending_list[10][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    date_12_list = [], ticker_12_list = []
    for (ticker in trending_list[11]) {
        mentions = trending_list[11][ticker]
        date_12_list.push(mentions[1])
        ticker_12_list.push(mentions[2])
    }

    var trace12 = {
        x: date_12_list,
        y: ticker_12_list,
        name: trending_list[11][0][0],
        line: {'color': 'lightblue'},
        hovertemplate: `<b>$${trending_list[11][0][0]}</b><br>` + hovertemplate,
        type: 'line',
        mode: 'lines'
    };

    if (period == "24H") {
        xaxis = "Time (UTC)"
        tickformat = "%H:%M"
    }
    else {
        xaxis = "Date (UTC)"
        tickformat = "%d/%m"
    }

    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:50,
            r:0,
            pad: 0
        },
        automargin: true,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        xaxis: {
            showgrid: false,
            showline: true,
            color: "gray",
            title: {
                text: xaxis,
                font: {
                    size: 12
                }
            },
            tickformat: tickformat
        },
        yaxis: {
            showgrid: false,
            showline: true,
            rangemode: 'tozero',
            color: "gray",
            title: {
                text: 'No. of Mentions',
                font: {
                    size: 12
                }
            },
        },
        hovermode:'closest',
    };

    var data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10, trace11, trace12];

    if (period == "24H") {
        Plotly.newPlot('trending_over_time_chart_24H', data, layout, {displayModeBar: false, showTips: false, responsive: true});
    }
    else {
        Plotly.newPlot('trending_over_time_chart_7d', data, layout, {displayModeBar: false, showTips: false, responsive: true});
    }
}

function load_change_chart(table_index) {
    ticker_list = [], mentions_list = [], change_list = [], parent_list = []
    tr = document.getElementsByTagName("table")[table_index].querySelectorAll("tr")
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        ticker_list.push(td[0].innerHTML)
        mentions_list.push(td[1].innerHTML)
        change_list.push(Math.floor(td[2].innerHTML))
        parent_list.push("")
    }

    var data = [{
        type: 'treemap',
        values: mentions_list,
        labels: ticker_list,
        parents: parent_list,
        customdata: change_list,
        marker: {
            cmin: -200,
            cmax: 200,
            cmid: 0,
            colorscale: [
                ['0.0', 'rgb(255, 40, 30)'],
                ['0.1', 'rgb(246, 53, 56)'],
                ['0.2', 'rgb(191, 64, 69)'],
                ['0.3', 'rgb(139, 68, 78)'],
                ['0.4', 'rgb(100, 73, 83)'],
                ['0.5', 'rgb(65, 69, 84)'],
                ['0.6', 'rgb(53, 118, 78)'],
                ['0.7', 'rgb(47, 158, 79)'],
                ['0.8', 'rgb(47, 158, 79)'],
                ['0.9', 'rgb(48, 204, 90)'],
                ['1.0', 'rgb(48, 255, 100)'],
            ],
            colors: change_list,
        },
        hovertemplate: "<b>%{label}</b><br>Mentions: %{value}<br>Change: %{customdata}%<br><extra></extra>",
        textposition: "center",
        texttemplate: "<b>%{label}</b><br>%{customdata}%",
    }]

    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:10,
            r:10,
            b: 15,
            pad: 0
        },
        automargin: true,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
        },
    }

    Plotly.newPlot('change_mentions', data, layout, {displayModeBar: false, showTips: false, responsive: true})
        .then(gd => {
            gd.on("plotly_treemapclick", () => false)
        })
}

function load_sentiment_chart(table_index, link) {
    ticker_list = [], sentiment_list = [], mentions_list = []
    tr = document.getElementsByTagName("table")[table_index].querySelectorAll("tr")
    for (i=1; i<31; i++) {
        td = tr[i].querySelectorAll("td")
        ticker_list.push(td[1].innerHTML)
        mentions_list.push(td[2].innerHTML)
        sentiment_list.push(td[3].innerHTML)
    }

    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        td[1].innerHTML = `<a href="/${link}_live_ticker/?quote=${td[1].innerHTML}"><b>${td[1].innerHTML}</b></a>`
    }

    var trace1 = {
        x: ticker_list,
        y: mentions_list,
        line: {'color': '#4444b1'},
        name: 'Mentions',
        hovertemplate:
                `<b>$%{x}</b><br>` +
                "Mentions: %{y}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines+markers',
        yaxis: 'y2'
    };

    var trace2 = {
        x: ticker_list,
        y: sentiment_list,
        name: 'Net Sentiment',
        marker: {
            color: '#ffa500c4',
        },
        hovertemplate:
                `<b>$%{x}</b><br>` +
                "Sentiment: %{y}%<br>" +
                "<extra></extra>",
        type: 'bar',
    };

    trace2.marker.color = trace2.y.map(function (v) {
      return v <= 0  ? '#ff0000ad' : 'rgb(38, 166, 154)'
    });

    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:50,
            r:50,
            pad: 0
        },
        automargin: true,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        xaxis: {
            showgrid: false,
            showline: true,
            color: "gray",
            rangemode: 'tozero',
            range: [-0.5, 30]
        },
        yaxis2: {
            showgrid: false,
            showline: true,
            rangemode: 'tozero',
            color: "gray",
            title: {
                text: 'No. of Mentions',
                font: {
                    size: 12,
                }
            },
            side: 'right'
        },
        yaxis: {
            showgrid: false,
            showline: true,
            rangemode: 'tozero',
            title: {
                text: 'Sentiment',
                font: {
                    size: 12,
                }
            },
            color: "gray",
        },
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
        },
    };

    var data = [trace2, trace1]
    Plotly.newPlot('sentiment_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});
}

function load_word_cloud(word_list){
    data = []
    for (i in word_list) {
        row = word_list[i]
        data.push({"x": row[0], "value": row[1]})
    }
    anychart.onDocumentReady(function() {
        var chart = anychart.tagCloud(data);
        chart.title().enabled(false);
        chart.angles([0])
        chart.colorRange(false);
        chart.container("word_cloud");
        chart.background().fill("transparent");
        chart.tooltip().useHtml(true);
        chart.tooltip().format(function() {
            return `<span>Mentions: ${this.getData("value")}</span>`
        });
        chart.tooltip().background().fill("gray");
        chart.draw();
    })
}

const searchTicker = (elem, table_index) =>{
let filter = elem.value.toUpperCase();
let filter_table = document.querySelectorAll("table")[table_index];
let tr = filter_table.getElementsByTagName('tr');
for (var i = 0; i < tr.length; i++){
    let td = tr[i].getElementsByTagName('td')[1];
    if(td) {
            let textValue = td.textContent || td.innerHTML;
            if (textValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display="";
            }
            else {
                tr[i].style.display="none";
            }
        }
    }
}

function show_banned_words(elem) {
    if (elem.className == "hidden") {
        document.querySelector("#banned_words_div").style.removeProperty("display")
        elem.classList.remove("hidden")
        elem.innerHTML = "Hide"
    }
    else {
        document.querySelector("#banned_words_div").style.display = "none"
        elem.classList.add("hidden")
        elem.innerHTML = "To see the list of excluded words, click here."
    }
}