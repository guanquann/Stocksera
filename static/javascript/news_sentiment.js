function display_data() {
    var main_content = document.getElementsByClassName("ticker_news");
    main_content[0].style.removeProperty("display");
    var tr = main_content[0].querySelector("table").getElementsByTagName("tr")
    for (row=1; row<tr.length; row++) {
        if (tr[row].children[2].innerHTML == "Bearish") {
            tr[row].style.color = "red"
        }
        else if (tr[row].children[2].innerHTML == "Bullish") {
            tr[row].style.color = "rgb(38, 166, 154)"
        }

    }
}