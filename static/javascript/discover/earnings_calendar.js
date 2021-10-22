var earnings_container_div = document.getElementsByClassName("earnings_container");

function sortTicker(self, threshold) {
    var btns = document.getElementsByTagName("button");
    for (btn of btns) {
        btn.className = "";
    }
    self.className = "selected_btn"
    document.getElementById("search_ticker").value = "";

    for (earning=0; earning<earnings_container_div.length; earning++) {
        mkt_cap = earnings_calendar[earning][2];
        if (Number(mkt_cap) < threshold) {
            earnings_container_div[earning].style.display = "none";
        }
        else {
            earnings_container_div[earning].style.removeProperty("display");
        }
    }
}

const searchTicker = () =>{
    var btns = document.getElementsByTagName("button");
    for (btn of btns) {
        btn.className = "";
    }

    let filter = document.getElementById('search_ticker').value.toUpperCase();

    for (earning=0; earning<earnings_container_div.length; earning++) {
        ticker_name = earnings_calendar[earning][0].toUpperCase();
        ticker = earnings_calendar[earning][1];

        if (ticker.indexOf(filter) > -1 | ticker_name.indexOf(filter) > -1) {
            earnings_container_div[earning].style.removeProperty("display");
        }
        else {
            earnings_container_div[earning].style.display = "none";
        }

    }
}

function date_filter(elem) {
    var selected_date = elem.value;
    var main_divs = document.getElementById("main").getElementsByTagName("div");
    for (main_div=1; main_div<main_divs.length; main_div++) {
        if (selected_date == "All") {
            main_divs[main_div].style.removeProperty("display");
        }

        else if (! main_divs[main_div].classList.contains(selected_date)) {
            main_divs[main_div].style.display = "none";
        }
        else {
            main_divs[main_div].style.removeProperty("display");
        }
    }
}

function sort_by(elem) {
    var sort_selection = elem.value;
    for (earning=0; earning<earnings_container_div.length; earning++) {
        if (sort_selection == "Market Cap") {
            mkt_cap = earnings_calendar[earning][2];

        }
        else {
            continue
        }
    }
}