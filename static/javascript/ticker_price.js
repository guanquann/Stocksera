function display_data() {
    if (document.getElementsByName("ticker")[0].value == "-") {
        document.getElementById("error_msg").style.removeProperty("display");
        document.getElementsByName("ticker")[0].value = "";
    }

    else if (document.getElementsByName("ticker")[0].value != "") {
        document.getElementsByClassName("ticker_summary")[0].style.removeProperty("display");
        document.getElementsByClassName("chart-container")[0].style.removeProperty("display");

        document.getElementById("img_div").style = "width:9%;display:inline-block;";
        document.getElementById("ticker_intro").style = "display:inline-block;";
        document.getElementById("days_btn").style.removeProperty("display");
        document.getElementById("ticker_table").style.removeProperty("display");
        document.getElementById("latest_price").style.removeProperty("display");

        if (document.getElementById("latest_price").innerHTML.includes("+")) {
            document.getElementById("latest_price").style.color = "green";
        }
        else {
            document.getElementById("latest_price").style.color = "red";
        }
    }
}