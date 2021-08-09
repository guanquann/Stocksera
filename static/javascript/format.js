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

function expand_nav(elem) {
    sub_nav_bar = document.getElementsByClassName("sub_nav_bar");
    selected_nav = elem.querySelectorAll(".sub_nav_bar");
    to_open = true

    if (selected_nav[0].style.display != "none") {
        to_open = false
    }

    for (i=0; i<sub_nav_bar.length; i++) {
        sub_nav_bar[i].style.display = "none";
    }

    for (i=0; i<selected_nav.length; i++) {
        if (to_open == true) {
            selected_nav[i].style.removeProperty("display");
        }
    }
}

function hide_nav_bar() {
    var nav_bar_div = document.getElementById("nav_bar_div");
    var nav_bar_div_sm = document.getElementById("nav_bar_div_sm");
    if (nav_bar_div.style.opacity == "1") {
        nav_bar_div.style.removeProperty("opacity");
        nav_bar_div.style.display = "none";
        nav_bar_div_sm.style.removeProperty("left");
    }
    else {
        nav_bar_div.style.opacity = "1";
        nav_bar_div.style.display = "block";
        nav_bar_div_sm.style.left = "105px";
    }
}

function activate_dark_mode() {
    var iframe = document.getElementsByTagName("iframe");
    if (document.getElementById("dark_mode").checked == true) {
        document.getElementsByTagName("body")[0].classList.add("dark_mode");
        localStorage.setItem("mode", "dark");
        if (iframe.length > 1) {
            for (i=1; i<iframe.length; i++) {
                if (typeof(iframe[i].contentDocument) != null) {
                    iframe[i].contentDocument.getElementsByTagName("body")[0].classList.add("dark_mode")
                }
            }
        }
    }
    else {
        document.getElementsByTagName("body")[0].classList.remove("dark_mode");
        localStorage.setItem("mode", "light");
        if (iframe.length > 1) {
            for (i=1; i<iframe.length; i++) {
                if (typeof(iframe[i].contentDocument) != null) {
                    iframe[i].contentDocument.getElementsByTagName("body")[0].classList.remove("dark_mode")
                }
            }
        }
    }
}

function restore_dark_mode() {
    if (localStorage.getItem("mode") == "dark") {
        document.getElementsByTagName("body")[0].classList.add("dark_mode");
        document.getElementById("dark_mode").checked = true;
    }
}

function show_ticker_price(information) {
    <!--Code to show price change-->
    var latest_price = information["regularMarketPrice"];
    var mkt_close = information["previousClose"];
    <!--Code to show price change-->
    var price_change = Math.round((latest_price - mkt_close) * 100) / 100
    var price_percentage_change = Math.round(((latest_price - mkt_close) / mkt_close) * 10000) / 100
    if (price_change > 0) {
        price_change = "+" + String(price_change)
        price_percentage_change = "+" + String(price_percentage_change) + "%"
    }
    else {
        price_percentage_change = String(price_percentage_change) + "%"
    }

    <!--Function to check that dictionary has a key-->
    function check_stats(property) {
        if (information.hasOwnProperty(property) == true) {
            property_name = information[property]
        }
        else {
            property_name = "N/A"
        }
        return property_name
    }

    function load_error_img(elem, symbol) {
        document.getElementById("ticker_basic_stats").innerHTML = `<div id="no_img_div">
        <div>${symbol}</div></div>` + document.getElementById("ticker_basic_stats").innerHTML
    }

    <!--If ticker does not have a website, bring users to Yahoo Finance-->
    if (information.hasOwnProperty("website") == true) {
        var website = information["website"]
    }
    else {
        var website = `https://finance.yahoo.com/quote/${information["symbol"]}`
    }

    <!--If ticker does not have an image, show a default image-->
    var img = `https://g.foolcdn.com/art/companylogos/mark/${information["symbol"]}.png`
    var img_code = `<img src="${img}" onerror="this.error=null;this.parentElement.remove();load_error_img(this, information['symbol'])">`

    <!--Code to display image, full name, symbol, industry and sector-->
    var official_name = check_stats("longName")
    var sector = check_stats("sector")
    var industry = check_stats("industry")

    if (price_percentage_change.includes("-")) {
        var price_code = `<div class="price_details negative_price">$${latest_price}<br>${price_change} (${price_percentage_change})</div>`
    }
    else {
        var price_code = `<div class="price_details positive_price">$${latest_price}<br>${price_change} (${price_percentage_change})</div>`
    }

    var ticker_basic_stats_code = `
        <div id="img_div">${img_code}</div>
        <div id="ticker_intro">
            <span>${official_name} (${information["symbol"]})</span>
            <br>Sector: <b>${sector}</b><br>Industry: <b>${industry}</b>
        </div>
        ${price_code}`
    document.getElementById("ticker_basic_stats").innerHTML = ticker_basic_stats_code;
}

function clickAndDisable(link) {
    // disable subsequent clicks
    link.onclick = function(event) {
        event.preventDefault();
    }
}