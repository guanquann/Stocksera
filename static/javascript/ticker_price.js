function expand_iframe(elem) {
    height = elem.contentWindow.document.body.scrollHeight
    elem.style.height = height + 'px';
}

function get_ssr() {
    low_price = document.getElementById("low").innerHTML.replace("$", "").split(": ")[1]
    previous_close = document.getElementById("previous_close").innerHTML.replace("$", "").split(": ")[1]
    if (isNaN(low_price) == false & isNaN(previous_close) == false) {
        difference = previous_close - low_price
        percent_diff = difference / previous_close
        if (percent_diff >= 0.10) {
            document.getElementById("ssr_msg").innerHTML = "<div class='positive_price'>SSR On</div>"
        }
        else {
            document.getElementById("ssr_msg").innerHTML = "<div class='negative_price'>SSR Off</div>"
        }
    }
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

function submit_onload(elem) {
    if (elem == "") {
        document.getElementsByClassName('show_more_btn')[0].form.submit();
    }
}