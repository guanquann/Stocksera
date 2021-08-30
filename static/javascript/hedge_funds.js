function load_page_num() {
    var current_pg_num = Number(document.getElementById("page_num").value);
    var total_pages = Number(document.getElementById("total_pages").value);

    if (current_pg_num >= 1 & total_pages > 1) {
        var total_code = '<div class="page_num" onclick="get_previous_pg()">&#9665;</div>';
        if (total_pages > 4) {
            last_2 = current_pg_num - 2;
            if (last_2 >= 1) {
                total_code += `<div class="page_num" onclick="update_pg_num(this);">1</div>`
            }
            else {
                total_code += `<div class="page_num" onclick="update_pg_num(this);">${total_pages-1}</div>`
            }

            last_1 = current_pg_num - 1;
            if (last_1 >= 1) {
                total_code += `<div class="page_num" onclick="update_pg_num(this);">${last_1}</div>`
            }
            else {
                total_code += `<div class="page_num" onclick="update_pg_num(this);">${total_pages}</div>`
            }
        }
        total_code += `<div class="page_num selected_page" onclick="update_pg_num(this);">${current_pg_num}</div>`

        forward_1 = current_pg_num + 1;
        if (forward_1 <= total_pages) {
            total_code += `<div class="page_num" onclick="update_pg_num(this);">${forward_1}</div>`
        }
        else {
            total_code += `<div class="page_num" onclick="update_pg_num(this);">${forward_1-total_pages}</div>`
        }

        forward_2 = current_pg_num + 2;
        if (forward_2 <= total_pages) {
            total_code += `<div class="page_num" onclick="update_pg_num(this);">${forward_2}</div>`
        }
        else {
            total_code += `<div class="page_num" onclick="update_pg_num(this);">${forward_2-total_pages}</div>`
        }

        total_code += '<div class="page_num" onclick="get_next_pg()">&#9655;</div>'
    }
    else {
        total_code = `<div class="page_num" onclick="update_pg_num(this);">1</div>`
    }
    document.getElementsByClassName("page_section")[0].innerHTML = total_code;
}

function update_pg_num(elem) {
    document.getElementById("page_num").innerHTML = elem.innerHTML;
    document.getElementById("page_num").setAttribute('value', elem.innerHTML);
    document.getElementById("form").submit();
}

function get_previous_pg() {
    var current = Number(document.getElementsByClassName("selected_page")[0].innerHTML)
    if (current == 1) {
        current = Number(document.getElementById("total_pages").value);
    }
    else {
        current -= 1
    }
    document.getElementById("page_num").innerHTML = current;
    document.getElementById("page_num").setAttribute('value', current);
    document.getElementById("form").submit();
}

function get_next_pg() {
    var current = Number(document.getElementsByClassName("selected_page")[0].innerHTML)
    if (current == Number(document.getElementById("total_pages").value)) {
        current = 1;
    }
    else {
        current += 1
    }
    document.getElementById("page_num").innerHTML = current;
    document.getElementById("page_num").setAttribute('value', current);
    document.getElementById("form").submit();
}