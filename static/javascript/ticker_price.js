function display_data() {
    var error_msg_class = document.getElementById("error_msg").className;
    if (error_msg_class == "instructions error_true") {
        document.getElementById("error_msg").style.removeProperty("display");
    }

    else {
        document.getElementsByClassName("ticker_summary")[0].style.removeProperty("display");
        document.getElementsByClassName("tradingview-widget-container")[0].style.removeProperty("display");

        document.getElementById("img_div").style.removeProperty("display");
        document.getElementById("ticker_intro").style = "display:inline-block;";
        document.getElementById("ticker_table").style.removeProperty("display");
        document.getElementById("latest_price").style.removeProperty("display");


        if (document.getElementById("latest_price").innerHTML.includes("-")) {
            document.getElementById("latest_price").style.color = "#ef5350";
        }
        else {
            document.getElementById("latest_price").style.color = "#26a69a";
        }
    }
}

function expand_iframe(elem) {
    elem.style.height = elem.contentWindow.document.body.scrollHeight + 'px';
}