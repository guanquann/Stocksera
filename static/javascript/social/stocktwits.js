function trending_ticker_graph(symbol) {
    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    var date_list = [], rank_list = [], watchlist_list = [];
    for (i=1; i<tr.length; i++) {
        var td = tr[i].querySelectorAll("td")
        rank_list.push(td[0].innerHTML)
        watchlist_list.push(td[1].innerHTML)
        date_list.push(td[2].innerHTML)
    }

    var trending_ticker_chart = document.getElementById('trending_ticker_chart');
    var trending_ticker_chart = new Chart(trending_ticker_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: symbol,
                    type: 'bar',
                    data: rank_list,
                    backgroundColor: 'rgb(38, 166, 154)',
                    borderColor: 'rgb(38, 166, 154)',
                    borderWidth: 2,
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Rank',
                        },
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        ticks: {
                            beginAtZero: true
                        }
                    }],

                xAxes: [{
                    offset: true,
                    ticks: {
                       userCallback: function(label, index, labels) {
                         return moment(label, "YYYYMMDD").format("DD MMM YY");
                       },
                       maxTicksLimit: 12,
                                    maxRotation: 30,
                                    minRotation: 0,
                     },
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                }],
            },

            // To show value when hover on any part of the graph
            tooltips: {
                mode: 'index',
                intersect: false,
            },

            // To remove the point of each label
            elements: {
                point: {
                    radius: 0
                }
            },

            hover: {
                mode: 'index',
                intersect: false
            },
        },
    });

    var watchlist_ticker_chart = document.getElementById('watchlist_ticker_chart');
    var watchlist_ticker_chart = new Chart(watchlist_ticker_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: symbol,
                    type: 'bar',
                    data: watchlist_list,
                    backgroundColor: 'lightblue',
                    borderColor: 'lightblue',
                    borderWidth: 2,
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Watchlist Count',
                        },
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        ticks: {
                            beginAtZero: false
                        }
                    }],

                xAxes: [{
                    offset: true,
                    ticks: {
                       userCallback: function(label, index, labels) {
                         return moment(label, "YYYYMMDD").format("DD MMM YY");
                       },
                       maxTicksLimit: 12,
                                    maxRotation: 30,
                                    minRotation: 0,
                     },
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                }],
            },

            // To show value when hover on any part of the graph
            tooltips: {
                mode: 'index',
                intersect: false,
            },

            // To remove the point of each label
            elements: {
                point: {
                    radius: 0
                }
            },

            hover: {
                mode: 'index',
                intersect: false
            },
        },
    });
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