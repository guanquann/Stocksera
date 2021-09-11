function load_table_url() {
    tr = document.getElementsByTagName("table")[0].querySelectorAll("tr");
    tr[0].querySelectorAll("th")[3].style.display = "none"
    for (i=1; i<tr.length; i++) {
        td = tr[i].querySelectorAll("td")
        url_link = td[3].innerHTML
        td[1].innerHTML = `<a href="${url_link}" target="_blank" class="explore_sec">Explore</a>` + td[1].innerHTML
        td[3].style.display = "none"
    }
}