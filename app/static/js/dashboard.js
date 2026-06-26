document.addEventListener('DOMContentLoaded', function() {
    const refreshForm = document.querySelector(".refresh-form");

    if (refreshForm) {
        refreshForm.addEventListener("submit", function(event) {
            const confirmed =confirm(
                "Refresh deals now? This will scrape the configured source again."
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    }

    const maxPriceInput = document.querySelector("#max-price");

    if (maxPriceInput) {
        maxPriceInput.addEventListener("input", function() {
            if (Number(maxPriceInput.value) < 0) {
                maxPriceInput.value = "";
                alert("Price cannot be negative. Please enter a valid value.");
            }
        });
    }
});