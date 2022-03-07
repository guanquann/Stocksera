function load_table() {
    trs = document.querySelectorAll("table tr");
    for (i=1; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        td[1].innerHTML = `<span class="${td[4].innerHTML} section">${td[4].innerHTML}</span>` + `<span class="news_source section">${td[2].innerHTML}</span>` + td[1].innerHTML
        td[3].innerHTML = `<a href="${td[3].innerHTML}" target="_blank" class="explore_news">Explore</a>`
        td[2].style.display = "none"
        td[4].style.display = "none"
    }
    trs[0].querySelectorAll("th")[2].style.display = "none"
    trs[0].querySelectorAll("th")[4].style.display = "none"
}

function filter_table(elem) {
    trs = document.querySelectorAll("table tr");
    to_filter = elem.value
    for (i=1; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        if (td[4].innerHTML == to_filter || to_filter == "all") {
            trs[i].style.display = ""
        }
        else {
            trs[i].style.display = "none"
        }
    }
}
