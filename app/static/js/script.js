document.addEventListener('DOMContentLoaded', function () {
  /*
   Theme Toggle Functionality using Font Awesome Icons
  */
  const toggle = document.getElementById('theme-toggle');

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
     Buying/Selling Selection Logic
  */
  const buyOption = document.getElementById("buy-option");
  const sellOption = document.getElementById("sell-option");
  const buyLabel = buyOption.parentElement;
  const sellLabel = sellOption.parentElement;
  const inputs = document.querySelectorAll('#housing-form input');

  let selectedPurpose = localStorage.getItem("selectedPurpose");

  function updateSelection(selectedValue) {
    selectedPurpose = selectedValue;
    localStorage.setItem("selectedPurpose", selectedValue);

    // Highlight selected option
    if (selectedValue === "buy") {
      buyLabel.classList.add("selected");
      sellLabel.classList.remove("selected");
    } else if (selectedValue === "sell") {
      sellLabel.classList.add("selected");
      buyLabel.classList.remove("selected");
    }

    //  Clear form when user switches between Buying and Selling
    clearForm();

    // Remove any "Select purpose" error messages
    document.querySelectorAll('.purpose-error').forEach(error => error.remove());
  }

  buyOption.addEventListener("change", () => updateSelection("buy"));
  sellOption.addEventListener("change", () => updateSelection("sell"));

  function resetOptions() {
    if (selectedPurpose === "buy" || selectedPurpose === "sell") {
      document.getElementById(`${selectedPurpose}-option`).checked = true;
      document.getElementById(`${selectedPurpose}-option`).parentElement.classList.add("selected");
    }
  }

  resetOptions();

  /*
     Clear Form Function - Called when user switches between Buying and Selling
  */
  function clearForm() {
    inputs.forEach(input => {
      input.value = ""; // Reset input values
      input.classList.remove("invalid"); // Remove red border if any
    });

    // Remove all validation error messages
    document.querySelectorAll('.error-msg, .purpose-error').forEach(error => error.remove());

    // Disable the "Predict" button (until valid input is entered again)
    predictBtn.disabled = true;
  }

  /*
     Prevent Typing Without Selecting a Purpose (Show Error Below Input)
  */
  inputs.forEach(input => {
    input.addEventListener('focus', function () {
      if (!selectedPurpose) {
        let errorMsgEl = this.nextElementSibling;

        if (!errorMsgEl || !errorMsgEl.classList.contains('purpose-error')) {
          errorMsgEl = document.createElement("div");
          errorMsgEl.className = "purpose-error";
          errorMsgEl.style.color = "red";
          errorMsgEl.style.fontSize = "0.9em";
          errorMsgEl.style.marginTop = "5px";
          errorMsgEl.textContent = "Hey there! Please choose whether you're buying or selling(above) before entering details.";
          this.parentNode.insertBefore(errorMsgEl, this.nextSibling);
        }

        this.blur(); // Prevent typing by removing focus
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

  /*
     Function to Validate a Single Input Field
  */
  function validateField(input) {
    const fieldName = input.name;
    const value = parseFloat(input.value);
    const rule = validationRules[fieldName];
    let errorMsgEl = input.nextElementSibling;

    if (!errorMsgEl || !errorMsgEl.classList.contains('error-msg')) {
      errorMsgEl = document.createElement("div");
      errorMsgEl.className = "error-msg";
      errorMsgEl.style.color = "red";
      errorMsgEl.style.fontSize = "0.9em";
      errorMsgEl.style.marginTop = "5px";
      input.parentNode.insertBefore(errorMsgEl, input.nextSibling);
    }

    if (input.value.trim() === "" || isNaN(value)) {
      errorMsgEl.textContent = "This field is required.";
      input.classList.add("invalid");
      return false;
    }

    if (value < rule.min || value > rule.max) {
      errorMsgEl.textContent = rule.error;
      input.classList.add("invalid");
      return false;
    }

    errorMsgEl.textContent = "";
    input.classList.remove("invalid");
    return true;
  }

  /*
     Function to Check Overall Form Validity and Enable/Disable Predict Button
  */
  function checkFormValidity() {
    let isValid = true;
    inputs.forEach(input => {
      if (!validateField(input)) {
        isValid = false;
      }
    });
    predictBtn.disabled = !isValid;
  }

  /*
     Attach Event Listeners to Each Input for Validation
  */
  inputs.forEach(input => {
    input.addEventListener('input', function () {
      validateField(input);
      checkFormValidity();
    });
  });


  /* ===============================
     Prediction History Logic
  =============================== */
  // This flag indicates whether to show the full history or only the last 5 entries.
  let historyExpanded = false;

  function loadHistory() {
    const historyTableBody = document.querySelector('#history-table tbody');
    historyTableBody.innerHTML = "";
    const history = JSON.parse(localStorage.getItem('predictionHistory')) || [];
    
    // Reverse the history so that the most recent is first.
    const reversedHistory = history.slice().reverse();
    // Determine which items to display:
    const itemsToShow = historyExpanded ? reversedHistory : reversedHistory.slice(0, 5);
// Display the history in the table
    itemsToShow.forEach(item => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${item.sqft_living}</td>
        <td>${item.no_of_bedrooms}</td>
        <td>${item.no_of_bathrooms}</td>
        <td>${item.sqft_lot}</td>
        <td>${item.no_of_floors}</td>
        <td>${item.house_age}</td>
        <td>${item.zipcode}</td>
        <td>$${parseFloat(item.predicted_price).toLocaleString()}</td>
      `;
      historyTableBody.appendChild(tr);
    });

    // Update the toggle button text with an arrow icon
    const toggleHistoryBtn = document.getElementById('toggle-history');
    if (history.length <= 5) {
      // If history has 5 or fewer entries, hide the toggle button.
      toggleHistoryBtn.style.display = 'none';
    } else {
      toggleHistoryBtn.style.display = 'inline-block';
      toggleHistoryBtn.innerHTML = historyExpanded 
        ? 'Show Less &#9650;'   // Up arrow when expanded
        : 'Show All &#9660;';   // Down arrow when collapsed
    }
  }

  loadHistory();

  // Toggle history view when the toggle button is clicked
  document.getElementById('toggle-history').addEventListener('click', function() {
    historyExpanded = !historyExpanded;
    loadHistory();
  });

  // Clear history button
  document.getElementById('clear-history').addEventListener('click', function() {
    localStorage.removeItem('predictionHistory');
    loadHistory();
  });

  /* ===============================
     Form Submission and Prediction Result
  =============================== */
  form.addEventListener('submit', function(e) {
    e.preventDefault();

    // Collect form data
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    // Send data to Flask backend via AJAX (expects a JSON response)
    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
      // Expected result: { predicted_price, confidence_interval }
      displayResult(result, data);
      updateHistory(result.predicted_price, data);
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while predicting. Please try again.');
    });
  });

  // Display prediction result and scroll to results section
  function displayResult(result, inputData) {
    const resultSection = document.getElementById('result-section');
    const predictionMessage = document.getElementById('prediction-message');

    predictionMessage.innerHTML = `Based on the data provided, your home is estimated to be valued at <strong>$${parseFloat(result.predicted_price).toLocaleString()}</strong>.<br>
      The confidence interval for this prediction ranges between <strong>$${parseFloat(result.confidence_interval[0]).toLocaleString()}</strong> and <strong>$${parseFloat(result.confidence_interval[1]).toLocaleString()}</strong>.`;
// Add the dynamic Realtor.com link
const realtorLinkContainer = document.getElementById('realtor-link-container');
realtorLinkContainer.innerHTML = `
    <p>View properties in your area on <a href="${result.realtor_url}" target="_blank">Realtor.com</a>.</p>
`;
    // Hide the form section and show the result section
    document.getElementById('form-section').classList.add('hidden');
    resultSection.classList.remove('hidden');
    resultSection.scrollIntoView({ behavior: 'smooth' });
  }

  // Update prediction history (store in localStorage and update the table)
  function updateHistory(predicted_price, inputData) {
    const history = JSON.parse(localStorage.getItem('predictionHistory')) || [];
    history.push({
      sqft_living: inputData.sqft_living,
      no_of_bedrooms: inputData.no_of_bedrooms,
      no_of_bathrooms: inputData.no_of_bathrooms,
      sqft_lot: inputData.sqft_lot,
      no_of_floors: inputData.no_of_floors,
      house_age: inputData.house_age,
      zipcode: inputData.zipcode,
      predicted_price: parseFloat(predicted_price).toFixed(2)
    });
    localStorage.setItem('predictionHistory', JSON.stringify(history)); // Save to localStorage for persistence and load history
    // Reset to compact view (latest 5) when a new prediction is added.
    historyExpanded = false; // Reset to compact view
    loadHistory();// Reload history table
  }

  // “Back to Form” button to allow making another prediction
  document.getElementById('back-to-form').addEventListener('click', function() {
    document.getElementById('result-section').classList.add('hidden');
    document.getElementById('form-section').classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    form.reset(); // Clear form fields
    predictBtn.disabled = true;
  });
});