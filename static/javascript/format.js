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
        if (iframe.length != 0) {

            for (i=0; i<iframe.length; i++) {
                iframe[i].contentDocument.getElementsByTagName("body")[0].classList.add("dark_mode")
            }
        }
        localStorage.setItem("mode", "dark");
    }
    else {
        document.getElementsByTagName("body")[0].classList.remove("dark_mode");
        if (iframe.length != 0) {
            for (i=0; i<iframe.length; i++) {
                iframe[i].contentDocument.getElementsByTagName("body")[0].classList.remove("dark_mode")
            }
        }
        localStorage.setItem("mode", "light");
    }
}

function restore_dark_mode() {
    if (localStorage.getItem("mode") == "dark") {
        document.getElementsByTagName("body")[0].classList.add("dark_mode");
        document.getElementById("dark_mode").checked = true;
    }
}

function show_spinner() {
    var add_to_div = `<div class="spinner_container">
                          <img src="/static/images/spinner.gif" class="spinner">`

    document.getElementById("spinner_div").innerHTML = add_to_div
}