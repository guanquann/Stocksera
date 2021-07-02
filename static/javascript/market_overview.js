function select_selector(index) {
    var selectors = document.getElementsByClassName("selector");
    var widgets = document.getElementsByClassName("chart-container");

    for (i=0; i<selectors.length; i++) {
        selectors[i].classList.remove("selected");
        widgets[i].style.display = "none"
    }
    selectors[index].classList.add("selected");
    widgets[index].style.removeProperty("display")
}