colorscale_list =
    [
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
    ]

layout_dict = {
        autosize: true,
        margin: {
            t:0,
            l:5,
            r:5,
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

function load_stock_chart(title) {
    parent_list = [""], mkt_cap_list = [""], change_list = [""], ticker_list = [title]

    tr = document.getElementsByTagName("table")[1].querySelectorAll("tr")
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        parent_list.push(title)
        ticker_list.push(td[0].innerHTML.replace(/&amp;/g, '&'))
        mkt_cap_list.push(0)
        change_list.push(td[3].innerHTML)
    }

    tr = document.getElementsByTagName("table")[2].querySelectorAll("tr")
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        parent_list.push(td[0].innerHTML.replace(/&amp;/g, '&'))
        ticker_list.push(td[1].innerHTML.replace(/&amp;/g, '&'))
        mkt_cap_list.push(0)
        change_list.push(td[4].innerHTML)
    }

    tr = document.getElementsByTagName("table")[0].querySelectorAll("tr")
    exclude_list = []
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        if (! exclude_list.includes(td[4].innerHTML.replace(/&amp;/g, '&'))) {
            ticker_list.push(td[0].innerHTML)
            change_list.push(td[2].innerHTML)
            mkt_cap_list.push(td[1].innerHTML)
            parent_list.push(td[4].innerHTML.replace(/&amp;/g, '&'))
        }
    }

    var data = [{
        type: 'treemap',
        values: mkt_cap_list,
        labels: ticker_list,
        parents: parent_list,
        customdata: change_list,
        showscale: false,
        marker: {
            cmin: -3,
            cmax: 3,
            cmid: 0,
            colorscale: colorscale_list,
            colors: change_list,
        },
        hovertemplate: "<b>%{label}</b><br>Price Change: %{customdata}%<br><extra></extra>",
        textposition: "center",
        texttemplate: "<b>%{label}</b><br>%{customdata}%",
    }]

    var layout = layout_dict
    Plotly.newPlot('heatmap_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true})
}

function load_crypto_chart() {
    var url = `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false`;
    fetch(url)
    .then(res => res.json())
    .then((out) => {
        symbol_list = [], parent_list = [], market_cap_list = [], color_list = [], custom_data_list = []
        for (i in out) {
            i = out[i]
            symbol = i["symbol"].toUpperCase()
            market_cap = i["market_cap"] / 1000000000
            current_price = i["current_price"]
            price_change_percentage_24h = i["price_change_percentage_24h"]
            parent_list.push("Top 100 Crypto by Market Cap")
            symbol_list.push(symbol)
            market_cap_list.push(market_cap)
            color_list.push(price_change_percentage_24h)
            custom_data_list.push([current_price, price_change_percentage_24h, Number(market_cap).toLocaleString()])
        }

        var data = [{
            type: 'treemap',
            values: market_cap_list,
            labels: symbol_list,
            parents: parent_list,
            customdata: custom_data_list,
            hovertemplate: "<b>%{label}</b><br>Price: $%{customdata[0]}<br>Price Change: %{customdata[1]:.2f}%<br>Market Cap: %{customdata[2]}B<extra></extra>",
            textposition: "center",
            texttemplate: "<b>%{label}</b><br>%{customdata[1]:.2f}%",
            showscale: false,
            marker: {
                cmin: -5,
                cmax: 5,
                cmid: 0,
                colorscale: colorscale_list,
                colors: color_list,
            },
        }]

        var layout = layout_dict

        Plotly.newPlot('heatmap_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true})
        .then(gd => {
            gd.on("plotly_treemapclick", () => false)
        })
    })
    .catch(err => { throw err });
}

function load_heatmap(title) {
    if (title.includes("Crypto")) {
        load_crypto_chart()
    }
    else {
        load_stock_chart(title)
    }
}

function show_ticker_chart(elem) {
    if (elem.classList.contains("close_chart")) {
        document.getElementById("ticker_chart_div").style.display = "none"
        elem.classList.remove("close_chart")
        elem.innerHTML = elem.innerHTML.replace("Hide", "View")
    }
    else {
        document.getElementById("ticker_chart_div").style.removeProperty("display")
        elem.classList.add("close_chart")
        elem.innerHTML = elem.innerHTML.replace("View", "Hide")
    }
}

function resize_plotly_graph() {
    Plotly.Plots.resize('heatmap_chart')
}