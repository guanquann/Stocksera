function color_table(is_checked, whether_drs) {
    var date_list = [], avg_inflation = [];
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");
    if (is_checked == "checked") {
        for (i=tr.length-1; i>0; i--) {
            var td = tr[i].querySelectorAll("td");
            for (k=1; k<td.length; k++) {
                const value = td[k].innerHTML
                if (value != "N/A") {
                    const l = 100 - (value * 11);
                    const textColor = l < 60 ? 'white' : '#000';
                    if (whether_drs == "DRS") {
                        td[k].style.backgroundColor = 'hsl(330, 70%, ' + l + '%)'
                    }
                    else {
                        td[k].style.backgroundColor = 'hsl(10, 70%, ' + l + '%)'
                    }
                    td[k].style.color = textColor
                }
            }
        }
    }
    else {
        for (i=tr.length-1; i>0; i--) {
            var td = tr[i].querySelectorAll("td");
            for (k=1; k<td.length; k++) {
                td[k].style.removeProperty("background-color");
                td[k].style.removeProperty("color");
            }
        }
    }
}

function show_reference(whether_drs) {
    var tds = document.getElementById("heatmap_reference").querySelector("tr").querySelectorAll("td")
    for (k=0; k<tds.length; k++) {
        const value = tds[k].innerHTML
        const l = 100 - (value * 11);
        const textColor = l < 60 ? 'white' : '#000';
        if (whether_drs == "normal") {
            tds[k].style.backgroundColor = 'hsl(10, 70%, ' + l + '%)'
        }
        else {
            tds[k].style.backgroundColor = 'hsl(330, 70%, ' + l + '%)'
        }
        tds[k].style.color = textColor
    }
}

function change_color_table(whether_drs) {
    checkbox = document.getElementsByClassName(whether_drs)[0]
    drs_your_shares = document.getElementsByClassName("drs_your_shares")[0]
    if (checkbox.checked == true) {
        color_table("checked", whether_drs)
    }
    else {
        color_table("unchecked", whether_drs)
    }
    if (whether_drs == "normal") {
        document.querySelector(".DRS").checked = false
        drs_your_shares.style.display = "none"
    }
    else {
        document.querySelector(".normal").checked = false
        drs_your_shares.style.removeProperty("display")
    }
    show_reference(whether_drs)
}

var inflation_chart = null

function inflation(duration) {
    var date_list = [], avg_inflation = [];
    var table = document.getElementsByTagName("table")[0];
    var tr = table.querySelectorAll("tr");

    if (duration == "one_year") {
        var month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        total_month = 12, current_month = 0
        most_recent_yr = tr[1].querySelectorAll("td")
        for (y=1; y<13; y++) {
            inflation_num = most_recent_yr[y].innerHTML
            if (inflation_num != "N/A") {
                avg_inflation.push(inflation_num)
                date_list.push(month_list[y-1] + " " + most_recent_yr[0].innerHTML)
                current_month += 1
            }
        }
        if (current_month != total_month) {
            prev_yr = tr[2].querySelectorAll("td")
            last_yr_date_list = [], last_yr_inflation = []
            num_months_remaining = total_month - current_month + 1
            for (n=prev_yr.length-num_months_remaining; n<13; n++) {
                inflation_num = prev_yr[n].innerHTML
                last_yr_inflation.push(inflation_num)
                last_yr_date_list.push(month_list[n-1] + " " + prev_yr[0].innerHTML)
            }
            date_list = last_yr_date_list.concat(date_list)
            avg_inflation = last_yr_inflation.concat(avg_inflation)
        }

    }
    else {
        for (i=tr.length-1; i>0; i--) {
            var td = tr[i].querySelectorAll("td");
            date_list.push(td[0].innerHTML)
            if (td[13].innerHTML != "N/A") {
                avg_inflation.push(td[13].innerHTML)
            }
        }
    }

    if (inflation_chart != null){
        inflation_chart.destroy();
    }
    inflation_chart = document.getElementById('inflation_chart');
    inflation_chart = new Chart(inflation_chart, {
        data: {
            labels: date_list,
            datasets: [
                {
                    label: 'Inflation',
                    type: 'line',
                    data: avg_inflation,
                    borderColor: 'rgb(38, 166, 154)',
                    backgroundColor: 'transparent',
                    lineTension: 0,
                    borderWidth: 2,
                }
                ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true,
            },
            elements: {
                point:{
                    radius: 0
                }
            },
            scales: {
                yAxes: [
                    {
                        display: true,
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey"
                        },
                        position: 'left',
                        type: "linear",
                        scaleLabel: {
                            display: true,
                            labelString: 'Inflation [%]',
                            beginAtZero: false,
                        }
                    }
                ],
                xAxes: [
                    {
                        offset: true,
                        ticks: {
                            maxTicksLimit: 10,
                            maxRotation: 30,
                            minRotation: 0,
                        },
                        gridLines: {
                            drawOnChartArea: false,
                            color: 'grey',
                        },
                    }
                ],
            },

            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItem, data) {
                        var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        var label = data.datasets[tooltipItem.datasetIndex].label;
                        return label + ': ' + value + '%';
                    }
                },
            },
            hover: {
                mode: 'index',
                intersect: false
            },
        },
    });
}

function btn_selected(elem) {
    date_range = document.getElementsByName("date_range")
    for (i=0; i<date_range.length; i++) {
        date_range[i].classList.remove("selected")
    }
    elem.classList.add("selected")
}