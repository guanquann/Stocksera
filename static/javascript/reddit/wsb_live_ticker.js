function load_ticker_graph() {
    tr = document.querySelectorAll("tr")
    mentions_list = [], sentiment_list = [], date_list = []

    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        mentions_list.push(td[0].innerHTML)
        sentiment_list.push(td[1].innerHTML)
        date_list.push(td[4].innerHTML)
    }

    var trace1 = {
        x: date_list,
        y: mentions_list,
        marker: {
            color: 'rgb(38, 166, 154)'
        },
        name: 'Mentions',
        hovertemplate:
                `<b>%{x|%d/%m (%H:%M)}</b><br>` +
                "Mentions: %{y}<br>" +
                "<extra></extra>",
        type: 'bar',
    };

    var trace2 = {
        x: date_list,
        y: sentiment_list,
        marker: {
            color: '#ffa500c4'
        },
        name: 'Sentiment',
        hovertemplate:
                `<b>%{x|%d/%m (%H:%M)}</b><br>` +
                "Sentiment: %{y}<br>" +
                "<extra></extra>",
        type: 'line',
        yaxis: 'y2'
    };

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
            title: {
                text: "Date (UTC)",
                font: {
                    size: 12
                }
            },
            tickformat: "%d/%m",
        },
        yaxis: {
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
        },
        yaxis2: {
            showgrid: false,
            showline: true,
            rangemode: 'tozero',
            range: [-1, 1],
            title: {
                text: 'Sentiment',
                font: {
                    size: 12,
                }
            },
            color: "gray",
            overlaying: 'y',
            side: 'right'
        },
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
        },
    };

    var data = [trace1, trace2]
    Plotly.newPlot('ticker_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});
}

function load_ticker_change() {
    comparison_div = document.querySelectorAll(".comparison")
    for (i=0; i<comparison_div.length; i++) {
        recent = comparison_div[i].querySelector(".recent").innerHTML
        prev = comparison_div[i].querySelector(".prev").innerHTML
        change = Math.round(10000 * (recent - prev) / prev) / 100
        comparison_div[i].querySelector(".change").innerHTML =isFinite(change) ? ` (${change}%)`: " (N/A)";
    }
}

function resize_plotly_graph() {
    Plotly.Plots.resize('ticker_chart')
}