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
    sub_nav_bar = elem.getElementsByClassName("sub_nav_bar");
    for (i=0; i<sub_nav_bar.length; i++) {
        if (sub_nav_bar[i].style.display == "none") {
            sub_nav_bar[i].style.removeProperty("display");
        }
        else {
            sub_nav_bar[i].style.display = "none";
        }
    }
}

function show_spinner() {
    var add_to_div = `<div class="spinner_container">
                          <img src="/static/images/spinner.gif" class="spinner">`

    document.getElementById("spinner_div").innerHTML = add_to_div
}