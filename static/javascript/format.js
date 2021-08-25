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

function highlight_selected_nav(elem) {
    document.getElementById(elem).classList.add("current_link")
}

function top_right_nav(elem) {
    var nav_bar_div = document.getElementById("nav_bar_div");
    var dark_mode_btn = document.getElementById("dark_mode_btn");
    if (elem.classList.contains("opened")){
        elem.classList.remove("opened")
        nav_bar_div.style.height = 0;
        nav_bar_div.style.width = 0;
        nav_bar_div.querySelector("ul").style.display = "none"
        dark_mode_btn.style.display = "none"
    }
    else {
        elem.classList.add("opened")
        nav_bar_div.style.height = "230px";
        nav_bar_div.style.width = "100%";
        nav_bar_div.querySelector("ul").style.display = "block"
        dark_mode_btn.style.display = "block"
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

function load_error_img(elem, symbol) {
    document.getElementById("ticker_basic_stats").innerHTML = `<div id="no_img_div">
    <div>${symbol}</div></div>` + document.getElementById("ticker_basic_stats").innerHTML
}

function load_table_error_img(elem, symbol) {
    elem.parentElement.innerHTML = `<div class="no_img_table_div">
        <div class="no_img_table_img table_ticker_logo">
            <div>${symbol[0]}</div>
        </div>
        <div class="no_img_table_img_symbol"><b>${symbol}</b></div>
        </div>`
    elem.remove()
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

function check_if_num(property) {
    property_name = information[property]
    if (typeof(property_name) == "number") {
        property_name= Number(property_name).toLocaleString()
    }
    else {
        property_name = "N/A"
    }
    return property_name
}

function show_ticker_price(information) {
    var latest_price = information["regularMarketPrice"];
    var mkt_close = information["previousClose"];
    var price_change = information["regularMarketChange"]
    var price_percentage_change = information["regularMarketChangePercent"]

    if (price_change > 0) {
        price_change = "+" + String(price_change)
        price_percentage_change = "+" + String(price_percentage_change)
        color_type = "positive_price"
    }
    else {
        color_type = "negative_price"
    }

    <!--If ticker does not have an image, show a default image-->
    var img = `https://g.foolcdn.com/art/companylogos/mark/${information["symbol"]}.png`
    var img_code = `<img src="${img}" onerror="this.error=null;this.parentElement.remove();load_error_img(this, information['symbol'])">`

    <!--Code to display image, full name, symbol, industry and sector-->
    var official_name = check_stats("longName")
    var sector = check_stats("sector")
    var industry = check_stats("industry")

    var current_mkt_status = information["marketState"]

    if (current_mkt_status == "PRE" || current_mkt_status == "PREPRE") {
        mkt_pre_post_code = `<div style="font-size:9px">Pre: $${Math.round((Number(latest_price.replace(",", "")) + Number(information["preMarketChange"])) * 100) / 100} (${information["preMarketChangePercent"]})</div> `
    }
    else if (current_mkt_status == "POST" || current_mkt_status == "POSTPOST") {
        mkt_pre_post_code = `<div style="font-size:9px">Post: $${Math.round((Number(latest_price.replace(",", "")) + Number(information["postMarketChange"])) * 100) / 100} (${information["postMarketChangePercent"]})</div> `
    }
    else {
        mkt_pre_post_code = ""
    }

    var price_code = `<div class="price_details ${color_type}">$${latest_price}
        <br> <div>${price_change} (${price_percentage_change})</div>
        ${mkt_pre_post_code}</div>`

    var ticker_basic_stats_code = `
        <div id="img_div">${img_code}</div>
        <div id="ticker_intro">
            <span>${official_name} (${information["symbol"]})</span>
            <br>Sector: <b>${sector}</b><br>Industry: <b>${industry}</b>
        </div>
        ${price_code}`
    document.getElementById("ticker_basic_stats").innerHTML = ticker_basic_stats_code;
}

function btn_selected(elem) {
    date_range = document.getElementsByName("date_range")
    for (i=0; i<date_range.length; i++) {
        date_range[i].classList.remove("selected")
    }
    elem.classList.add("selected")
}

function get_date_difference(duration, delimiter) {
    var d = new Date();
    d.setMonth(d.getMonth() - duration);
    var dd = d.getDate();
    if (dd <= 9) {
        dd = "0" + dd
    }
    var mm = d.getMonth() + 1;
    if (mm <= 9) {
        mm = "0" + mm
    }
    var yyyy = d.getFullYear();
    var date_threshold = yyyy + delimiter + mm + delimiter + dd;
    return date_threshold
}

function clickAndDisable(link) {
    // disable subsequent clicks
    link.onclick = function(event) {
        event.preventDefault();
    }
}