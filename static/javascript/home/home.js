function show_dd(type, elem) {
    var dd_btn = document.getElementsByClassName("dd_btn")[0].querySelectorAll("button")
    for (i=0; i<dd_btn.length; i++) {
        dd_btn[i].classList.remove("selected")
    }
    elem.classList.add("selected");

    if (type == "analysis") {
        text = "View latest price, key statistics, major holders, institutional holders, earnings, recommendations and sort historical data."
        url = "/ticker/"
    }
    else if (type == "options") {
        text = "View max pain for the week, Call & Put Ratio and option chain of a ticker."
        url = "/ticker/options/"
    }
    else if (type == "short_volume") {
        text = "Get short volume of some of the popular tickers."
        url = "/ticker/short_volume/"
    }
    else if (type == "ftd") {
        text = "View Failure to Deliver (FTD) data of some of the popular tickers. Data is updated whenever latest information from SEC is available."
        url = "/ticker/failure_to_deliver/"
    }
    else if (type == "wsb_live") {
        text = "View number of mentions of a ticker in r/wallstreetbets over time."
        url = "/wsb_live/"
    }
    document.getElementById("dd_description").innerHTML = `
        <div class="section_div_text">${text}</div><div class="href_btn"><a href="${url}">VIEW MORE</a></div>`
}

function show_reddit(type, elem) {
    var reddit_btn = document.getElementsByClassName("reddit_btn")[0].querySelectorAll("button")
    for (i=0; i<reddit_btn.length; i++) {
        reddit_btn[i].classList.remove("selected")
    }
    elem.classList.add("selected");

    if (type == "reddit_trending") {
        text = "Get trending tickers on stocks & crypto-related subreddits based on sentiment, number of posts, comments and upvotes."
        url = "/reddit_analysis/"
    }
    else if (type == "wsb_live") {
        text = "Get live sentiment and analysis on most mentioned tickers in WSB discussion thread."
        url = "/wsb_live/"
    }
    else if (type == "crypto_live") {
        text = "Get live sentiment and analysis on most mentioned symbols in r/CryptoCurrency discussion thread."
        url = "/crypto_live/"
    }
    else if (type == "reddit_etf") {
        text = "WSB ETF contains the top 10 trending tickers on r/wallstreetbets. Past performance included as well."
        url = "/reddit_etf/"
    }
    else if (type == "subreddit") {
        text = "View percentage of growth in users and active users in popular subreddits."
        url = "/subreddit_count/"
    }
    document.getElementById("reddit_description").innerHTML = `
        <div class="section_div_text">${text}</div><div class="href_btn"><a href="${url}">VIEW MORE</a></div>`
}

function show_discover(type, elem) {
    var discover_btn = document.getElementsByClassName("discover_btn")[0].querySelectorAll("button")
    for (i=0; i<discover_btn.length; i++) {
        discover_btn[i].classList.remove("selected")
    }
    elem.classList.add("selected");

    if (type == "heatmap") {
        text = "View overall performance of S&P500, Nasdaq100 & Crypto market."
        url = "/market_summary/"
    }
    else if (type == "short_int") {
        text = "View stocks with high short interest. Squeeze time!"
        url = "/short_interest/"
    }
    else if (type == "latest_insider") {
        text = "Analyse largest net latest insider transactions in the last month."
        url = "/latest_insider/"
    }
    else if (type == "ark") {
        text = "Get holdings, daily trades and news of ARK Fund."
        url = "/ark_trades/"
    }
    else if (type == "amd_xlnx_ratio") {
        text = "View current AMD-XLNX Share Price Ratio and percentage upside for XLNX when the merger is complete."
        url = "/amd_xlnx_ratio/"
    }
    else if (type == "earnings") {
        text = "View earnings calendar of the week."
        url = "/earnings_calendar/"
    }
    document.getElementById("discover_description").innerHTML = `
        <div class="section_div_text">${text}</div><div class="href_btn"><a href="${url}">VIEW MORE</a></div>`
}

function show_economy(type, elem) {
    var economy_btn = document.getElementsByClassName("economy_btn")[0].querySelectorAll("button")
    for (i=0; i<economy_btn.length; i++) {
        economy_btn[i].classList.remove("selected")
    }
    elem.classList.add("selected");

    if (type == "rrp") {
        text = "View record high reverse-repo transaction."
        url = "/reverse_repo/"
    }
    else if (type == "treasury") {
        text = "Get daily US Treasury’s cash and debt operations for the Federal Government."
        url = "/daily_treasury/"
    }
    else if (type == "inflation") {
        text = "View heat map of the monthly inflation level."
        url = "/inflation/"
    }
    else if (type == "retail") {
        text = "Get total sales of the US economy and look at how Covid-19 cases affect spending."
        url = "/retail_sales/"
    }
    else if (type == "initial_jobless_claims") {
        text = "View number of individuals who filed for unemployment insurance last week."
        url = "/initial_jobless_claims/"
    }
    document.getElementById("economy_description").innerHTML = `
        <div class="section_div_text">${text}</div><div class="href_btn"><a href="${url}">VIEW MORE</a></div>`
}

function show_beta(type, elem) {
    var beta_btn = document.getElementsByClassName("beta_btn")[0].querySelectorAll("button")
    for (i=0; i<beta_btn.length; i++) {
        beta_btn[i].classList.remove("selected")
    }
    elem.classList.add("selected");

    if (type == "true_beta") {
        text = "Ever wonder why different websites show different beta values for the same stock? Find out here!"
        url = "/beta/"
    }
    else if (type == "covid_beta") {
        text = "With the rise of Covid-19 cases, what are some of the best plays right now?"
        url = "/covid_beta/"
    }
    document.getElementById("beta_description").innerHTML = `
        <div class="section_div_text">${text}</div><div class="href_btn"><a href="${url}">VIEW MORE</a></div>`
}

function show_op(type, elem) {
    var op_btn = document.getElementsByClassName("op_btn")[0].querySelectorAll("button")
    for (i=0; i<op_btn.length; i++) {
        op_btn[i].classList.remove("selected")
    }
    elem.classList.add("selected");

    if (type == "video") {
        text = "Watch out for new videos in our YouTube Channel for new updates in the future!"
        url = "https://youtu.be/jkAZu7DvhvY"
    }
    else if (type == "donate") {
        text = `Stocksera is an open-source application.
                I spent months creating this application, with no monetary benefits.
                If you like this project, you can suppoort me via <a href="https://www.paypal.me/stocksera" target="_blank">Paypal</a> or <a href="https://www.patreon.com/stocksera" target="_blank">Patreon</a>.`
        url = "https://www.paypal.com/paypalme/stocksera"
    }
    else if (type == "code") {
        text = "You can view the code in GitHub. Do give a star if you like it!"
        url = "https://github.com/spartan737/Stocksera"
    }
    document.getElementById("op_description").innerHTML = `
        <div class="section_div_text">${text}</div><div class="href_btn"><a href="${url}" target="_blank">VIEW MORE</a></div>`
}

function restore_dark_mode_img() {
    if (localStorage.getItem("mode") == "dark") {
        img = document.querySelector("#intro_images").querySelectorAll("img")
        for (i=0; i<img.length; i++) {
            img[i].src = img[i].src.replace("light", "dark")
        }
    }
}