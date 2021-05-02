function show_graph(elem) {
    var parent_div = elem.parentElement.parentElement.childNodes
    // console.log(parent_div)
    parent_div[1].querySelectorAll("button")[0].className = "selected_btn"
    parent_div[1].querySelectorAll("button")[1].className = ""
    parent_div[5].style.display = "none";
    parent_div[3].style.removeProperty("display");
}

function show_table(elem) {
    var parent_div = elem.parentElement.parentElement.childNodes

    parent_div[1].querySelectorAll("button")[0].className = ""
    parent_div[1].querySelectorAll("button")[1].className = "selected_btn"
    parent_div[5].style.removeProperty("display");
    parent_div[3].style.display = "none";

    elem.className = "selected_btn";
}