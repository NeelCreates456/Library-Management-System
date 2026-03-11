// CLOCK FUNCTION

function updateTime(){

let now = new Date();

let date = now.toLocaleDateString();
let time = now.toLocaleTimeString();

document.getElementById("datetime").innerHTML =
date + " | " + time;

}

setInterval(updateTime,1000);

// SEARCH FUNCTION
const searchInput = document.getElementById("searchInput");

if(searchInput){
searchInput.addEventListener("keyup", function(){

let value = this.value.toLowerCase();
let books = document.querySelectorAll(".book-card");

books.forEach(function(book){

let title = book.getAttribute("data-title").toLowerCase();

if(title.includes(value)){
book.style.display = "";
}else{
book.style.display = "none";
}

});

});
}