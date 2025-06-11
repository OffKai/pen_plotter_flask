addEventListener("DOMContentLoaded", () => {
    let button = document.getElementById("landing-canvas-button");
    if (button) {
        button.addEventListener("click", () => {
            button.blur();
            window.location = "/canvas";
        })
    }
})