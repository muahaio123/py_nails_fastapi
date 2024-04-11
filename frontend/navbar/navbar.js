// Get the modal
var workModal = document.getElementById("newWorkModal");
// Get the button that opens the modal
var workBtn = document.getElementById("newWorkBtn");
// Get the button that opens the modal
var closeSpan = document.getElementById("closeSpan");

// When the user clicks the button, open the modal 
workBtn.onclick = function() {
    workModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
closeSpan.onclick = function() {
    workModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == workModal) {
        workModal.style.display = "none";
    }
}