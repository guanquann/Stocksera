function load_heatmap() {
    var trs = document.querySelector("table").querySelectorAll("tr")
    for (i=0; i<trs.length; i++) {
        td = trs[i].querySelectorAll("td")
        for (k=0; k<td.length; k++) {
            console.log(td[k].innerHTML)
            const value = td[k].innerHTML
            if (value != "-") {
                const l = 55 - (value * 45);
                const textColor = l < 60 ? 'white' : '#000';
                td[k].style.backgroundColor = 'hsl(10, 70%, ' + l + '%)'
                td[k].style.color = textColor
            }
        }
    }
}
