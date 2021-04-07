var disclaimer_model = document.getElementById("disclaimer_model");
var contact_model = document.getElementById("contact_model");
var privacy_model = document.getElementById("privacy_model");

var disclaimer_btn = document.getElementById("disclaimer");
var contact_btn = document.getElementById("contact");
var privacy_btn = document.getElementById("privacy");

var disclaimer_span = document.getElementsByClassName("close")[0];
var contact_span = document.getElementsByClassName("close")[1];
var privacy_span = document.getElementsByClassName("close")[2];

// When the user clicks the button, open the modal 
disclaimer_btn.onclick = function() {
    disclaimer_model.style.display = "block";
}
contact_btn.onclick = function() {
    contact_model.style.display = "block";
}
privacy_btn.onclick = function() {
    privacy_model.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
disclaimer_span.onclick = function() {
    disclaimer_model.style.display = "none";
}
contact_span.onclick = function() {
    contact_model.style.display = "none";
}
privacy_span.onclick = function() {
    privacy_model.style.display = "none";
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == disclaimer_model) {
    disclaimer_model.style.display = "none";
  }

  if (event.target == contact_model) {
    contact_model.style.display = "none";
  }

  if (event.target == privacy_model) {
    privacy_model.style.display = "none";
  }
}