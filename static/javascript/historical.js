function display_data() {
    var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    var historical_data = document.getElementsByTagName("table")[0]

    var input_row = historical_data.insertRow(1);
    var input_day = input_row.insertCell(0);
    var input_date = input_row.insertCell(1);
    var input_open = input_row.insertCell(2);
    var input_high = input_row.insertCell(3);
    var input_low = input_row.insertCell(4);
    var input_close = input_row.insertCell(5);
    var input_vol = input_row.insertCell(6);
    var input_price_change = input_row.insertCell(7);
    var input_amplitude = input_row.insertCell(8);
    var input_vol_change = input_row.insertCell(9);

    input_day.innerHTML = "<input placeholder='Search: ' onkeyup='searchColumn(this, 0)'>"
    input_date.innerHTML = "<input placeholder='Search: ' onkeyup='searchColumn(this, 1)'>"
    input_open.innerHTML = "<input placeholder='Search: ' onkeyup='searchColumn(this, 2)'>"
    input_high.innerHTML = "<input placeholder='Search: ' onkeyup='searchColumn(this, 3)'>"
    input_low.innerHTML = "<input placeholder='Search: ' onkeyup='searchColumn(this, 4)'>"
    input_close.innerHTML = "<input placeholder='Search: ' onkeyup='searchColumn(this, 5)'>"
    input_vol.innerHTML = "<input placeholder='Search: ' onkeyup='searchColumn(this, 6)'>"
    input_price_change.innerHTML = "<input placeholder='Search: ' onkeyup='searchColumn(this, 7)'>"
    input_amplitude.innerHTML = "<input placeholder='Search: ' onkeyup='searchColumn(this, 8)'>"
    input_vol_change.innerHTML = "<input placeholder='Search: ' onkeyup='searchColumn(this, 9)'>"

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

    for (i=2; i<historical_data.length-1; i++) {
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

        var vol_diff = Number(td[5].innerHTML) - Number(prev_td[5].innerHTML);
        var vol_percent_diff = Math.round((vol_diff / Number(prev_td[5].innerHTML)) * 10000) / 100
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

const searchColumn = (elem, col_num) =>{
let filter = elem.value.toUpperCase();
let table = document.getElementsByTagName("table")[0];
let tr = table.getElementsByTagName('tr');
for (var i = 2; i < tr.length; i++){
    let td = tr[i].getElementsByTagName('td')[col_num];
    if(td) {
        let textValue = td.textContent || td.innerHTML;
        if (textValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display="";
        }
        else {
            tr[i].style.display="none";
            }
        }
    }
}