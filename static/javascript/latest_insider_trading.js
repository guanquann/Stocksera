function change_header_description() {
    ticker_selected = document.querySelector(".ticker_input").value.toUpperCase()
    document.querySelector(".ticker_insider_header").innerHTML = `Recent Insider Trading of ${ticker_selected}`
}

function load_table() {
    tr = document.querySelector("table").querySelectorAll("tr")
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        td[0].innerHTML = `<a href="/ticker/?quote=${td[0].innerHTML}" target="_blank"><b><u>${td[0].innerHTML}</u></b></a>`
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
    symbol_list = [], value_list = [], customdata_list = [], color_list = [], parent_list = []
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
    }

    var data = [{
      type: 'treemap',
      values: value_list,
      labels: symbol_list,
      parents: parent_list,
      customdata: customdata_list,
      textinfo: "test",
      hovertemplate: "<b>%{label}</b><br>Net Purchase: %{customdata:.2f}M<br><extra></extra>",
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

    Plotly.newPlot('top_insider', data, layout, {displayModeBar: false, showTips: true, responsive: true})
}