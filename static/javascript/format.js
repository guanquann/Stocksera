function update_price_color() {
    var tickers = document.getElementsByClassName("ticker_item");
    for (i=0; i<tickers.length; i++) {
        if (tickers[i].querySelector("span").innerHTML.includes("+") == true) {
            tickers[i].querySelector("span").style.color="#26a69a"
        }

        else {
            tickers[i].querySelector("span").style.color="#ef5350"
        }
    }
}

function show_ticker_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "ticker_price"
}

function show_reddit_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "reddit_analysis"
}

function show_google_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "google_analysis"
}

function show_industry_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "industry"
}

function show_reddit_etf_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "reddit_etf"
}

function show_opinion_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "opinion"
}

function show_contact_iframe() {
    document.getElementsByTagName("iframe")[0]["src"] = "contact"
}

function hide_nav_bar() {
    var nav_bar_btn = document.getElementById("nav_bar_btn");
    var nav_bar_div = document.getElementById("nav_bar_div");
    var nav_bar_title = document.getElementsByClassName("nav_bar_title")[0];
    var nav_bar = document.getElementsByClassName("nav_bar");
    var logo = document.getElementsByTagName("img");
    var iframe = document.getElementsByTagName("iframe")[0];

    if (nav_bar_btn.innerHTML == "&gt;") {  // &gt; == ">"
        nav_bar_div.style.width = "200px";
        for (i=0; i<logo.length; i++) {
            logo[i].style.width = "15px";
            nav_bar[i].style.fontSize = "medium";
            nav_bar[i].style.textAlign = "";
            nav_bar[i].style.marginTop = "";
            nav_bar[i].style.marginBottom = "";
        }
        nav_bar_title.style.fontSize = "medium";
        iframe.style.width = "84vw";
        nav_bar_btn.innerHTML = "<";
    }
    else {
        nav_bar_div.style.width = "70px";
        for (i=0; i<logo.length; i++) {
            logo[i].style.width = "35px";
            nav_bar[i].style.fontSize = "xx-small";
            nav_bar[i].style.textAlign = "center";
            nav_bar[i].style.marginTop = "9%";
            nav_bar[i].style.marginBottom = "9%";
        }
        nav_bar_title.style.fontSize = "xx-small";
        iframe.style.width = "94vw";
        nav_bar_btn.innerHTML = ">";
    }
}