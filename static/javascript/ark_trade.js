function update_fund(elem) {
    document.getElementById("fund_selected").value = elem.innerHTML;
    load_holdings()
    load_profile()
}

function load_profile() {
    let profile_url = `https://arkfunds.io/api/v1/etf/profile?symbol=${document.getElementById("fund_selected").value}`;
    fetch(profile_url)
        .then(res => res.json())
        .then((out) => {
            profile = out["profile"][0]
            console.log(profile)
            profile_code = `
                <span>${profile["name"]} (${profile["symbol"]})</span>
                <p>${profile["description"]}</p>
                ${profile["website"]}
            `
            document.getElementById("profile").innerHTML = profile_code
        })
        .catch(err => { throw err });
}

function load_holdings() {
    let holdings_url = `https://arkfunds.io/api/v1/etf/holdings?symbol=${document.getElementById("fund_selected").value}`;
    <!--    &date=2021-05-13-->
    table_code = `
        <table>
            <tr>
                <th>Weight Rank</th>
                <th>Company</th>
                <th>Ticker</th>
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
                if (ticker == null) {
                    ticker = ""
                }
                var company = stats["company"]
                img_url = `https://logo.clearbit.com/${company.split(" ")[0].toLowerCase()}.com`
                table_code += `
                    <tr>
                        <td style="width: min-content;">${stats["weight_rank"]}</td>
                        <td><div><img src=${img_url}><a href="http://127.0.0.1:8000/ticker/?quote=${ticker}">${company}</a></div></td>
                        <td>${ticker}</td>
                        <td>${stats["weight"]}%</td>
                        <td>${stats["shares"]}</td>
                        <td>$${stats["market_value"]}</td>
                    </tr>`

            }
            table_code += "</table>"
            document.getElementsByClassName("scrollable_div")[0].innerHTML = table_code
        })
        .catch(err => { throw err });
}

function load_trades() {
    let trades_url = `https://arkfunds.io/api/v1/etf/trades?symbol=${document.getElementById("fund_selected").value}`;

    table_code = `
    <table>
        <tr>
            <th>Company</th>
            <th>Ticker</th>
            <th>Date</th>
            <th>Direction</th>
            <th>Shares</th>
            <th>ETF Weight</th>
        </tr>`


    fetch(trades_url)
        .then(res => res.json())
        .then((out) => {
            var trades = out["trades"]
            for (trade=0; trade<trades.length; trade++) {
                var stats = trades[trade]
                table_code += `
                <tr>
                   <td>${stats["company"]}</td>
                   <td>${stats["ticker"]}</td>
                   <td>${stats["date"]}</td>
                   <td>${stats["direction"]}</td>
                   <td>${stats["shares"]}</td>
                   <td>${stats["etf_percent"]}%</td>
                </tr>`
            }
            table_code += "</table>"
            document.getElementsByClassName("scrollable_div")[0].innerHTML = table_code
        })
        .catch(err => { throw err });
}

function load_ownership() {
    ticker_selected = "TSLA"
    let ownership_url = `https://arkfunds.io/api/v1/stock/fund-ownership?symbol=${ticker_selected}`

    table_code = `
    <table>
        <tr>
            <th>Fund</th>
            <th>Weight</th>
            <th>Weight Rank</th>
            <th>Shares</th>
            <th>Market Value</th>
            <th>Date</th>
        </tr>`

    fetch(ownership_url)
        .then(res => res.json())
        .then((out) => {
            var ownerships = out["ownership"]
            console.log(ownerships)
            for (ownership=0; ownership<ownerships.length; ownership++) {
                var stats = ownerships[ownership]
                table_code += `
                <tr>
                    <td>${stats["fund"]}</td>
                    <td>${stats["weight"]}</td>
                    <td>${stats["weight_rank"]}</td>
                    <td>${stats["shares"]}</td>
                    <td>$${stats["market_value"]}</td>
                    <td>${out["date"]}</td>
                <tr>`
            }
            var total = out["totals"]
            table_code += `
                <tr>
                    <td>Total: ${total["funds"]}</td>
                    <td></td>
                    <td></td>
                    <td>${total["shares"]}</td>
                    <td>$${total["market_value"]}</td>
                    <td>${out["date"]}</td>
                </tr>
            </table>`
            document.getElementsByClassName("scrollable_div")[0].innerHTML = table_code
        })
        .catch(err => { throw err });
}