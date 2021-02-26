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