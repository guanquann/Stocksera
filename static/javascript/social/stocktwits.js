function trending_ticker_graph(symbol) {
    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    var date_list = [], rank_list = [], watchlist_list = [];
    for (i=1; i<tr.length; i++) {
        var td = tr[i].querySelectorAll("td")
        rank_list.push(td[0].innerHTML)
        watchlist_list.push(td[1].innerHTML)
        date_list.push(td[2].innerHTML)
    }

    var tr = document.getElementsByTagName("table")[2].querySelectorAll("tr");
    var price_date_list = [], price_list = [], volume_list = [];
    for (i=1; i<tr.length; i++) {
        var td = tr[i].querySelectorAll("td")
        price_date_list.push(td[0].innerHTML)
        price_list.push(td[1].innerHTML)
        volume_list.push(td[2].innerHTML)
    }

    var trace1 = {
        x: date_list,
        y: rank_list,
        name: "Rank",
        marker: {
            color: 'rgb(38, 166, 154)'
        },
        hovertemplate:
                `<b>%{x|%d/%m/%Y (%H:%M)}</b><br>` +
                "Rank: %{y}<br>" +
                "<extra></extra>",
        type: 'bar'
    };
    var trace2 = {
        x: date_list,
        y: watchlist_list,
        yaxis: 'y2',
        name: "Watchlist Count",
        marker: {
            color: 'red'
        },
        hovertemplate:
                `<b>%{x|%d/%m/%Y (%H:%M)}</b><br>` +
                "Watchlist Count: %{y}<br>" +
                "<extra></extra>",
        type: 'scatter'
    };
    var layout = {
        autosize: true,
        margin: {
            t:30,
            l:60,
            r:60,
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
                text: 'Date',
                font: {
                      size: 12,
                }
            },
        },
        yaxis: {
            showgrid: false,
            showline: true,
            color: "gray",
            title: {
                text: 'Rank',
                font: {
                      size: 12,
                }
            },
        },
        yaxis2: {
            showgrid: false,
            showline: true,
            color: "gray",
            title: {
                text: 'Watchlist Count',
                font: {
                      size: 12,
                }
            },
            overlaying: 'y',
            side: 'right',
        },
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
            font: {
                size: 12,
            }
        },
    };
    var data = [trace1, trace2,];
    Plotly.newPlot('trending_ticker_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});

    var trace1 = {
        x: price_date_list,
        y: volume_list,
        name: "Volume",
        marker: {
            color: 'lightblue'
        },
        hovertemplate:
                `<b>%{x|%d/%m/%Y (%H:%M)}</b><br>` +
                "Volume: %{y}<br>" +
                "<extra></extra>",
        type: 'bar'
    };
    var trace2 = {
        x: price_date_list,
        y: price_list,
        yaxis: 'y2',
        name: "Price",
        hovertemplate:
                `<b>%{x|%d/%m/%Y}</b><br>` +
                "Price: $%{y}<br>" +
                "<extra></extra>",
        type: 'scatter'
    };
    var layout = {
        autosize: true,
        margin: {
            t:30,
            l:60,
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
            title: {
                text: 'Date',
                font: {
                      size: 12,
                }
            },
        },
        yaxis: {
            showgrid: false,
            showline: true,
            color: "gray",
            title: {
                text: 'Volume',
                font: {
                      size: 12,
                }
            },
        },
        yaxis2: {
            showgrid: false,
            showline: true,
            color: "gray",
            title: {
                text: 'Price',
                font: {
                      size: 12,
                }
            },
            overlaying: 'y',
            side: 'right',
        },
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
            font: {
                size: 12,
            }
        },
    };
    var data = [trace1, trace2];
    Plotly.newPlot('price_ticker_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});
}

function load_top30(symbol) {
    var tr = document.getElementsByTagName("table")[1].querySelectorAll("tr");
    top30_code = ""
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        current_symbol = td[2].innerHTML
        if (symbol == current_symbol) {
            color = "rgb(38, 166, 154)"
        }
        else {
            color = "inherit"
        }
        top30_code += `<a href="/stocktwits/?quote=${current_symbol}" style="color: ${color}">
                       <div class="top30_individual_div" style="color: ${color}; border-color: ${color}">
                           <div><b>${current_symbol}</b></div>
                           <div>Rank: ${td[0].innerHTML}</div>
                           <div>Watchlist: ${td[1].innerHTML}</div>
                       </div>
                       </a>`
    }
    document.querySelector("#top30_div").innerHTML = top30_code
}

const buttonRight = document.getElementById('slideRight');
const buttonLeft = document.getElementById('slideLeft');

buttonRight.onclick = function () {
    document.getElementById('top30_div').scrollLeft += 220;
};
buttonLeft.onclick = function () {
    document.getElementById('top30_div').scrollLeft -= 220;
};

function resize_plotly_graph() {
    Plotly.Plots.resize('trending_ticker_chart')
    Plotly.Plots.resize('price_ticker_chart')
}