document.addEventListener('DOMContentLoaded', function () {
    /*
       Theme Toggle Functionality using Font Awesome Icons
    */
    const toggle = document.getElementById('theme-toggle');
  
    // Determine saved theme or use system preference if none saved
    let theme = localStorage.getItem('theme');
    if (!theme) {
      theme = (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
        ? 'dark'
        : 'light';
    }
    setTheme(theme);
  
    function setTheme(theme) {
      if (theme === 'dark') {
        document.documentElement.classList.add('dark-mode');
        document.documentElement.classList.remove('light-mode');
        toggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
      } else {
        document.documentElement.classList.add('light-mode');
        document.documentElement.classList.remove('dark-mode');
        toggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
      }
      localStorage.setItem('theme', theme);
    }
  
    toggle.addEventListener('click', function () {
      setTheme(document.documentElement.classList.contains('dark-mode') ? 'light' : 'dark');
    });
  
    /* 
      🚀 Buying/Selling Selection Logic (Enabling Input Fields)
    */
    const buyOption = document.getElementById("buy-option");
    const sellOption = document.getElementById("sell-option");
    const buyLabel = buyOption.parentElement;
    const sellLabel = sellOption.parentElement;
    const inputs = document.querySelectorAll('#housing-form input'); // Get all input fields
  
    function enableInputs() {
      inputs.forEach(input => {
        input.disabled = false;
      });
    }
  
    function disableInputs() {
      inputs.forEach(input => {
        input.disabled = true;
      });
    }
  
    function updateSelection(selectedValue) {
      if (selectedValue === "buy") {
        buyLabel.classList.add("selected");
        sellLabel.classList.remove("selected");
      } else if (selectedValue === "sell") {
        sellLabel.classList.add("selected");
        buyLabel.classList.remove("selected");
      }
  
      localStorage.setItem("selectedPurpose", selectedValue);
      enableInputs(); // Enable form fields once a selection is made
    }
  
    buyOption.addEventListener("change", () => updateSelection("buy"));
    sellOption.addEventListener("change", () => updateSelection("sell"));
  
    function resetOptions() {
      buyLabel.classList.remove("selected");
      sellLabel.classList.remove("selected");
  
      const savedPurpose = localStorage.getItem("selectedPurpose");
      if (savedPurpose === "buy" || savedPurpose === "sell") {
        document.getElementById(`${savedPurpose}-option`).checked = true;
        document.getElementById(`${savedPurpose}-option`).parentElement.classList.add("selected");
        enableInputs(); // Enable inputs if user previously selected a purpose
      } else {
        disableInputs(); // Keep inputs disabled until selection is made
      }
    }
  
    resetOptions();
  
    /* 
      🚨 Prevent Input Without Selecting a Purpose
    */
    inputs.forEach(input => {
      input.addEventListener('focus', function () {
        const selectedPurpose = localStorage.getItem("selectedPurpose");
        if (!selectedPurpose) {
          alert("Please select a purpose (Buying or Selling) first!");
          input.blur(); // Remove focus to prevent entry
        }
      });
    });
  
    /* 
       Housing Form and Prediction Logic
    */
    const form = document.getElementById('housing-form');
    const predictBtn = document.getElementById('predict-btn');
  
    const validationRules = {
      sqft_living: { min: 200, max: 10000, error: "Living area must be between 200 and 10,000 sqft." },
      no_of_bedrooms: { min: 1, max: 25, error: "Number of bedrooms must be between 1 and 25." },
      no_of_bathrooms: { min: 1, max: 15, error: "Number of bathrooms must be between 1 and 15." },
      sqft_lot: { min: 500, max: 50000, error: "Lot size must be between 500 and 50,000 sqft." },
      no_of_floors: { min: 0, max: 10, error: "Floors must be between 0 and 10." },
      house_age: { min: 0, max: 150, error: "House age must be between 0 and 150 years." },
      zipcode: { min: 98001, max: 99001, error: "Invalid ZIP code. Must be between 98001 and 99001." }
    };
  
    function validateField(input) {
      const fieldName = input.name;
      const value = parseFloat(input.value);
      const rule = validationRules[fieldName];
      const errorMsgEl = input.nextElementSibling;
  
      if (input.value.trim() === "" || isNaN(value)) {
        errorMsgEl.textContent = "This field is required.";
        errorMsgEl.style.display = "block";
        input.classList.add("invalid");
        return false;
      }
  
      if (value < rule.min || value > rule.max) {
        errorMsgEl.textContent = rule.error;
        errorMsgEl.style.display = "block";
        input.classList.add("invalid");
        return false;
      }
  
      errorMsgEl.textContent = "";
      errorMsgEl.style.display = "none";
      input.classList.remove("invalid");
      return true;
    }
  
    function checkFormValidity() {
      let isValid = true;
      inputs.forEach(input => {
        if (!validateField(input)) {
          isValid = false;
        }
      });
      predictBtn.disabled = !isValid;
    }
  
    inputs.forEach(input => {
      input.addEventListener('input', function () {
        validateField(input);
        checkFormValidity();
      });
    });
  
  });
  