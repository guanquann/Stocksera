function inflation(scope) {
    country_list = []
    inflation_list = []
    var trs = document.querySelector("table").querySelectorAll("tr")
    for (i=1; i<trs.length; i++) {
        tr = trs[i].querySelectorAll("td")
        country_list.push(tr[0].innerHTML)
        inflation_list.push(tr[1].innerHTML)
        if (scope != tr[4].innerHTML.toLowerCase() && scope != "world") {
            trs[i].style.display = "none"
        }
        else {
            trs[i].style.removeProperty("display")
        }
    }
    var data = [{
        type: 'choropleth',
        locationmode: 'country names',
        locations: country_list,
        z: inflation_list,
        zmin: 0,
        zmax: 20,
        showscale: false,
        autocolorscale: true
    }];

    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:0,
            r:0,
            b: 0,
            pad: 0
        },
        height: window.innerWidth < 600 ? 250 : 400,
        automargin: true,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        geo: {
            resolution: 50,
            scope: scope,
            bgcolor: "#EAE9E9",
        },
    }

    Plotly.newPlot('inflation_chart', data, layout, {displayModeBar: false, showTips: false, responsive: true})
}

function btn_selected(elem) {
    date_range = document.getElementsByName("date_range")
    for (i=0; i<date_range.length; i++) {
        date_range[i].classList.remove("selected")
    }
    elem.classList.add("selected")
}

function resize_plotly_graph() {
    Plotly.Plots.resize('inflation_chart')
}