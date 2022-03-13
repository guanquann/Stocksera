function normalise_num(table_cell) {
    data_value = table_cell.innerHTML;
    if (data_value < 1000000000) {
        table_cell.innerHTML = String(Math.round(data_value / 10000, 2)) / 100 + "M"
    }
    else if (data_value >= 1000000000) {
        table_cell.innerHTML = String(Math.round(data_value / 10000000, 2)) / 100 + "B"
    }
}

function get_dates(duration) {
    var d = new Date();
    d.setDate(d.getDate() + duration);
    var dd = d.getDate();
    if (dd <= 9) {
        dd = "0" + dd
    }
    var mm = d.getMonth() + 1;
    if (mm <= 9) {
        mm = "0" + mm
    }
    var yyyy = d.getFullYear();
    var date_threshold = yyyy + "-" + mm + "-" + dd;
    return date_threshold
}

function load_table() {
    var trs = document.querySelectorAll("table tr");

    for (i=1; i<trs.length; i++) {
        tds = trs[i].querySelectorAll("td")
        tds[2].innerHTML = `<b><a href="/ticker/?quote=${tds[2].innerHTML}" target="_blank">${tds[2].innerHTML}</a></b>`
        normalise_num(tds[5])
        normalise_num(tds[6])
        normalise_num(tds[7])
    }

    today_date = new Date()
    day = today_date.getDate()
    month = today_date.getMonth() + 1
    if (day < 10) {
        day = "0" + day
    }
    if (month < 10) {
        month = "0" + month
    }
    year = today_date.getFullYear()
    today_date = year + "-" + month + "-" + day

    for (i=0; i<=21; i++) {
        date_to_append = get_dates(i)
        document.getElementById("date_filter").innerHTML += `<option value="${date_to_append}">${date_to_append}</option>`
    }
}

const searchTicker = (elem) =>{
    let filter = elem.value.toUpperCase();
    var trs = document.querySelectorAll("table tr");
    for (i=1; i<trs.length; i++) {
        tds = trs[i].querySelectorAll("td")
        ticker = tds[2].textContent.toUpperCase();
        if (ticker.indexOf(filter) > -1) {
            trs[i].classList.remove("ticker_filter")
        }
        else {
            trs[i].classList.add("ticker_filter")
        }

    }
}

function mkt_cap_filter(self, threshold) {
    threshold = self.value
    if (threshold == ">$1B") {
        threshold = 1
    }
    else if (threshold == ">$5B") {
        threshold = 5
    }
    else if (threshold == ">$10B") {
        threshold = 10
    }
    else if (threshold == ">$20B") {
        threshold = 20
    }
    else if (threshold == ">$50B") {
        threshold = 50
    }

    var trs = document.querySelectorAll("table tr");

    for (i=1; i<trs.length; i++) {
        tds = trs[i].querySelectorAll("td")

        mkt_cap = tds[7].innerHTML;
        mkt_num_number = mkt_cap.split("M")[0].split("B")[0]
        if (threshold == "All") {
            trs[i].classList.remove("mkt_cap_filter")
        }
        else if (threshold == "<$1B" & mkt_cap.includes("M")) {
            trs[i].classList.remove("mkt_cap_filter")
        }
        else if (mkt_num_number < threshold || mkt_cap.includes("M") || mkt_num_number == "N/A") {
            trs[i].classList.add("mkt_cap_filter")
        }
        else {
            trs[i].classList.remove("mkt_cap_filter")
        }
    }
}

function date_filter(elem) {
    var selected_date = elem.value;
    var trs = document.querySelectorAll("table tr");

    for (i=1; i<trs.length; i++) {
        tds = trs[i].querySelectorAll("td")
        if (selected_date == "All") {
            trs[i].classList.remove("date_filter")
        }
        else if (tds[0].innerHTML == selected_date) {
            trs[i].classList.remove("date_filter")
        }
        else {
            trs[i].classList.add("date_filter")
        }
    }
}

function time_filter(elem) {
    var selected_time = elem.value;
    var trs = document.querySelectorAll("table tr");

    for (i=1; i<trs.length; i++) {
        tds = trs[i].querySelectorAll("td")
        if (selected_time == "All") {
            trs[i].classList.remove("time_filter")
        }
        else if (tds[1].innerHTML == selected_time) {
            trs[i].classList.remove("time_filter")
        }
        else {
            trs[i].classList.add("time_filter")
        }
    }
}
