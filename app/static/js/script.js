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
const form = document.getElementById('housing-form');
const predictBtn = document.getElementById('predict-btn');

let selectedPurpose = localStorage.getItem("selectedPurpose") || "";

// Function to update the selected purpose
function updateSelection(selectedValue) {
  console.log(`Updating selection to: ${selectedValue}`);
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

  // Clear form when user switches between Buying and Selling
  clearForm();

  // Remove any "Select purpose" error messages
  document.querySelectorAll('.purpose-error').forEach(error => error.remove());
}

// Event listeners for the radio buttons
buyOption.addEventListener("change", () => updateSelection("buy"));
sellOption.addEventListener("change", () => updateSelection("sell"));

// Function to reset options based on stored value
function resetOptions() {
  if (selectedPurpose === "buy" || selectedPurpose === "sell") {
    document.getElementById(`${selectedPurpose}-option`).checked = true;
    document.getElementById(`${selectedPurpose}-option`).parentElement.classList.add("selected");
  }
}

// Call resetOptions on load
resetOptions();

/*
     Clear Form Function - Called when user switches between Buying and Selling
*/
function clearForm() {
  console.log("Clearing form inputs...");
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
      console.log("Purpose not selected. Showing error message.");
      let errorMsgEl = this.nextElementSibling;

      if (!errorMsgEl || !errorMsgEl.classList.contains('purpose-error')) {
        errorMsgEl = document.createElement("div");
        errorMsgEl.className = "purpose-error";
        errorMsgEl.style.color = "red";
        errorMsgEl.style.fontSize = "0.9em";
        errorMsgEl.style.marginTop = "5px";
        errorMsgEl.textContent = "Hey there! Please choose whether you're buying or selling (above) before entering details.";
        this.parentNode.insertBefore(errorMsgEl, this.nextSibling);
      }

      this.blur(); // Prevent typing by removing focus
    }
  });
});

/*
     Housing Form and Prediction Logic
*/
const validationRules = {
  sqft_living: { min: 200, max: 10000, error: "Living area must be between 200 and 10,000 sqft." },
  no_of_bedrooms: { min: 1, max: 25, error: "Number of bedrooms must be between 1 and 25." },
  no_of_bathrooms: { min: 1, max: 15, error: "Number of bathrooms must be between 1 and 15." },
  sqft_lot: { min: 500, max: 50000, error: "Lot size must be between 500 and 50,000 sqft." },
  no_of_floors: { min: 0, max: 10, error: "Floors must be between 0 and 10." },
  house_age: { min: 0, max: 150, error: "House age must be between 0 and 150 years." },
  zipcode: { min: 98001, max: 99001, error: "Invalid ZIP code. Must be between 98001 and 99001." }
};

// Function to validate a single input field
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

// Function to check overall form validity and enable/disable predict button
function checkFormValidity() {
  let isValid = true;
  inputs.forEach(input => {
    if (!validateField(input)) {
      isValid = false;
    }
  });
  predictBtn.disabled = !isValid || !selectedPurpose;  // Disable if form is invalid or purpose is not selected
}

// Attach event listeners to each input for validation
inputs.forEach(input => {
  input.addEventListener('input', function () {
    validateField(input);
    checkFormValidity();
  });
});

/*
     Form Submission and Prediction Logic
*/
predictBtn.addEventListener("click", function (event) {
  event.preventDefault(); // Prevent default form submission
  console.log("Predict button clicked. Starting form submission...");

  if (!selectedPurpose) {
    console.error("No purpose selected. Aborting submission.");
    alert("Please select a purpose (Buy/Sell) before submitting.");
    return;
  }

  // Collect property details from form inputs
  const formData = new FormData(form);
  const data = { purpose: selectedPurpose };

  formData.forEach((value, key) => {
    data[key] = value;
  });

  console.log("Collected form data:", data);

  // Validate the form before proceeding
  const isFormValid = Array.from(inputs).every(input => validateField(input));
  if (!isFormValid) {
    console.error("Form validation failed. Aborting submission.");
    alert("Please fix the errors in the form before submitting.");
    return;
  }

  // Send data to backend
  console.log("Sending data to backend...");
  fetch('/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  .then(response => {
    console.log("Received response from backend:", response);
    if (!response.ok) {
      throw new Error(`HTTP Error ${response.status}`);
    }
    return response.json();
  })
  .then(result => {
    console.log("Parsed JSON response from backend:", result);
    displayResult(result, data);
    updateHistory(result.predicted_price, data);
  })
  .catch(error => {
    console.error("Error during fetch:", error);
    alert("An error occurred while predicting. Please try again.");
  });
});

/*
     Display Prediction Result
*/
function displayResult(result, inputData) {
  console.log("Displaying prediction result...");
  const resultSection = document.getElementById('result-section');
  const predictionMessage = document.getElementById('prediction-message');

  // Display the predicted price and confidence interval
  predictionMessage.innerHTML = `Based on the data provided, your home is estimated to be valued at <strong>$${parseFloat(result.predicted_price).toLocaleString()}</strong>.<br>
    The confidence interval for this prediction ranges between <strong>$${parseFloat(result.confidence_interval[0]).toLocaleString()}</strong> and <strong>$${parseFloat(result.confidence_interval[1]).toLocaleString()}</strong>.`;

  // Add recommendations if any
  const recommendationsContainer = document.getElementById('recommendations-container');
  if (result.recommendations && result.recommendations.length > 0) {
    recommendationsContainer.innerHTML = `
      <h3>Recommendations:</h3>
      <ul>
        ${result.recommendations.map(recommendation => `<li>${recommendation}</li>`).join('')}
      </ul>
    `;
  } else {
    recommendationsContainer.innerHTML = `<p>No specific recommendations available for your input.</p>`;
  }

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
      <td>${item.purpose}</td> <!-- Added Purpose Column -->
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

// Update prediction history (store in localStorage and update the table)
function updateHistory(predicted_price, inputData) {
  const history = JSON.parse(localStorage.getItem('predictionHistory')) || [];

  // Get selected purpose value
  const selectedPurpose = document.querySelector('input[name="purpose"]:checked')?.value || 'N/A';

  history.push({
    sqft_living: inputData.sqft_living,
    no_of_bedrooms: inputData.no_of_bedrooms,
    no_of_bathrooms: inputData.no_of_bathrooms,
    sqft_lot: inputData.sqft_lot,
    no_of_floors: inputData.no_of_floors,
    house_age: inputData.house_age,
    zipcode: inputData.zipcode,
    purpose: selectedPurpose, // Store purpose
    predicted_price: parseFloat(predicted_price).toFixed(2)
  });

  localStorage.setItem('predictionHistory', JSON.stringify(history)); // Save to localStorage for persistence
  // Reset to compact view (latest 5) when a new prediction is added.
  historyExpanded = false;
  loadHistory(); // Reload history table
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