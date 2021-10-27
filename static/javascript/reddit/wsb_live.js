function load_mkt_cap_chart(table_index) {
    ticker_list = [], mkt_cap_list = [], price_change_list = [], mentions_list = [], parent_list = []
    difference_list = [], difference_52w_high_list = [], difference_52w_low_list = []
    tr = document.getElementsByTagName("table")[table_index].querySelectorAll("tr")
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        ticker_list.push(td[0].innerHTML)
        mkt_cap_list.push(td[1].innerHTML)
        price_change_list.push(td[2].innerHTML)
        difference_list.push(td[3].innerHTML)
        difference_52w_high_list.push(td[4].innerHTML)
        difference_52w_low_list.push(td[5].innerHTML)
        mentions_list.push(td[6].innerHTML)
        parent_list.push("")
    }

    mentions_list_sm = mentions_list.map(bb_size)
    function bb_size(num) {
        num = num / 10
        if (num < 8) {
            num = 8
        }
        return num
    }

    var trace1 = {
        x: mkt_cap_list,
        y: mentions_list,
        customdata: ticker_list,
        text: mentions_list.map(String),
        hovertemplate:
                `<b>$%{customdata}</b><br>` +
                "Mentions: %{y}<br>" +
                "Mkt Cap: %{x}<br>" +
                "<extra></extra>",
        textposition: 'auto',
        mode: 'markers',
        marker: {
            size: mentions_list_sm,
            color: "rgb(38, 166, 154)"
        }
    };

    var data = [trace1];

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
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
        },
        xaxis: {
            showgrid: false,
            showline: true,
            color: "gray",
            rangemode: 'tozero',
            type: 'log',
            autorange: true,
            title: {
                text: 'Log. Mkt Cap',
                font: {
                    size: 12,
                }
            },
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
    }

    Plotly.newPlot('mkt_cap_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true})

    var data = [{
        type: 'treemap',
        values: mentions_list,
        labels: ticker_list,
        parents: parent_list,
        customdata: price_change_list,
        marker: {
            cmin: -10,
            cmax: 10,
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
            colors: price_change_list,
        },
        hovertemplate: "<b>%{label}</b><br>Mentions: %{value}<br>Price Change: %{color:.2f}%<br><extra></extra>",
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

    Plotly.newPlot('price_change_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true})
        .then(gd => {
        gd.on("plotly_treemapclick", () => false)
    })

    var trace1 = {
        x: difference_list.slice(0, 15).reverse(),
        y: ticker_list.slice(0, 15).reverse(),
        mode: 'markers',
        type: 'scatter',
        name: '50SMA',
        hovertemplate: `<b>$%{y}</b><br>Diff. 50SMA: %{x}%<extra></extra>`,
        marker: {
            size: 12,
            color: "orange"
        }
    };

    var trace2 = {
        x: difference_52w_high_list.slice(0, 15).reverse(),
        y: ticker_list.slice(0, 15).reverse(),
        mode: 'markers',
        type: 'scatter',
        name: '52H',
        hovertemplate: `<b>$%{y}</b><br>Diff. 52W High: %{x}%<extra></extra>`,
        marker: {
            size: 12,
            color: "rgb(38, 166, 154)"
        }
    };

    var trace3 = {
        x: difference_52w_low_list.slice(0, 15).reverse(),
        y: ticker_list.slice(0, 15).reverse(),
        mode: 'markers',
        type: 'scatter',
        name: '52L',
        hovertemplate: `<b>$%{y}</b><br>Diff. 52W Low: %{x}%<extra></extra>`,
        marker: {
            size: 12,
            color: "darkred"
        }
    };

    var data = [trace1, trace2, trace3];

    var layout = {
        xaxis: {
            showgrid: false,
            showline: true,
            rangemode: 'tozero',
            color: "gray",
            title: {
                text: "% Difference",
                font: {
                    size: 12
                }
            },
        },
        yaxis: {
            showgrid: false,
            showline: true,
            rangemode: 'tozero',
            color: "gray",
        },
        autosize: true,
        margin: {
            t: 0,
            l: 50,
            r: 20,
            pad: 0
        },
        automargin: true,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.05,
            orientation: 'h',
        },
        annotations: [
            {
                  x: 10,
                  y: -1,
                  xref: 'x',
                  yref: 'y',
                  text: 'Current Price',
                  showarrow: false,
            }
        ]
    };

    Plotly.newPlot('50SMA_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});
}

function load_options_chart(table_index) {
    call_list = [], put_list = [], ticker_list = []
    tr = document.getElementsByTagName("table")[table_index].querySelectorAll("tr")

    th = tr[0].querySelectorAll("th")
    th[1].style.display = "none"
    th[2].style.display = "none"

    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        ticker_list.push(td[0].innerHTML)
        call_list.push(td[1].innerHTML)
        put_list.push(td[2].innerHTML)
        td[1].style.display = "none"
        td[2].style.display = "none"
    }
    var trace1 = {
        x: ticker_list,
        y: call_list,
        name: 'Calls',
        marker: {
            color: 'darkgreen',
        },
        hovertemplate:
                `<b>$%{x}</b><br>` +
                "Calls: %{y}<br>" +
                "<extra></extra>",
        type: 'bar',
    };

    var trace2 = {
        x: ticker_list,
        y: put_list,
        name: 'Puts',
        marker: {
            color: 'darkred',
        },
        hovertemplate:
                `<b>$%{x}</b><br>` +
                "Puts: %{y}<br>" +
                "<extra></extra>",
        type: 'bar',
    };

    var layout = {
        barmode: 'stack',
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

    var data = [trace1, trace2]
    Plotly.newPlot('options_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});
}

function resize_plotly_graph() {
    Plotly.Plots.resize('trending_over_time_chart_24H')
    Plotly.Plots.resize('trending_over_time_chart_7d')
    Plotly.Plots.resize('change_mentions')
    Plotly.Plots.resize('mkt_cap_chart')
    Plotly.Plots.resize('price_change_chart')
    Plotly.Plots.resize('50SMA_chart')
    Plotly.Plots.resize('sentiment_chart')
    Plotly.Plots.resize('options_chart')
}