var holdings_clicks= 0;
var trades_clicks = 0;
var news_clicks = 0;

var profile_clicks = 0;

const searchFun = () =>{
    let filter = document.getElementById('ticker_name').value.toUpperCase();
    let filter_table = document.getElementsByTagName('table')[0];

    let btn_selected = document.getElementsByClassName("button_parent")[0].querySelector(".selected").innerHTML;

    let tr = filter_table.getElementsByTagName('tr');

    for (var i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName('td')[2];

        if (td) {
            let textValue = td.textContent || td.innerHTML;
            if (textValue.indexOf(filter) > -1){
                tr[i].style.display="";
            }
            else {
                tr[i].style.display="none";
            }
        }
    }
}

function update_fund(elem) {
    document.getElementById("fund_selected").value = elem.innerHTML;
    holdings_clicks = 0, trades_clicks = 0, news_clicks = 0;
    load_holdings(0)
    load_profile()
    var fund_type = document.getElementsByClassName("fund_type");
    for (i=0; i<fund_type.length; i++) {
        fund_type[i].classList.remove("selected");
    }
    elem.classList.add("selected");
}

function load_profile() {
    var fund_selected = document.getElementById("fund_selected").value;
    var loading_profile = false;
    var profile_url = `https://arkfunds.io/api/v2/etf/profile?symbol=${fund_selected}`;
    if (loading_profile == false) {
        loading_profile = true;
        fetch(profile_url)
        .then(res => res.json())
        .then((out) => {
            profile = out["profile"];
            description = profile["description"];
            profile_code = `
                <a href="${profile["website"]}" target="_blank"><span>${profile["name"]} (${profile["symbol"]})</span></a>
                <p>${description}</p>`
            document.getElementById("profile").innerHTML = profile_code
        })
        .catch(err => { throw err });
        loading_profile = false;
    }
}

function load_holdings(elem) {
    var btn_type = document.getElementsByClassName("btn_type");
    for (i=0; i<btn_type.length; i++) {
        btn_type[i].classList.remove("selected");
    }
    btn_type[elem].classList.add("selected");
    document.getElementsByClassName("search_bar")[0].style.removeProperty("display");
    if (holdings_clicks == 0) {
        holdings_clicks = 1, trades_clicks = 0, news_clicks = 0;
        var ticker_list = [], weight_list = [], top_10_weight = 0, top_20_weight = 0
        var holdings_url = `https://arkfunds.io/api/v2/etf/holdings?symbol=${document.getElementById("fund_selected").value}`;  <!--    &date=2021-05-13-->
        table_code = `
            <table>
                <tr>
                    <th>Rank</th>
                    <th>Company</th>
                    <th>Ticker</th>
                    <th>Last Price</th>
                    <th>Weight</th>
                    <th>Shares</th>
                    <th>Market Value</th>
                </tr>`
        fetch(holdings_url)
            .then(res => res.json())
            .then((out) => {
                var symbol = out.symbol;
                var date = out.date;
                var holdings = out.holdings;
                for (holding=0; holding<holdings.length; holding++) {
                    var stats = holdings[holding];
                    var ticker = stats["ticker"]
                    var weightage = stats["weight"]
                    var num_shares = stats["shares"]
                    var mkt_value = stats["market_value"]
                    var quote = Math.round(100 * mkt_value / num_shares) / 100

                    if (ticker == null) {
                        ticker = ""
                    }
                    ticker_list.push(ticker)
                    weight_list.push(weightage)
                    top_20_weight += weightage
                    if (ticker_list.length <= 10) {
                        top_10_weight += weightage
                    }
                    else if (ticker_list.length == 20) {
                        load_graph(ticker_list, weight_list, top_10_weight, top_20_weight)
                    }

                    var company = stats["company"]
                    img_url = `https://g.foolcdn.com/art/companylogos/mark/${ticker}.png`
                    table_code += `
                        <tr onclick="load_individual_profile(this);">
                            <td style="width: min-content;">${stats["weight_rank"]}</td>
                            <td><div><img src=${img_url} onerror=this.src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSl4idYt_TOF1TPtJ1rF8OOLgALA0WDd00shg&usqp=CAU"><div>${company}</div></div></td>
                            <td>${ticker}</td>
                            <td>$${quote}</td>
                            <td>${weightage}%</td>
                            <td>${num_shares.toLocaleString()}</td>
                            <td>$${mkt_value.toLocaleString()}</td>
                        </tr>`
                }
                table_code += "</table>"
                document.getElementsByClassName("scrollable_div")[0].innerHTML = table_code
            })
            .catch(err => { throw err });
    }
}

var weighting_chart = null

function load_graph(ticker_list, weight_list, top_10_weight, top_20_weight) {
    if (weighting_chart != null){
        weighting_chart.destroy();
    }

    weighting_chart = document.getElementById('weighting_chart');
    weighting_chart = new Chart(weighting_chart, {
        data: {
            labels: ticker_list,
            datasets: [
                {
                    label: 'Weight',
                    type: 'bar',
                    data: weight_list,
                    backgroundColor: 'rgb(38, 166, 154)',
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
                        gridLines: {
                            drawOnChartArea: false,
                            color: "grey",
                        },
                        type: "linear",
                        stacked: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Weightage [%]',
                            beginAtZero: true,
                        },
                    }],

                xAxes: [{
                    offset: true,
                    gridLines: {
                        drawOnChartArea: false,
                        color: "grey",
                    },
                    stacked: true
                }],
            },

            // To show value when hover on any part of the graph
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(tooltipItems, data) {
                        return "Weight: " + tooltipItems.yLabel + '%';
                    }
                },
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

     document.getElementsByClassName("weightage_div")[0].innerHTML = `
            <div><b>Top 10 Holdings:</b> ${Math.round(top_10_weight * 100) / 100}%</div>
            <div><b>Top 20 Holdings:</b> ${Math.round(top_20_weight * 100) / 100}%</div>
        </div>`
}

function load_trades(elem) {
    var btn_type = document.getElementsByClassName("btn_type");
    for (i=0; i<btn_type.length; i++) {
        btn_type[i].classList.remove("selected");
    }
    btn_type[elem].classList.add("selected");
    document.getElementsByClassName("search_bar")[0].style.removeProperty("display");
    if (trades_clicks == 0) {
        holdings_clicks = 0, trades_clicks = 1, news_clicks = 0;
        var fund_selected = document.getElementById("fund_selected").value;
        if (fund_selected != "PRNT" && fund_selected != "IZRL") {
            let trades_url = `https://arkfunds.io/api/v2/etf/trades?symbol=${fund_selected}`;
            table_code = `
            <table>
                <tr>
                    <th>Date</th>
                    <th>Company</th>
                    <th>Ticker</th>
                    <th>Direction</th>
                    <th>Shares</th>
                    <th>ETF Weight</th>
                </tr>`
            fetch(trades_url)
                .then(res => res.json())
                .then((out) => {
                    var trades = out["trades"]
                    for (trade=0; trade<trades.length; trade++) {
                        var stats = trades[trade];
                        var ticker = stats["ticker"]
                        if (ticker == null) {
                            ticker = ""
                        }
                        var company = stats["company"]
                        img_url = `https://g.foolcdn.com/art/companylogos/mark/${ticker}.png`
                        table_code += `
                        <tr onclick="load_individual_profile(this);">
                           <td>${stats["date"]}</td>
                           <td><div><img src=${img_url} onerror=this.src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSl4idYt_TOF1TPtJ1rF8OOLgALA0WDd00shg&usqp=CAU"><div>${company}</div></div></td>
                           <td>${ticker}</td>
                           <td>${stats["direction"]}</td>
                           <td>${stats["shares"].toLocaleString()}</td>
                           <td>${stats["etf_percent"]}%</td>
                        </tr>`
                    }
                    table_code += "</table>"
                    document.getElementsByClassName("scrollable_div")[0].innerHTML = table_code
                })
                .catch(err => { throw err });
        }
        else {
            document.getElementsByClassName("scrollable_div")[0].innerHTML = `<div class="instructions">${fund_selected} is not an actively manages ETF. There are no daily trades available.</div>`
        }
    }
}

function load_news(elem) {
    var btn_type = document.getElementsByClassName("btn_type");
    for (i=0; i<btn_type.length; i++) {
        btn_type[i].classList.remove("selected");
    }
    btn_type[elem].classList.add("selected");
    document.getElementsByClassName("search_bar")[0].style.display = "none";
    if (news_clicks == 0) {
        holdings_clicks = 0, trades_clicks = 0, news_clicks = 1;
        var today_date = new Date();
        today_date.setMonth(today_date.getMonth() - 1);
        date_from = today_date.toISOString().split("T")[0];
        var news_url = `https://arkfunds.io/api/v1/etf/news?symbol=${document.getElementById('fund_selected').value}&date_from=${date_from}`
        news_code = ""
        fetch(news_url)
            .then(res => res.json())
            .then((out) => {
                news = out["news"]
                for (i=0; i<news.length; i++) {
                    var stats = news[i]
                    var news_date = stats["datetime"].split("T")[0]
                    var headline = stats["headline"]
                    var image = stats["image"]
                    if (image == "") {
                        image = "static/images/not_available.svg"
                    }
                    var source = stats["source"]
                    var url = stats["url"]
                    news_code += `
                        <div>
                            <div class="news_div">
                                <a href="${url}" target="_blank"><img src="${image}" onerror=this.src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSl4idYt_TOF1TPtJ1rF8OOLgALA0WDd00shg&usqp=CAU"></a>
                                <div>
                                    <div><a href="${url}" target="_blank"><b>${headline} (${news_date})</b></a></div>
                                    <div>${source}</div>
                                </div>
                            </div>
                        </div>`
                }
                document.getElementsByClassName("scrollable_div")[0].innerHTML = news_code
            })
    }
}

function load_individual_profile(elem) {
    document.getElementById("ticker_description").innerHTML = ""
    document.getElementById("ticker_trade").innerHTML = ""
    document.getElementById("fund_ownership").innerHTML = ""
    if (profile_clicks == 0) {
        var ticker_selected = elem.querySelectorAll("td")[2].innerHTML;
        if (ticker_selected != "") {
            profile_clicks = 1
            var fund_selected = document.getElementById("fund_selected").value
            var profile_url = `https://arkfunds.io/api/v1/stock/profile?symbol=${ticker_selected}`
            fetch(profile_url)
                .then(res => res.json())
                .then((out) => {
                    var company_name = out["name"].replace(",", "");
                    img_url = `https://g.foolcdn.com/art/companylogos/mark/${ticker_selected}.png`
                    profile_code = `
                        <div id="img_div">
                            <a href="/ticker/?quote=${out["ticker"]}" target="_blank"><img src="${img_url}" onerror=this.src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSl4idYt_TOF1TPtJ1rF8OOLgALA0WDd00shg&usqp=CAU"></a>
                        </div>
                        <div id="ticker_intro">
                            <div><span><a href="/ticker/?quote=${out["ticker"]}" target="_blank">${company_name} (${out["ticker"]})</a></span></div>
                            Sector: <b>${out["sector"]}</b><br>Industry: <b>${out["industry"]}</b>
                        </div>
                        <div class="ticker_summary">
                        <p><b>Summary</b></p>
                        ${out["summary"]}<br>
                        <a href=${out["website"]} target="_blank" class="read_more"><i>${out["website"]}</i></a>
                        </div>
                        `
                    document.getElementById("ticker_description").innerHTML = profile_code
                })

            if (fund_selected != "PRNT" && fund_selected != "IZRL") {
                individual_trade_code = `
                <p><b>Trades of ${ticker_selected} made by ${fund_selected}</b></p>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Direction</th>
                        <th>ETF Percent</th>
                        <th>Shares</th>
                        <th>Fund</th>
                    </tr>`
                var trades_url = `https://arkfunds.io/api/v1/stock/trades?symbol=${ticker_selected}`
                fetch(trades_url)
                    .then(res => res.json())
                    .then((out) => {
                        var trades = out["trades"];
                        for (trade=0; trade<trades.length; trade++) {
                            var fund  = trades[trade]["fund"];
                            if (fund == document.getElementById("fund_selected").value) {
                                var date = trades[trade]["date"];
                                var direction = trades[trade]["direction"];
                                var etf_percent = trades[trade]["etf_percent"];
                                var shares = trades[trade]["shares"];
                                individual_trade_code +=
                                    `<tr>
                                         <td>${date}</td>
                                         <td>${direction}</td>
                                         <td>${etf_percent}%</td>
                                         <td>${shares.toLocaleString()}</td>
                                         <td>${fund}</td>
                                     </tr>`
                            }
                        }
                        individual_trade_code += "</table>"
                        document.getElementById("ticker_trade").innerHTML = individual_trade_code
                    })
                    .catch(err => { throw err });
            }
            else {
                document.getElementById("ticker_trade").innerHTML = `<p><b>Trades of ${ticker_selected} made by ${fund_selected}</b></p><div class="instructions">${fund_selected} is not an actively manages ETF. Hence, there are no daily trades for ${ticker_selected}.</div>`
            }

            var ownership_url = `https://arkfunds.io/api/v1/stock/fund-ownership?symbol=${ticker_selected}`
            ownership_code = `
            <p><b>Ownership of ${ticker_selected} by all ARK Funds</b></p>
            <table>
                <tr>
                    <th>Fund</th>
                    <th>Weight</th>
                    <th>Rank</th>
                    <th>Shares</th>
                    <th>Market Value</th>
                    <th>Date</th>
                </tr>`
            fetch(ownership_url)
                .then(res => res.json())
                .then((out) => {
                    var ownerships = out["ownership"]
                    for (ownership=0; ownership<ownerships.length; ownership++) {
                        var stats = ownerships[ownership]
                        ownership_code += `
                        <tr>
                            <td>${stats["fund"]}</td>
                            <td>${stats["weight"]}%</td>
                            <td>${stats["weight_rank"]}</td>
                            <td>${stats["shares"].toLocaleString()}</td>
                            <td>$${stats["market_value"].toLocaleString()}</td>
                            <td>${out["date"]}</td>
                        <tr>`
                    }
                    var total = out["totals"]
                    ownership_code += `
                        <tr>
                            <td>Number Funds: ${total["funds"]}</td>
                            <td></td>
                            <td></td>
                            <td>${total["shares"].toLocaleString()}</td>
                            <td>$${total["market_value"].toLocaleString()}</td>
                            <td>${out["date"]}</td>
                        </tr>
                    </table>`
                    document.getElementById("fund_ownership").innerHTML = ownership_code;
                    document.getElementById("ticker_model").style.display = "block";
                })
                .catch(err => { throw err });
        }
    }
}

var ticker_model = document.getElementById("ticker_model");
var ticker_span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
ticker_span.onclick = function() {
    ticker_model.style.display = "none";
    profile_clicks = 0
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == ticker_model) {
    ticker_model.style.display = "none";
    profile_clicks = 0
  }
}
