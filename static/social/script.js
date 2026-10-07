document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".message").forEach((message) => {
        setTimeout(() => {
            message.style.opacity = "0";
            message.style.transition = "opacity .5s";
            setTimeout(() => message.remove(), 500);
        }, 3000);
    });
});
