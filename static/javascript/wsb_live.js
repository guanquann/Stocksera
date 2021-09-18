function load_graph(trending_list) {

    date_1_list = [], ticker_1_list = []
    for (ticker in trending_list[0]) {
        mentions = trending_list[0][ticker]
        date_1_list.push(mentions[1])
        ticker_1_list.push(mentions[2])
    }

    var trace1 = {
        x: date_1_list,
        y: ticker_1_list,
        name: trending_list[0][0][0],
        line: {'color': 'rgb(38, 166, 154)'},
        hovertemplate:
                `<b>${trending_list[0][0][0]}</b><br>` +
                "Mentions: %{y}<br>" +
                "Time: %{x|%H:%M}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines',
    };

    date_2_list = [], ticker_2_list = []
    for (ticker in trending_list[1]) {
        mentions = trending_list[1][ticker]
        date_2_list.push(mentions[1])
        ticker_2_list.push(mentions[2])
    }

    var trace2 = {
        x: date_2_list,
        y: ticker_2_list,
        name: trending_list[1][0][0],
        line: {'color': 'blue'},
        hovertemplate:
                `<b>${trending_list[1][0][0]}</b><br>` +
                "Mentions: %{y}<br>" +
                "Time: %{x|%H:%M}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines'
    };

    date_3_list = [], ticker_3_list = []
    for (ticker in trending_list[2]) {
        mentions = trending_list[2][ticker]
        date_3_list.push(mentions[1])
        ticker_3_list.push(mentions[2])
    }

    var trace3 = {
        x: date_3_list,
        y: ticker_3_list,
        name: trending_list[2][0][0],
        line: {'color': 'purple'},
        hovertemplate:
                `<b>${trending_list[2][0][0]}</b><br>` +
                "Mentions: %{y}<br>" +
                "Time: %{x|%H:%M}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines'
    };

    date_4_list = [], ticker_4_list = []
    for (ticker in trending_list[3]) {
        mentions = trending_list[3][ticker]
        date_4_list.push(mentions[1])
        ticker_4_list.push(mentions[2])
    }

    var trace4 = {
        x: date_4_list,
        y: ticker_4_list,
        name: trending_list[3][0][0],
        line: {'color': 'grey'},
        hovertemplate:
                `<b>${trending_list[3][0][0]}</b><br>` +
                "Mentions: %{y}<br>" +
                "Time: %{x|%H:%M}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines'
    };

    date_5_list = [], ticker_5_list = []
    for (ticker in trending_list[4]) {
        mentions = trending_list[4][ticker]
        date_5_list.push(mentions[1])
        ticker_5_list.push(mentions[2])
    }

    var trace5 = {
        x: date_5_list,
        y: ticker_5_list,
        name: trending_list[4][0][0],
        line: {'color': 'yellow'},
        hovertemplate:
                `<b>${trending_list[4][0][0]}</b><br>` +
                "Mentions: %{y}<br>" +
                "Time: %{x|%H:%M}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines'
    };

    date_6_list = [], ticker_6_list = []
    for (ticker in trending_list[5]) {
        mentions = trending_list[5][ticker]
        date_6_list.push(mentions[1])
        ticker_6_list.push(mentions[2])
    }

    var trace6 = {
        x: date_6_list,
        y: ticker_6_list,
        name: trending_list[5][0][0],
        line: {'color': 'brown'},
        hovertemplate:
                `<b>${trending_list[5][0][0]}</b><br>` +
                "Mentions: %{y}<br>" +
                "Time: %{x|%H:%M}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines'
    };

    date_7_list = [], ticker_7_list = []
    for (ticker in trending_list[6]) {
        mentions = trending_list[6][ticker]
        date_7_list.push(mentions[1])
        ticker_7_list.push(mentions[2])
    }

    var trace7 = {
        x: date_7_list,
        y: ticker_7_list,
        name: trending_list[6][0][0],
        line: {'color': 'orange'},
        hovertemplate:
                `<b>${trending_list[6][0][0]}</b><br>` +
                "Mentions: %{y}<br>" +
                "Time: %{x|%H:%M}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines'
    };

    date_8_list = [], ticker_8_list = []
    for (ticker in trending_list[7]) {
        mentions = trending_list[7][ticker]
        date_8_list.push(mentions[1])
        ticker_8_list.push(mentions[2])
    }

    var trace8 = {
        x: date_8_list,
        y: ticker_8_list,
        name: trending_list[7][0][0],
        line: {'color': '#9c6679'},
        hovertemplate:
                `<b>${trending_list[7][0][0]}</b><br>` +
                "Mentions: %{y}<br>" +
                "Time: %{x|%H:%M}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines'
    };

    date_9_list = [], ticker_9_list = []
    for (ticker in trending_list[8]) {
        mentions = trending_list[8][ticker]
        date_9_list.push(mentions[1])
        ticker_9_list.push(mentions[2])
    }

    var trace9 = {
        x: date_9_list,
        y: ticker_9_list,
        name: trending_list[8][0][0],
        line: {'color': 'wheat'},
        hovertemplate:
                `<b>${trending_list[8][0][0]}</b><br>` +
                "Mentions: %{y}<br>" +
                "Time: %{x|%H:%M}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines'
    };

    date_10_list = [], ticker_10_list = []
    for (ticker in trending_list[9]) {
        mentions = trending_list[9][ticker]
        date_10_list.push(mentions[1])
        ticker_10_list.push(mentions[2])
    }

    var trace10 = {
        x: date_10_list,
        y: ticker_10_list,
        name: trending_list[9][0][0],
        line: {'color': 'red'},
        hovertemplate:
                `<b>${trending_list[9][0][0]}</b><br>` +
                "Mentions: %{y}<br>" +
                "Time: %{x|%H:%M}<br>" +
                "<extra></extra>",
        type: 'line',
        mode: 'lines'
    };


    var layout = {
        autosize: true,
        margin: {
            t:0,
            l:50,
            r:00,
            pad: 0
        },
        automargin: true,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        xaxis: {
            tick0: '2000-01-01',
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
                text: 'No. of Mentions',
            },
        },
        hovermode:'closest',
    };

    var data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8, trace9, trace10];
    Plotly.newPlot('chart', data, layout, {displayModeBar: false, showTips: false, responsive: true});
}