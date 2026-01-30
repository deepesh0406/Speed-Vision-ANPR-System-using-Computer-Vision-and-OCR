const themeSwitch = document.getElementById('theme-switch')
const body = document.body;

themeSwitch.addEventListener("click", () => {
    body.classList.toggle("darkmode");

    darkmode = localStorage.getItem('darkmode')
    if (body.classList.contains("darkmode")) 
        localStorage.setItem("theme", "darkmode");
    else 
        localStorage.setItem("theme", "lightmode");
})

if (localStorage.getItem("theme") === "darkmode") {
    body.classList.add("darkmode");
} else {
    body.classList.add("lightmode")
}