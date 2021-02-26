function display_data() {
    if (document.getElementsByName("ticker")[0].value != "") {
        document.getElementsByClassName("ticker_summary")[0].style.removeProperty("display");
        document.getElementsByClassName("chart-container")[0].style.removeProperty("display");

        document.getElementById("img_div").style = "width:9%;display:inline-block;";
        document.getElementById("ticker_intro").style = "display:inline-block;";
        document.getElementById("days_btn").style.removeProperty("display");
        document.getElementById("ticker_table").style.removeProperty("display");
    }
}