function change_header_description() {
    ticker_selected = document.querySelector(".ticker_input").value.toUpperCase()
    document.querySelector(".ticker_insider_header").innerHTML = `Recent Insider Trading of ${ticker_selected}`
}

function load_table() {
    tr = document.querySelector("table").querySelectorAll("tr")
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        td[0].innerHTML = `<a href="/ticker/?quote=${td[0].innerHTML}" target="_blank"><b>${td[0].innerHTML}</b></a>`
        td[2].innerHTML = "$" + Number(td[2].innerHTML).toLocaleString()
        td[3].innerHTML += "%"
        if (td[1].innerHTML.includes("-")) {
            td[1].innerHTML = Number(td[1].innerHTML).toLocaleString().replace("-", "-$")
            td[1].parentElement.style.backgroundColor = "#ff000054"
        }
        else {
            td[1].innerHTML = "$" + Number(td[1].innerHTML).toLocaleString()
            td[1].parentElement.style.backgroundColor = "#00800078"
        }
    }
}

function load_graph() {
    tr = document.querySelector("table").querySelectorAll("tr")
    symbol_list = [], value_list = [], customdata_list = [], color_list = [], parent_list = [], proportion_list = [], mkt_cap_list = []
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        value_list.push(td[1].innerHTML.replace("-", "") / 1000000)
        customdata_list.push(td[1].innerHTML / 1000000)
        parent_list.push("")
        symbol_list.push(td[0].innerHTML)
        if (td[1].innerHTML.includes("-")) {
            color_list.push("#c52222")
        }
        else {
            color_list.push("#26a671")
        }
        mkt_cap_list.push(td[2].innerHTML)
        proportion_list.push(td[3].innerHTML)
    }

    var data = [{
        type: 'treemap',
        values: value_list,
        labels: symbol_list,
        parents: parent_list,
        customdata: customdata_list,
        textinfo: "test",
        hovertemplate: "<b>%{label}</b><br>Net Purchase: %{customdata:.2f}M<br><extra></extra>",
        textposition: "center",
        texttemplate: "<b>%{label}</b><br>%{customdata:.2f}M",
        marker: {colors: color_list}
    }]

    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:0,
            r:0,
            b: 15,
            pad: 0
        },
        automargin: true,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
    }

    Plotly.newPlot('top_insider', data, layout, {displayModeBar: false, showTips: false, responsive: true})
    .then(gd => {
        gd.on("plotly_treemapclick", () => false)
    })

    mkt_cap_size = mkt_cap_list.map(bb_size)
    function bb_size(num) {
        num = num / 20000000000
        if (num < 10) {
            num = 10
        }
        return num
    }

    var trace1 = {
        x: proportion_list,
        y: mkt_cap_list,
        customdata: symbol_list,
        hovertemplate:
                `<b>$%{customdata}</b><br>` +
                "Mkt Cap: %{y}<br>" +
                "% of Mkt Cap: %{x}%<br>" +
                "<extra></extra>",
        textposition: 'auto',
        mode: 'markers',
        marker: {
            size: mkt_cap_size,
            color: color_list
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
                text: 'Log. % of Market Cap',
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
                text: 'Market Cap',
                font: {
                    size: 12,
                }
            },
        },
    }
    Plotly.newPlot('mkt_cap', data, layout, {displayModeBar: false, showTips: false, responsive: true})
}

function resize_plotly_graph() {
    Plotly.Plots.resize('top_insider')
    Plotly.Plots.resize('mkt_cap')
}