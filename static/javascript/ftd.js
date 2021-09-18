Date.prototype.addDays = function(days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

Date.prototype.removeDays = function(days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() - days);
    return date;
}

function display_top_ftd_table() {
    var tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    for (i=1; i<tr.length; i++) {
        var td = tr[i].querySelectorAll("td");
        var date_string = td[0].innerHTML
        if (date_string != "") {
            if (td[2].innerHTML >= 500000) {
                tr[i].style.color = "red"
                tr[i].style.fontWeight = "bold"
            }

            td[1].innerHTML = `<a href="/ticker/failure_to_deliver/?quote=${td[1].innerHTML}" target="_blank" class="ftd_ticker_link">${td[1].innerHTML}</a>`
            td[2].innerHTML = Number(td[2].innerHTML).toLocaleString()
            td[3].innerHTML = "$" + td[3].innerHTML
            td[4].innerHTML = "$" + Number(td[4].innerHTML).toLocaleString()
        }
        else {
            td[0].style.padding = "15px"
        }
    }
}

function display_table() {
    var ftd = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    var threshold = document.getElementById("90th_percentile").innerHTML
//    ftd[0].innerHTML += `
//        <th>T+35 Date</th>`
    for (tr=ftd.length-1; tr>0; tr--) {
        var total_td = ftd[tr].querySelectorAll("td");
        date_string = total_td[0].innerHTML;
        total_td[0].innerHTML = date_string;

        if ((Number(total_td[1].innerHTML) > 1000000 | Number(total_td[3].innerHTML) > threshold) & Number(total_td[1].innerHTML) > 100000) {
            total_td[1].parentElement.style.color = "red";
            total_td[1].parentElement.style.fontWeight = "bold";
        }
        total_td[1].innerHTML = Number(total_td[1].innerHTML).toLocaleString()

        total_td[2].innerHTML = "$" + total_td[2].innerHTML
        total_td[3].innerHTML = "$" + Number(total_td[3].innerHTML).toLocaleString()

//        f35_date = new Date(date_string).addDays(36)
//        date_string = date_string.replaceAll("/", ",")
//        console.log(date_string)
//        f35_date = new Date(date_string).addDays(36).toUTCString()
//        console.log(f35_date)
//        month = f35_date.getMonth() + 1;
//        day = f35_date.getUTCDate();
//        year = f35_date.getUTCFullYear();
//        if (day < 10) {
//            day = "0" + day
//        }
//        if (month < 10) {
//            month = "0" + month
//        }
//        f35_date = year + "/" + month + "/" + day;
//        ftd[tr].innerHTML += `<td>${f35_date}</td>`
    }
}

var ftd_chart = null

function ftd_graph(duration) {
    var date_threshold = get_date_difference(duration, "/")

    var ftd = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    var date_list = [], price_list = [], vol_list = []
    for (tr=ftd.length-1; tr>0; tr--) {
        var total_td = ftd[tr].querySelectorAll("td");
        date_string = total_td[0].innerHTML;
        if (date_string >= date_threshold) {
            ftd[tr].style.removeProperty("display");
            date_list.push(date_string);
            vol_list.push(Number(total_td[1].innerHTML.replace(/[^0-9-.]/g, "")))
            price_list.push(Number(total_td[2].innerHTML.replace("$", "")));
        }
        else {
            ftd[tr].style.display = "none"
        }
    }

    if (ftd_chart != null){
        ftd_chart.destroy();
    }
    ftd_chart = document.getElementById('ftd_chart');
    ftd_chart = new Chart(ftd_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'FTD',
                    type: 'line',
                    data: vol_list,
                    borderColor: 'orange',
                    backgroundColor: 'transparent',
                    yAxisID: 'B',
                },
                {
                    label: 'Price',
                    type: 'line',
                    data: price_list,
                    backgroundColor: 'transparent',
                    borderColor: 'rgb(38, 166, 154)',
                    yAxisID: 'A',
                }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                        position: 'left',
                        gridLines: {
                            display: false
                        },
                        type: "linear",
                        id: "A",
                        scaleLabel: {
                            display: true,
                            labelString: 'Price',
                        },
                        ticks: {
                            callback: function(value, index, values) {
                                return "$" + value;
                            }
                        },
                    },
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'FTD',
                        },
                        type: "linear",
                        id: "B",
                        position:"right",
                        gridLines: {
                            display: false
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

            // To remove the point of each label
            elements: {
                line: {
                    tension: 0
                },
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
