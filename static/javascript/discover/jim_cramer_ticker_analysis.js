function load_ticker_table() {
    tr = document.getElementsByTagName("table")[1].querySelectorAll("tr");
    date_list = [], close_list = [];
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        date_list.push(td[0].innerHTML)
        close_list.push(td[1].innerHTML)
    }

    buy_date_list = [], buy_price_list = [];
    positive_date_list = [], positive_price_list = [];
    hold_date_list = [], hold_price_list = [];
    negative_date_list = [], negative_price_list = [];
    sell_date_list = [], sell_price_list = [];
    cramer_performance = 0;
    var tr = document.querySelector("table").querySelectorAll("tr")
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        if (td[2].innerHTML == "Buy") {
            buy_date_list.push(td[0].innerHTML)
            buy_price_list.push(td[3].innerHTML)
        }
        else if (td[2].innerHTML == "Positive") {
            positive_date_list.push(td[0].innerHTML)
            positive_price_list.push(td[3].innerHTML)
        }
        else if (td[2].innerHTML == "Hold") {
            hold_date_list.push(td[0].innerHTML)
            hold_price_list.push(td[3].innerHTML)
        }
        else if (td[2].innerHTML == "Negative") {
            negative_date_list.push(td[0].innerHTML)
            negative_price_list.push(td[3].innerHTML)
        }
        else if (td[2].innerHTML == "Sell") {
            sell_date_list.push(td[0].innerHTML)
            sell_price_list.push(td[3].innerHTML)
        }
        else {
            continue
        }
        td[3].innerHTML = "$" + td[3].innerHTML
        cramer_performance += Number(td[4].innerHTML)
        td[4].innerHTML += "%"
        td[5].innerHTML += "%"
        td[4].parentElement.style.backgroundColor = td[4].innerHTML.includes("-") ? "#ff000054" : "#00800078"
        document.querySelector("#cramer_performance").innerHTML = Math.round(100 * cramer_performance / (tr.length-1)) / 100
    }

    var trace = {
        x: date_list,
        y: close_list,
        name: "Price",
        line: {'color': 'orange'},
        hovertemplate:
                "Price: $%{y}<br>" +
                "Date: %{x|%Y-%m-%d}" +
                "<extra></extra>",
        type: 'scatter'
    };

    var trace1 = {
        x: buy_date_list,
        y: buy_price_list,
        name: "Buy",
        mode: 'markers',
        line: {'color': 'rgb(38, 166, 154)'},
        hovertemplate:
                "Buy Price: $%{y}<br>" +
                "Date: %{x|%Y-%m-%d}" +
                "<extra></extra>",
        type: 'scatter'
    };

    var trace2 = {
        x: positive_date_list,
        y: positive_price_list,
        name: "Positive",
        mode: 'markers',
        line: {'color': 'lightgreen'},
        hovertemplate:
                "Positive Price: $%{y}<br>" +
                "Date: %{x|%Y-%m-%d}" +
                "<extra></extra>",
        type: 'scatter'
    };

    var trace3 = {
        x: hold_date_list,
        y: hold_price_list,
        name: "Hold",
        mode: 'markers',
        line: {'color': 'grey'},
        hovertemplate:
                "Hold Price: $%{y}<br>" +
                "Date: %{x|%Y-%m-%d}" +
                "<extra></extra>",
        type: 'scatter'
    };

    var trace4 = {
        x: negative_date_list,
        y: negative_price_list,
        name: "Negative",
        mode: 'markers',
        line: {'color': 'brown'},
        hovertemplate:
                "Negative Price: $%{y}<br>" +
                "Date: %{x|%Y-%m-%d}" +
                "<extra></extra>",
        type: 'scatter'
    };

    var trace5 = {
        x: sell_date_list,
        y: sell_price_list,
        name: "Sell",
        mode: 'markers',
        line: {'color': 'red'},
        hovertemplate:
                "Sell Price: $%{y}<br>" +
                "Date: %{x|%Y-%m-%d}" +
                "<extra></extra>",
        type: 'scatter'
    };

    var data = [trace, trace1, trace2, trace3, trace4, trace5];
    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:50,
            r:30,
            b: 40,
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
                text: "Date",
                font: {
                    size: 12
                }
            }
        },
        yaxis: {
            showgrid: false,
            showline: true,
            autorange: true,
            fixedrange: false,
            color: "gray",
            title: {
                text: 'Price [$]',
                font: {
                    size: 11,
                }
            },
        },
        legend: {
            x: 0.5,
            xanchor: 'center',
            y: 1.1,
            orientation: 'h',
            font: {
                size: 10,
            }
        },
    };

    Plotly.newPlot('price_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});
}

function toggle_checkbox(elem) {
    checkbox = document.getElementById(elem)
    tr = document.querySelector("table").querySelectorAll("tr");
    for (i=1; i<tr.length; i++) {
        if (tr[i].querySelector("td").innerHTML != "N/A") {
            tr[i].style.backgroundColor = tr[i].style.backgroundColor == "rgba(0, 128, 0, 0.47)" ? "rgba(255, 0, 0, 0.33)" : "rgba(0, 128, 0, 0.47)"
        }
    }
    if (elem == "pro") {
        document.querySelector("#inverse").checked = false
    }
    else {
        document.querySelector("#pro").checked = false
    }
    document.querySelector("#cramer_performance_title").innerHTML = document.querySelector("#cramer_performance_title").innerHTML == "Inverse Cramer's Performance" ? "Pro Cramer's Performance" : "Inverse Cramer's Performance"
    document.querySelector("#cramer_performance").innerHTML *= -1
}

function resize_plotly_graph() {
    Plotly.Plots.resize('price_chart')
}
