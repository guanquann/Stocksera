function display_input() {
    var error_msg_class = document.getElementById("error_msg").className;
    if (error_msg_class == "instructions error_false") {
        document.getElementById("date_dropdown").style.removeProperty("display");
        document.getElementById("graph_section").style.removeProperty("display");
        document.getElementById("list_format").style.removeProperty("display");
        document.getElementById("options_choice").style.removeProperty("display");
        document.getElementsByClassName("ticker_stats")[0].style.removeProperty("display");
    }
    else if (error_msg_class == "instructions error_true") {
        document.getElementById("error_msg").style.removeProperty("display");
    }
}

function update_table() {
    var tables = document.getElementsByClassName("dataframe");

    var calls_tr = tables[0].getElementsByTagName("tr");
    for (i = 1; i < calls_tr.length; i++) {
        if (calls_tr[i].children[11].innerHTML == "True") {
            calls_tr[i].style.backgroundColor = "#26a69a";
            calls_tr[i].style.fontWeight = "bold";
            calls_tr[i].style.opacity = "0.65";
        }
        calls_tr[i].children[7].innerHTML = calls_tr[i].children[7].innerHTML + "%"
        calls_tr[i].children[10].innerHTML = calls_tr[i].children[10].innerHTML + "%"
        calls_tr[i].children[11].style.display = "none";
    }

    var puts_tr = tables[1].getElementsByTagName("tr");
    for (i = 1; i < puts_tr.length; i++) {
        if (puts_tr[i].children[11].innerHTML == "True") {
            puts_tr[i].style.backgroundColor = "red";
            puts_tr[i].style.fontWeight = "bold";
            puts_tr[i].style.opacity = "0.65";
        }

        puts_tr[i].children[7].innerHTML = puts_tr[i].children[7].innerHTML + "%"
        puts_tr[i].children[10].innerHTML = puts_tr[i].children[10].innerHTML + "%"
        puts_tr[i].children[11].style.display = "none";
    }

    calls_tr[0].children[11].style.display = "none";
    puts_tr[0].children[11].style.display = "none";

    var straddle = tables[2].getElementsByTagName("tr");
    var straddle_th = straddle[0].querySelectorAll("th");
    for (i=0; i<=4; i++) {
        straddle_th[i].style.backgroundColor = "#26a69a"
    }
    for (i=6; i<=10; i++) {
        straddle_th[i].style.backgroundColor = "red"
    }

    for (i=0; i<straddle.length; i++) {
        straddle[i].children[5].style.backgroundColor = "#9b9999"
    }
}

function show_choice(elem) {
    var choices = document.getElementsByClassName("choices");
    var list_format = document.getElementById("list_format");
    var straddle_format = document.getElementById("straddle_format");
    if (elem == "list") {
        choices[0].className = "choices choice_selected";
        choices[1].className = "choices";
        list_format.style.display = "";
        straddle_format.style.display = "none";
    }
    else {
        choices[0].className = "choices";
        choices[1].className = "choices choice_selected";
        list_format.style.display = "none";
        straddle_format.style.display = "";
    }
}

function draw_open_interest() {
    var tr = document.getElementsByTagName("table")[2].querySelectorAll("tr");

    var tr_length = Math.round(tr.length / 2);
    var diff = Math.round(document.getElementsByTagName("table")[2].querySelectorAll("tr").length * 0.4);
    var lower_limit = tr_length - diff;
    var upper_limit = tr_length + diff;

    var calls_oi_list = [];
    var puts_oi_list = [];
    var strike_list = [];

    for (row=lower_limit; row<upper_limit; row++) {
        var td = tr[row].querySelectorAll("td");
        calls_oi_list.push(td[4].innerHTML);
        puts_oi_list.push(td[10].innerHTML);
        strike_list.push(td[5].innerHTML);
    }

    var oi_chart = document.getElementById('oi_chart');
    var display_chart = new Chart(oi_chart, {
        type: 'line',
        data: {
            labels: strike_list,
            datasets: [{
                label: 'Calls',
                lineTension: 0,  // straight line instead of curve
                data: calls_oi_list,
                borderColor: "green",
                backgroundColor: 'transparent',
                tension: 0.1,
            },
            {
                label: 'Puts',
                lineTension: 0,  // straight line instead of curve
                data: puts_oi_list,
                borderColor: "red",
                backgroundColor: 'transparent',
                tension: 0.1,
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }, 
                    gridLines: {
                        drawOnChartArea: false
                    },
                    
                }],

                xAxes: [{
                    ticks: {
                        maxTicksLimit: 20,
                        maxRotation: 45,
                        minRotation: 0,
                        callback: function(value, index, values) {
                            return "$" + value;
                        }
                    },
                    gridLines: {
                        drawOnChartArea: false
                    },  
                }]
            },
            // To remove the point of each label
            elements: {
                point: {
                    radius: 0
                }
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
        },
    });

    
}