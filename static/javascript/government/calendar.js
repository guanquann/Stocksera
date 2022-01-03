// Adapted from https://github.com/niinpatel/calendarHTML-Javascript/blob/master/scripts.js
today = new Date();
//currentMonth = today.getMonth();
//currentYear = today.getFullYear();
selectYear = document.getElementById("year");
selectMonth = document.getElementById("month");

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

monthAndYear = document.getElementById("monthAndYear");
dates_available = document.getElementById("dates_available").innerHTML;

original_date_selected = document.getElementById("date_selected").innerHTML;
original_date_selected_split = original_date_selected.split("-")
original_date_split = original_date_selected.split("-")
originalMonth = Number(original_date_split[1]) - 1;
originalYear = Number(original_date_split[0]);
originalDate = Number(original_date_split[2]);

date_selected = document.getElementById("date_selected").innerHTML;
date_split = date_selected.split("-")
currentMonth = Number(date_split[1]) - 1;
currentYear = Number(date_split[0]);
showCalendar(currentMonth, currentYear);


function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear);
}

function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear);
}

function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    showCalendar(currentMonth, currentYear);
}

function showCalendar(month, year) {
    let firstDay = (new Date(year, month)).getDay();

    tbl = document.getElementById("calendar-body"); // body of the calendar

    // clearing all previous cells
    tbl.innerHTML = "";

    // filing data about month and in the page via DOM.
    monthAndYear.innerHTML = months[month] + " " + year;
    selectYear.value = year;
    selectMonth.value = month;

    // creating all cells
    let date = 1;
    for (let i = 0; i < 6; i++) {
        // creates a table row
        let row = document.createElement("tr");

        //creating individual cells, filing them up with data.
        for (let j = 0; j < 7; j++) {
            if (i === 0 && j < firstDay) {
                cell = document.createElement("td");
                cellText = document.createTextNode("");
                cell.appendChild(cellText);
                row.appendChild(cell);
            }
            else if (date > daysInMonth(month, year)) {
                break;
            }

            else {
                cell = document.createElement("td");
                cellText = document.createTextNode(date);
                if (date === today.getDate() && year === today.getFullYear() && month === today.getMonth()) {
                    cell.classList.add("bg-today");
                }
                if (date === originalDate && month === originalMonth && year === originalYear) {
                    cell.classList.add("bg-selected");
                }

                date_ = (date <= 9) ? "0" + date : date;
                month_ = (month <= 8) ? "0" + (month+1) : month+1;
                actual_date = `${year}-${month_}-${date_}`

                if (dates_available.includes(actual_date)) {
                    cell.classList.add("bg-info");
                }
                cell.classList.add("hoverable");
                cell.setAttribute("onclick",`get_clicked_date('${actual_date}')`);
                cell.appendChild(cellText);

                row.appendChild(cell);
                date++;
            }
        }
        tbl.appendChild(row); // appending each row into calendar body.
    }
}

// check how many days in a month code from https://dzone.com/articles/determining-number-days-month
function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}
// End of https://github.com/niinpatel/calendarHTML-Javascript/blob/master/scripts.js

function open_calendar() {
    calendar_class = document.querySelector(".calendar_div").classList
    calendar_btn = document.querySelector("#open_calendar")
    if (calendar_class.contains("hide_calendar")) {
        calendar_class.remove("hide_calendar")
        calendar_btn.innerHTML = "Hide Calendar"
    }
    else {
        calendar_class.add("hide_calendar")
        calendar_btn.innerHTML = "Open Calendar"
    }
}