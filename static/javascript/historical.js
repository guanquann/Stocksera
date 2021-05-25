function display_data() {
    var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    var historical_data = document.getElementsByTagName("table")[0]
    historical_data.querySelector("tr").innerHTML = `
        <th>Day</th>
        <th>Date</th>
        <th>Open</th>
        <th>High</th>
        <th>Low</th>
        <th>Close</th>
        <th>Volume</th>
        <th>% Price Change</th>
        <th>Amplitude</th>
        <th>% Vol Change</th>`

    historical_data = historical_data.querySelectorAll("tr");
    for (i=1; i<historical_data.length-1; i++) {
        var td = historical_data[i].querySelectorAll("td");

        var prev_td = historical_data[i+1].querySelectorAll("td");

        var d = new Date(td[0].innerHTML);
        var dayName = days[d.getDay()];

        historical_data[i].innerHTML = `<td>${dayName}</td>` + historical_data[i].innerHTML

        var price_diff = td[4].innerHTML - prev_td[4].innerHTML;
        var price_percent_diff = Math.round((price_diff / prev_td[4].innerHTML) * 10000) / 100
        if (String(price_percent_diff).includes("-")) {
            historical_data[i].innerHTML += `<td style="color:red">${price_percent_diff}%</td>`
        }
        else {
            historical_data[i].innerHTML += `<td style="color:green">+${price_percent_diff}%</td>`
        }

        var amplitude = Math.round(((td[2].innerHTML - td[3].innerHTML) / td[1].innerHTML) * 10000) / 100;
        historical_data[i].innerHTML += `<td>${amplitude}%</td>`

        var vol_diff = td[5].innerHTML - prev_td[5].innerHTML;
        var vol_percent_diff = Math.round((vol_diff / prev_td[5].innerHTML) * 10000) / 100
        if (String(vol_percent_diff).includes("-")) {
            historical_data[i].innerHTML += `<td style="color:red">${vol_percent_diff}%</td>`
        }
        else {
            historical_data[i].innerHTML += `<td style="color:green">+${vol_percent_diff}%</td>`
        }
    }

    var d = new Date(historical_data[historical_data.length-1].querySelector("td").innerHTML);
    var dayName = days[d.getDay()];
    historical_data[historical_data.length-1].innerHTML = `<td>${dayName}</td>` + historical_data[i].innerHTML
    historical_data[historical_data.length-1].innerHTML += "<td></td><td></td><td></td>"
}
