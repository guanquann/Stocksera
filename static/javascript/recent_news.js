function load_table_url() {
    tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    tr[0].querySelectorAll("th")[2].style.display = "none"
    tr[0].querySelectorAll("th")[3].style.display = "none"
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        if (td[3].innerHTML.includes("Bearish")) {
            td[3].parentElement.style.backgroundColor = "#ff000054"
        }
        else if (td[3].innerHTML.includes("Bullish")){
            td[3].parentElement.style.backgroundColor = "#00800078"
        }
        url_link = td[2].innerHTML
        td[1].innerHTML = `<a href="${url_link}" target="_blank" class="explore_sec">Explore</a>` + td[1].innerHTML
        td[2].style.display = "none"
        td[3].style.display = "none"
    }
}