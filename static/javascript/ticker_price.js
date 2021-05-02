function display_data() {
    if (document.getElementsByName("quote")[0].value == "-") {
        document.getElementById("error_msg").style.removeProperty("display");
        document.getElementsByName("quote")[0].value = "";
    }

    else if (document.getElementsByName("quote")[0].value != "") {
        document.getElementsByClassName("ticker_summary")[0].style.removeProperty("display");
        document.getElementsByClassName("chart-container")[0].style.removeProperty("display");
        document.getElementsByClassName("ticker_news")[0].style.removeProperty("display");
        
        document.getElementById("more_info_div").style.removeProperty("display");
        document.getElementById("img_div").style.removeProperty("display");
        document.getElementById("ticker_intro").style = "display:inline-block;";
        document.getElementById("days_btn").style.removeProperty("display");
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