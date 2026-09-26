const display = document.getElementById("display");
const errorMessage = document.getElementById("error");

document.querySelectorAll("[data-value]").forEach((button) => {
button.addEventListener("click", () => {
display.value += button.dataset.value;
errorMessage.textContent = "";
});
});

document.querySelector('[data-action="clear"]').addEventListener("click", () => {
display.value = "";
errorMessage.textContent = "";
});

document.querySelector('[data-action="calculate"]').addEventListener("click", calculate);

async function calculate() {
const expression = display.value.trim();

if (!expression) {
    return;
}

try {
    const response = await fetch("/api/calculate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ expression })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Calculation failed");
    }

    display.value = data.result;
} catch (error) {
    errorMessage.textContent = error.message;
}


}

document.addEventListener("keydown", (event) => {
if (event.key === "Enter") {
calculate();
return;
}

if (event.key === "Escape") {
    display.value = "";
    errorMessage.textContent = "";
}

const allowed = "0123456789+-*/().";

if (allowed.includes(event.key)) {
    display.value += event.key;
}


});