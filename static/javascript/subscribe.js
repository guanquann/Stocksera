function change_freq(freq) {
    document.getElementsByName("frequency")[0].value = freq
    for (i=0; i<2; i++) {
        document.getElementsByClassName("frequency")[i].classList.remove("selected")
    }
    document.getElementById(freq).classList.add("selected")
}

function get_freq(freq) {
    document.getElementById(freq).classList.add("selected")
}