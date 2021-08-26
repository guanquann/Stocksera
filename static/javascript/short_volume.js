function display_data() {
    var error_msg_class = document.getElementById("error_msg").className;
    if (error_msg_class == "instructions error_true") {
        document.getElementById("error_msg").style.removeProperty("display");
        document.getElementById("short_vol_data").style.display = "none";
    }
}

function display_table() {
    var shorted_vol_daily = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    for (tr=shorted_vol_daily.length-1; tr>0; tr--) {
        var total_td = shorted_vol_daily[tr].querySelectorAll("td");
        total_td[2].innerHTML = Number(total_td[2].innerHTML).toLocaleString()
        total_td[3].innerHTML = Number(total_td[3].innerHTML).toLocaleString()
    }
}

var vol_chart = null
var price_chart = null

function short_vol_graph(duration) {
    var date_threshold = get_date_difference(duration, "-")

    var shorted_vol_daily = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    var date_list = [], price_list = [], short_vol_list = [], long_vol_list = [], percentage_list = []
    for (tr=shorted_vol_daily.length-1; tr>0; tr--) {
        var total_td = shorted_vol_daily[tr].querySelectorAll("td");
        date_string = total_td[0].innerHTML;
        if (date_string >= date_threshold) {
            date_list.push(date_string);
            price_list.push(total_td[1].innerHTML.replace("$", ""));
            short_vol_num = Number(total_td[2].innerHTML.replace(/[^0-9-.]/g, ""))
            long_vol_num = Number(total_td[3].innerHTML.replace(/[^0-9-.]/g, ""))
            short_vol_list.push(short_vol_num);
            long_vol_list.push(long_vol_num - short_vol_num);
            percentage_list.push(total_td[4].innerHTML.replace("%", ""));
            shorted_vol_daily[tr].style.removeProperty("display");
        }
        else {
            shorted_vol_daily[tr].style.display = "none"
        }
    }

    if (vol_chart != null){
        vol_chart.destroy();
        price_chart.destroy();
    }

    vol_chart = document.getElementById('vol_chart');
    vol_chart = new Chart(vol_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Short Percentage',
                    type: 'line',
                    data: percentage_list,
                    borderColor: 'wheat',
                    backgroundColor: 'transparent',
                    yAxisID: 'B',
                },
                {
                    label: 'Short Volume',
                    type: 'bar',
                    data: short_vol_list,
                    backgroundColor: 'red',
                    barThickness: 'flex',
                    yAxisID: 'A',
                },
                {
                    label: 'Long Volume',
                    type: 'bar',
                    data: long_vol_list,
                    backgroundColor: 'rgb(38, 166, 154)',
                    barThickness: 'flex',
                    yAxisID: 'A',
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true
             },
            scales: {
                yAxes: [{
                        position: 'left',
                        gridLines: {
                            display: false
                        },
                        type: "linear",
                        id: "A",
                        stacked: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Volume',
                            beginAtZero: true,
                        },
                    },
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Short Percentage',
                            beginAtZero: true,
                        },
                        type: "linear",
                        id: "B",
                        position:"right",
                        gridLines: {
                            display: false
                        },
                        ticks: {
                            max: 100,
                            min: 0,
                            callback: function(value, index, values) {
                                return value + "%";
                            }
                        },
                    }],

                xAxes: [{
                    offset: true,
                    ticks: {
                      maxTicksLimit: 10,
                      maxRotation: 45,
                      minRotation: 0,
                    },
                    gridLines: {
                        drawOnChartArea: false
                    },
                    stacked: true
                }],
            },

            // To show value when hover on any part of the graph
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'index',
                intersect: false
            },
            elements: {
                line: {
                    tension: 0
                },
                point:{
                    radius: 0
                }
            },
        },
    });

    price_chart = document.getElementById('price_chart');
    price_chart = new Chart(price_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Close Price',
                    type: 'line',
                    data: price_list,
                    borderColor: 'yellow',
                    backgroundColor: 'transparent',
                    yAxisID: 'A',
                },
                {
                    label: 'Short Percentage',
                    type: 'line',
                    data: percentage_list,
                    borderColor: 'wheat',
                    backgroundColor: 'transparent',
                    yAxisID: 'B',
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true
             },
            scales: {
                yAxes: [
                    {
                        position: 'left',
                        gridLines: {
                            display: false
                        },
                        type: "linear",
                        id: "A",
                        scaleLabel: {
                            display: true,
                            labelString: 'Close Price',
                            beginAtZero: false,
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return "$" + value;
                            },
                        }
                    },
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Short Percentage',
                            beginAtZero: true,
                        },
                        type: "linear",
                        id: "B",
                        position:"right",
                        gridLines: {
                            display: false
                        },
                        ticks: {
                            max: 100,
                            min: 0,
                            callback: function(value, index, values) {
                                return value + "%";
                            }
                        },
                    }],

                xAxes: [{
                    ticks: {
                      maxTicksLimit: 10,
                      maxRotation: 45,
                      minRotation: 0,
                    },
                    gridLines: {
                        drawOnChartArea: false
                    },
                    stacked: true
                }],
            },

            // To show value when hover on any part of the graph
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'index',
                intersect: false
            },
            elements: {
                line: {
                    tension: 0
                },
                point:{
                    radius: 0
                }
            },
        },
    });

    var short_vol = Number(short_vol_list[short_vol_list.length-1]);
    var short_vol_prev = Number(short_vol_list[short_vol_list.length-2]);
    var long_vol = Number(long_vol_list[long_vol_list.length-1]);
    var total_vol = short_vol + long_vol;
    var percentage_change = Math.round(((short_vol - short_vol_prev) / short_vol_prev) * 100)
    if (percentage_change >=0) {
        percentage_change = "+" + String(percentage_change)
    }

    var summary_code = `<p>The short volume for $${document.getElementById("quote").value} is ${percentage_list[percentage_list.length-1]}% on ${date_list[date_list.length-1]}. The short sale volume is ${short_vol}, long sale volume is ${long_vol}. The total volume is ${total_vol}. The short sale volume is ${percentage_change}% compared to ${date_list[date_list.length-2]}.</p>`

    document.getElementById("summary").innerHTML = summary_code
}

function btn_selected(elem) {
    date_range = document.getElementsByName("date_range")
    for (i=0; i<date_range.length; i++) {
        date_range[i].classList.remove("selected")
    }
    elem.classList.add("selected")
}
