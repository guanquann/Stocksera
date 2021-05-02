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

function date_filter() {
    // selected_date = document.getElementById("select_date").value;

}