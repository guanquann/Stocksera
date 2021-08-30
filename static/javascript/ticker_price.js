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