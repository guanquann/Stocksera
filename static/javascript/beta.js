function load_beta_graph(beta_value) {
    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    date_list = [], ticker_1_list = [], ticker_2_list = []
    ticker_1_name = tr[0].querySelectorAll("th")[1].innerHTML
    ticker_2_name = tr[0].querySelectorAll("th")[2].innerHTML
    for (i=tr.length-1; i>0; i--) {
        var td = tr[i].querySelectorAll("td");
        date_list.push(td[0].innerHTML)
        ticker_1_list.push(Number(td[1].innerHTML))
        ticker_2_list.push(Number(td[2].innerHTML))
    }
    document.getElementsByClassName("instructions")[0].innerHTML += `
        <br>
        <div id="consecutive_text">The beta value of ${ticker_1_name} with respect to ${ticker_2_name} is ${beta_value}.</div>`

    var trace1 = {
        x: date_list,
        y: ticker_1_list,
        name: ticker_1_name,
        line: {'color': 'rgb(38, 166, 154)'},
        hovertemplate:
                `<b>${ticker_1_name}</b><br>` +
                "% Change: %{y}%<br>" +
                "<extra></extra>",
        type: 'scatter'
    };

    var trace2 = {
        x: date_list,
        y: ticker_2_list,
        name: ticker_2_name,
        line: {'color': 'orange'},
        hovertemplate:
                `<b>${ticker_2_name}</b><br>` +
                "% Change: %{y}%<br>" +
                "<extra></extra>",
        type: 'scatter'
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
            title: {
                text: 'Date',
            },
        },
        yaxis: {
            showgrid: false,
            showline: true,
            color: "gray",
            title: {
                text: '% Price Change',
            },
        },
        hovermode:'x',
        legend: {
            x: 1,
            xanchor: 'right',
            y: 1
        }
    };

    var data = [trace1, trace2];
    Plotly.newPlot('beta_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});
}

function swap_ticker_position() {
    var ticker_inputs = document.getElementsByClassName("ticker_input")
    var tmp = ticker_inputs[0].value
    ticker_inputs[0].value = ticker_inputs[1].value
    ticker_inputs[1].value = tmp
}