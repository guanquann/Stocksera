function to_remove(elem, text) {
    var more_details = document.getElementsByClassName("more_details");
    var show_more_btn = document.getElementsByClassName("show_more_btn");
    for (i=0; i<more_details.length; i++) {
        more_details[i].style.display = "none"
        show_more_btn[i].classList.remove("selected")
    }

    parent = elem.parentElement
    elem.remove()
    parent.innerHTML = `<button type="button" name="quote" class="show_more_btn submitted" onclick="to_remove(this, '${text}')">${text}</button>`

    document.getElementsByName(text)[0].style.removeProperty("display")
    parent.firstChild.classList.add("selected")
}

function submit_onload(elem) {
    if (elem == "") {
        document.getElementsByClassName('show_more_btn')[0].form.submit();
    }
}

function show_ticker_table(information) {
    <!--Check if input is an ETF/Crypto/Stock and display information to user accordingly-->
    var quoteType = information["quoteType"]
    if (quoteType == "ETF") {
        var summary = check_stats("longBusinessSummary").replace(/[^\x00-\x7F]/g, "");
        var official_name = check_stats("longName");
        var total_assets = information["totalAssets"];
        var navPrice = check_stats("navPrice");
        var three_year_return = information["threeYearAverageReturn"];
        var five_year_return = information["fiveYearAverageReturn"];
        var beta = check_stats("beta3Year");
        var yield = check_stats("Yield");
        var dividend_yield = information["trailingAnnualDividendYield"];
        var dividend_amount = information["trailingAnnualDividendRate"];

        if (dividend_yield != "N/A") {
            dividend_amount = "$" + String(dividend_amount)
        }

        table_part_ii_code = `
            <tr>
                <td>Total Assets: ${total_assets}</td>
                <td>NAV: ${navPrice}</td>
            </tr>
            <tr>
                <td>3Y Annual Return: ${three_year_return}</td>
                <td>5Y Annual Return: ${five_year_return}</td>
            </tr>
            <tr>
                <td>Beta: ${beta}</td>
                <td>Yield: ${yield}</td>
            </tr>
            <tr>
                <td>Div. Yield: ${dividend_yield}</td>
                <td>Dividend: ${dividend_amount}</td>
            </tr>`
        document.getElementById("more_info_div").style.removeProperty("display");
        btn_div = document.getElementsByClassName("btn_div")
        btn_div[1].style.display = "none"
        btn_div[4].style.display = "none"
        btn_div[5].style.display = "none"
        btn_div[6].style.display = "none"
        btn_div[7].style.display = "none"
        btn_div[8].style.display = "none"
        btn_div[9].style.display = "none"
    }

    else if (quoteType == "CRYPTOCURRENCY") {
        var summary = check_stats("description").replace(/[^\x00-\x7F]/g, "");
        var official_name = check_stats("shortName");
        var mkt_cap = information["marketCap"];
        var supply = information["circulatingSupply"];
        table_part_ii_code = `
            <tr>
                <td>Mkt Cap: ${mkt_cap}</td>
                <td>Circulating Supply: ${supply}</td>
            </tr>
        `
    }

    else {
        var summary = check_stats("longBusinessSummary").replace(/[^\x00-\x7F]/g, "");
        var official_name = check_stats("longName");
        var beta = check_stats("beta")
        var eps = check_stats("trailingEps")
        var p_e_ratio = check_stats("trailingPE")
        var forward_p_e = check_stats("forwardPE")

        var outstanding_shares = information["sharesOutstanding"]
        var floating_shares = information["floatShares"]
        var short_ratio = information["shortRatio"]
        var peg_ratio = information["pegRatio"]
        var enterpriseToRevenue = information["enterpriseToRevenue"]
        var income = information["netIncomeToCommon"]
        var mkt_cap = information["marketCap"];
        var short_percent = information["shortPercentOfFloat"]
        var dividend_yield = information["trailingAnnualDividendYield"]
        var dividend_amount = information["trailingAnnualDividendRate"]
        var employees = information["fullTimeEmployees"]
        var country = information["country"]

        if (dividend_yield != "N/A") {
            dividend_amount = "$" + String(dividend_amount)
        }
        table_part_ii_code = `
            <tr>
                <td>Outstanding Shares: ${outstanding_shares}</td>
                <td>Floating Shares: ${floating_shares}</td>
            </tr>
            <tr>
                <td>Short Ratio: ${short_ratio}</td>
                <td>Short % of Float: ${short_percent}</td>
            </tr>
            <tr>
                <td>P/E: ${p_e_ratio}</td>
                <td>Forward P/E: ${forward_p_e}</td>
            </tr>
            <tr>
                <td>PEG Ratio: ${peg_ratio}</td>
                <td>Enterprise value / Revenue: ${enterpriseToRevenue}</td>
            </tr>
            <tr>
                <td>Income: ${income}</td>
                <td>Mkt Cap: ${mkt_cap}</td>
            </tr>
            <tr>
                <td>Beta: ${beta}</td>
                <td>EPS: ${eps}</td>
            </tr>
            <tr>
                <td>Div. Yield: ${dividend_yield}</td>
                <td>Dividend: ${dividend_amount}</td>
            </tr>
            <tr>
                <td>Employees: ${employees}</td>
                <td>Country: ${country}</td>
            </tr>`
        document.getElementById("more_info_div").style.removeProperty("display");
    }

    <!--Code to display image, full name, symbol, industry and sector-->
    var sector = check_stats("sector")
    var industry = check_stats("industry")

    <!--If ticker does not have a website, bring users to Yahoo Finance-->
    if (information.hasOwnProperty("website") == true && information["website"] != "N/A") {
        var website = information["website"]
    }
    else {
        var website = `https://finance.yahoo.com/quote/${information["symbol"]}`
    }

    <!--Code to show summary of ticker-->
    var summary_code = `
        <p class="header">
            <b>Summary</b>
        </p>${summary}<br>
        <a href=${website} target="_blank" class="read_more"><i>${website}</i></a>`
    document.getElementsByClassName("ticker_summary")[0].innerHTML = summary_code;


    <!--Code to show basic statistics of ticker-->
    table_code = `
        <table>
            <tr>
                <td>Open: $${information["regularMarketOpen"]}</td>
                <td>Prev Close: $${information["previousClose"]}</td>
            </tr>
            <tr>
                <td>High: $${information["dayHigh"]}</td>
                <td>52-wk High: $${information["fiftyTwoWeekHigh"]}</td>
            </tr>
            <tr>
                <td>Low: $${information["regularMarketDayLow"]}</td>
                <td>52-wk Low: $${information["fiftyTwoWeekLow"]}</td>
            </tr>
            <tr>
                <td>Volume: ${information["regularMarketVolume"]}</td>
                <td>10D Avg Vol: ${information["averageDailyVolume10Day"]}</td>
            </tr>
            <tr>
                <td>50D SMA: $${information["fiftyDayAverage"]}</td>
                <td>200D SMA: $${information["twoHundredDayAverage"]}</td>
            </tr>`
    table_code += table_part_ii_code + "</table>";
    document.getElementsByClassName("scrollable_div")[0].innerHTML = table_code;
}

const buttonRight = document.getElementById('slideRight');
const buttonLeft = document.getElementById('slideLeft');

buttonRight.onclick = function () {
    document.getElementsByClassName('main_btn_div')[0].scrollLeft += 100;
};
buttonLeft.onclick = function () {
    document.getElementsByClassName('main_btn_div')[0].scrollLeft -= 100;
};