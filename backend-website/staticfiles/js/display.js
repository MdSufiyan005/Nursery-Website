document.addEventListener('DOMContentLoaded', function () {
    // ====== Search Suggestions ======
    const searchInput = document.getElementById('search');
    const suggestionsBox = document.getElementById('suggestions');
    const searchForm = document.getElementById('searchForm');

    searchInput?.addEventListener('keyup', (e) => {
        const query = searchInput.value.trim();

        if (query.length === 0) {
            suggestionsBox.innerHTML = '';
            return;
        }

        if (e.key === 'Enter') {
            searchForm.submit();
            return;
        }

        fetch(`/ajax/suggestions/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                suggestionsBox.innerHTML = '';
                data.results.forEach(item => {
                    const div = document.createElement('div');
                    div.textContent = item;
                    div.classList.add('suggestion');
                    div.addEventListener('click', () => {
                        searchInput.value = item;
                        suggestionsBox.innerHTML = '';
                        searchForm.submit();
                    });
                    suggestionsBox.appendChild(div);
                });
            });
    });

    // ====== Price Slider ======
    const slider = document.getElementById('price-slider');
    if (slider && window.noUiSlider) {
        const minStart = parseInt("{{ min_price|default_if_none:real_min_price|default_if_none:0 }}") || 0;
        const maxStart = parseInt("{{ max_price|default_if_none:real_max_price|default_if_none:1000 }}") || 1000;
        const realMin = parseInt("{{ real_min_price|default_if_none:0 }}") || 0;
        const realMax = parseInt("{{ real_max_price|default_if_none:1000 }}") || 1000;

        noUiSlider.create(slider, {
            start: [minStart, maxStart],
            connect: true,
            step: 1,
            range: {
                min: realMin,
                max: realMax
            },
            tooltips: [true, true],
            format: {
                to: value => Math.round(value),
                from: value => Number(value)
            }
        });

        const minInput = document.getElementById('min_price_input');
        const maxInput = document.getElementById('max_price_input');
        const minDisplay = document.getElementById('min_price_display');
        const maxDisplay = document.getElementById('max_price_display');

        slider.noUiSlider.on('update', function (values) {
            const [min, max] = values;
            if (minInput) minInput.value = min;
            if (maxInput) maxInput.value = max;
            if (minDisplay) minDisplay.textContent = min;
            if (maxDisplay) maxDisplay.textContent = max;
        });
    }

    // ====== Filter Section Buttons ======
    const categoryBtn = document.getElementById("categoryToggle");
    const sortBtn = document.getElementById("sortToggle");
    const priceBtn = document.getElementById("priceToggle");

    const categoryDropdown = document.getElementById("categoryDropdown");
    const sortDropdown = document.getElementById("sortDropdown");
    const priceSliderWrap = document.getElementById("priceSliderWrap");

    function toggleElement(elem) {
        if (!elem) return;
        elem.style.display = (elem.style.display === "none" || !elem.style.display)
            ? "block"
            : "none";
    }

    categoryBtn?.addEventListener("click", () => {
        toggleElement(categoryDropdown);
        sortDropdown.style.display = "none";
        priceSliderWrap.style.display = "none";
    });

    sortBtn?.addEventListener("click", () => {
        toggleElement(sortDropdown);
        categoryDropdown.style.display = "none";
        priceSliderWrap.style.display = "none";
    });

    priceBtn?.addEventListener("click", () => {
        toggleElement(priceSliderWrap);
        categoryDropdown.style.display = "none";
        sortDropdown.style.display = "none";
    });

    // ====== Price Range Toggle ======
    const priceToggleBtn = document.getElementById("priceToggleBtn");
    const priceDropdown = document.getElementById("priceDropdown");

    priceToggleBtn?.addEventListener("click", function () {
        if (priceDropdown) {
            const isHidden = priceDropdown.style.display === "none" || !priceDropdown.style.display;
            priceDropdown.style.display = isHidden ? "block" : "none";
            priceToggleBtn.textContent = isHidden ? "Price Range ▲" : "Price Range ▼";
        }
    });


    // Auto-submit on dropdown change
document.getElementById('categorySelect')?.addEventListener('change', () => {
    document.getElementById('filterForm')?.submit();
});
document.getElementById('sortSelect')?.addEventListener('change', () => {
    document.getElementById('filterForm')?.submit();
});

// Auto-submit on slider change
if (slider && window.noUiSlider) {
    slider.noUiSlider.on('change', function (values) {
        const [min, max] = values;
        if (minInput) minInput.value = min;
        if (maxInput) maxInput.value = max;
        document.getElementById('filterForm')?.submit();
    });
}


    });

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("search");
  const dataTag = document.getElementById("plant-names");

  if (!dataTag || !searchInput) return;

  const plantNames = JSON.parse(dataTag.textContent);

  let i = 0, j = 0;
  let isDeleting = false;
  let showCursor = true; // Cursor toggle

  function type() {
    if (!plantNames.length) return;

    const fullText = plantNames[i];
    const currentText = isDeleting
      ? fullText.substring(0, j--)
      : fullText.substring(0, j++);

    // Add blinking cursor
    searchInput.placeholder = currentText + (showCursor ? "|" : "");

    if (!isDeleting && j === fullText.length + 1) {
      isDeleting = true;
      setTimeout(type, 1000);
      return;
    }

    if (isDeleting && j === 0) {
      isDeleting = false;
      i = (i + 1) % plantNames.length;
    }

    // Toggle cursor on every frame
    showCursor = !showCursor;

    setTimeout(type, isDeleting ? 50 : 100);
  }

  type();
});
