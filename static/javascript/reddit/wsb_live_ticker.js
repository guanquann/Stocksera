function load_ticker_graph(duration) {
    var date_threshold = get_date_difference(duration, "-")

    tr = document.getElementsByTagName("table")[0].querySelectorAll("tr")
    mentions_list = [], call_list = [], put_list = [], date_list = []

    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")

        date_string = td[3].innerHTML
        if (date_string >= date_threshold) {
            mentions_list.push(td[0].innerHTML)
            call_list.push(td[1].innerHTML)
            put_list.push(-td[2].innerHTML)
            date_list.push(date_string)
        }
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

    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:50,
            r:20,
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
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
        },
    };

    var data = [trace1]
    Plotly.newPlot('mentions_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});

    var trace1 = {
        x: date_list,
        y: call_list,
        marker: {
            color: 'green'
        },
        name: 'Calls',
        hovertemplate:
                `<b>%{x|%d/%m (%H:%M)}</b><br>` +
                "Calls: %{y}<br>" +
                "<extra></extra>",
        type: 'bar',
    };

    var trace2 = {
        x: date_list,
        y: put_list,
        marker: {
            color: 'red'
        },
        name: 'Puts',
        hovertemplate:
                `<b>%{x|%d/%m (%H:%M)}</b><br>` +
                "Puts: %{y}<br>" +
                "<extra></extra>",
        type: 'bar',
    };

    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:50,
            r:20,
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
                text: 'Calls / Puts Mentions',
                font: {
                    size: 12,
                }
            },
        },
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
        },
    };

    var data = [trace1, trace2]
    Plotly.newPlot('call_put_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});

    tr = document.getElementsByTagName("table")[1].querySelectorAll("tr")
    sentiment_list = [], date_list = []

    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")

        date_string = td[1].innerHTML
        if (date_string >= date_threshold) {
            sentiment_list.push(td[0].innerHTML)
            date_list.push(date_string)
        }
    }

    var trace1 = {
        x: date_list,
        y: sentiment_list,
        marker: {
            color: 'orange'
        },
        name: 'Sentiment',
        hovertemplate:
                `<b>%{x|%d/%m}</b><br>` +
                "Sentiment: %{y}<br>" +
                "<extra></extra>",
        type: 'bar',
    };

    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:50,
            r:20,
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
                text: 'Sentiment',
                font: {
                    size: 12,
                }
            },
        },
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
        },
    };

    var data = [trace1]
    Plotly.newPlot('sentiment_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});
}

function load_ticker_change() {
    comparison_div = document.querySelectorAll(".comparison")
    for (i=0; i<comparison_div.length; i++) {
        recent = comparison_div[i].querySelector(".recent").innerHTML
        prev = comparison_div[i].querySelector(".prev").innerHTML
        change = Math.round(10000 * (recent - prev) / prev) / 100
        comparison_div[i].querySelector(".change").innerHTML =isFinite(change) ? `${change}%`: "N/A";
    }
}

function resize_plotly_graph() {
    Plotly.Plots.resize('mentions_chart')
    Plotly.Plots.resize('call_put_chart')
}