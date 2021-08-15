function display_data() {
    var error_msg_class = document.getElementById("error_msg").className;
    if (error_msg_class == "instructions error_true") {
        document.getElementById("error_msg").style.removeProperty("display");
    }

    else {
        document.getElementsByClassName("ticker_summary")[0].style.removeProperty("display");
        document.getElementsByClassName("tradingview-widget-container")[0].style.removeProperty("display");

        if (document.getElementById("img_div") != null) {
            document.getElementById("img_div").style.removeProperty("display");
        }

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
    height = elem.contentWindow.document.body.scrollHeight
    elem.style.height = height + 'px';
}

function to_remove(elem, text) {
    parent = elem.parentElement
    elem.remove()
    parent.innerHTML = `<button type="button" name="quote" class="show_more_btn" onclick="to_remove(this, '${text}')">${text}</button>`
    var more_details = document.getElementsByClassName("more_details");
    var show_more_btn = document.getElementsByClassName("show_more_btn");
    for (i=0; i<more_details.length; i++) {
        more_details[i].style.display = "none"
        show_more_btn[i].classList.remove("selected")
    }
    document.getElementsByName(text)[0].style.removeProperty("display")
    parent.firstChild.classList.add("selected")
}