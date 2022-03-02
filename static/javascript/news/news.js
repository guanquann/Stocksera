function load_table() {
    trs = document.querySelectorAll("table tr");
    for (i=1; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        td[2].innerHTML = `<a href="${td[2].innerHTML}" target="_blank" class="explore_news">Explore</a>`
        td[3].style.display = "none"
    }
    trs[0].querySelectorAll("th")[3].style.display = "none"
}

function filter_table(elem) {
    trs = document.querySelectorAll("table tr");
    to_filter = elem.value
    for (i=1; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        if (td[3].innerHTML == to_filter || to_filter == "all") {
            trs[i].style.display = ""
        }
        else {
            trs[i].style.display = "none"
        }
    }
}

//function change_nav(elem) {
//    more_info_divs = document.querySelectorAll(".more_info_div");
//    for (i=0; i<more_info_divs.length; i++) {
//        more_info_divs[i].classList.remove("current_link")
//    }
//    elem.classList.add("current_link")
//}