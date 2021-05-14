function compare_chart() {
    var list_of_industries = []
    var perf_list = []
    var perf_day = [], perf_wk = [], perf_month = [], perf_quart = [], perf_half = [], perf_year = [], perf_ytd = []
    var tr = document.getElementsByTagName("tr")
    for (row=1; row<tr.length; row++) {
        var td = tr[row].querySelectorAll("td");
        for (i=1; i<td.length; i++) {
            if (! td[i].innerHTML.includes("%")) {
                td[i].innerHTML = Math.round(td[i].innerHTML*10000)/100 + "%"
            }

            if (td[i].innerHTML.includes("-")) {
                td[i].style.color = "red";
            }
            else {
                td[i].innerHTML = "+" + td[i].innerHTML
                td[i].style.color = "rgb(38, 166, 154)"
            }
        }
        list_of_industries.push(td[0].innerHTML);
        perf_day.push(Number(td[1].innerHTML.replace("%", "")));
        perf_wk.push(Number(td[2].innerHTML.replace("%", "")));
        perf_month.push(Number(td[3].innerHTML.replace("%", "")));
        perf_quart.push(Number(td[4].innerHTML.replace("%", "")));
        perf_half.push(Number(td[5].innerHTML.replace("%", "")));
        perf_year.push(Number(td[6].innerHTML.replace("%", "")));
        perf_ytd.push(Number(td[7].innerHTML.replace("%", "")));
    }

    var options_dict = {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
            display: false
        },
        scales: {
            yAxes: [{
                gridLines: {
                    drawOnChartArea: false
                }
            }],

            xAxes: [{
                ticks: {
//                  maxTicksLimit: 10,
//                  maxRotation: 45,
//                  minRotation: 0,
                  beginAtZero: true,
                },
                gridLines: {
                    drawOnChartArea: false
                }
            }]
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
    }

    var day_chart = document.getElementById('day_chart');
    var day_chart = new Chart(day_chart, {
        type: 'bar',
        data: {
            labels: list_of_industries,
            datasets: [{
                label: 'Performance (Day)',
                data: perf_day,
                backgroundColor: 'rgba(255, 159, 64, 0.5)',
                borderColor: 'rgb(255, 159, 64)',
                borderWidth: '2',
            }]
        },
        options: options_dict,
    });

    var wk_chart = document.getElementById('wk_chart');
    var wk_chart = new Chart(wk_chart, {
        type: 'bar',
        data: {
            labels: list_of_industries,
            datasets: [{
                label: 'Performance (Week)',
                data: perf_wk,
                backgroundColor: 'rgba(255, 159, 64, 0.5)',
                borderColor: 'rgb(255, 159, 64)',
                borderWidth: '2',
            }]
        },
        options: options_dict,
    });

    var month_chart = document.getElementById('month_chart');
    var month_chart = new Chart(month_chart, {
        type: 'bar',
        data: {
            labels: list_of_industries,
            datasets: [{
                label: 'Performance (Month)',
                data: perf_month,
                backgroundColor: 'rgba(255, 159, 64, 0.5)',
                borderColor: 'rgb(255, 159, 64)',
                borderWidth: '2',
            }]
        },
        options: options_dict,
    });

    var quart_chart = document.getElementById('quart_chart');
    var quart_chart = new Chart(quart_chart, {
        type: 'bar',
        data: {
            labels: list_of_industries,
            datasets: [{
                label: 'Performance (Quarter)',
                data: perf_quart,
                backgroundColor: 'rgba(255, 159, 64, 0.5)',
                borderColor: 'rgb(255, 159, 64)',
                borderWidth: '2',
            }]
        },
        options: options_dict,
    });

    var half_chart = document.getElementById('half_chart');
    var half_chart = new Chart(half_chart, {
        type: 'bar',
        data: {
            labels: list_of_industries,
            datasets: [{
                label: 'Performance (Half Year)',
                data: perf_half,
                backgroundColor: 'rgba(255, 159, 64, 0.5)',
                borderColor: 'rgb(255, 159, 64)',
                borderWidth: '2',
            }]
        },
        options: options_dict,
    });

    var year_chart = document.getElementById('year_chart');
    var year_chart = new Chart(year_chart, {
        type: 'bar',
        data: {
            labels: list_of_industries,
            datasets: [{
                label: 'Performance (Year)',
                data: perf_year,
                backgroundColor: 'rgba(255, 159, 64, 0.5)',
                borderColor: 'rgb(255, 159, 64)',
                borderWidth: '2',
            }]
        },
        options: options_dict,
    });

    var ytd_chart = document.getElementById('ytd_chart');
    var ytd_chart = new Chart(ytd_chart, {
        type: 'bar',
        data: {
            labels: list_of_industries,
            datasets: [{
                label: 'Performance (YTD)',
                data: perf_ytd,
                backgroundColor: 'rgba(255, 159, 64, 0.5)',
                borderColor: 'rgb(255, 159, 64)',
                borderWidth: '2',
            }]
        },
        options: options_dict,
    });
}