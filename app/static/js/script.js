document.addEventListener('DOMContentLoaded', function() {
  /* ===============================
     Theme Toggle Functionality
  =============================== */
  const toggle = document.getElementById('theme-toggle');

  // Determine saved theme or use system preference if none saved
  let theme = localStorage.getItem('theme');
  if (!theme) {
    theme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }
  setTheme(theme);

  function setTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark-mode');
      document.documentElement.classList.remove('light-mode');
      toggle.textContent = '🌕'; // Full moon icon
    } else {
      document.documentElement.classList.add('light-mode');
      document.documentElement.classList.remove('dark-mode');
      toggle.textContent = '🌙'; // Crescent moon icon
    }
    localStorage.setItem('theme', theme);
  }

  toggle.addEventListener('click', function() {
    if (document.documentElement.classList.contains('dark-mode')) {
      setTheme('light');
    } else {
      setTheme('dark');
    }
  });

  /* ===============================
     Housing Form and Prediction Logic
  =============================== */
  const form = document.getElementById('housing-form');
  const predictBtn = document.getElementById('predict-btn');
  const inputs = form.querySelectorAll('input');

  // Define validation rules (min, max, and error messages)
  const validationRules = {
    sqft_living: { min: 200, max: 10000, error: "Living area must be between 200 and 10,000 sqft." },
    no_of_bedrooms: { min: 1, max: 25, error: "Number of bedrooms must be between 1 and 25." },
    no_of_bathrooms: { min: 1, max: 15, error: "Number of bathrooms must be between 1 and 15." },
    sqft_lot: { min: 500, max: 50000, error: "Lot size must be between 500 and 50,000 sqft." },
    no_of_floors: { min: 0, max: 10, error: "Floors must be between 0 and 10." },
    house_age: { min: 0, max: 150, error: "House age must be between 0 and 150 years." },
    zipcode: { min: 98001, max: 99001, error: "Invalid ZIP code. Must be between 98001 and 99001." }
  };

  // Real-time validation for each input field
  inputs.forEach(input => {
    input.addEventListener('input', function() {
      validateField(input);
      checkFormValidity();
    });
  });

  function validateField(input) {
    const fieldName = input.name;
    const value = parseFloat(input.value);
    const rule = validationRules[fieldName];
    const errorMsgEl = input.nextElementSibling; // Assumes a <small> element follows the input

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

  // Load prediction history from localStorage and display in table
  function loadHistory() {
    const historyTableBody = document.querySelector('#history-table tbody');
    historyTableBody.innerHTML = "";
    const history = JSON.parse(localStorage.getItem('predictionHistory')) || [];
    history.forEach(item => {
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
  }

  loadHistory();

  // Clear history button
  document.getElementById('clear-history').addEventListener('click', function() {
    localStorage.removeItem('predictionHistory');
    loadHistory();
  });

  // Handle form submission (using AJAX/fetch)
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
      headers: {
        'Content-Type': 'application/json'
      },
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

    // Hide the form section and show the result section
    document.getElementById('form-section').classList.add('hidden');
    resultSection.classList.remove('hidden');
    resultSection.scrollIntoView({ behavior: 'smooth' });
  }

  // Update prediction history (both localStorage and the displayed table)
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
    localStorage.setItem('predictionHistory', JSON.stringify(history));
    loadHistory();
  }

  // “Back to Form” button to allow making another prediction
  document.getElementById('back-to-form').addEventListener('click', function() {
    document.getElementById('result-section').classList.add('hidden');
    document.getElementById('form-section').classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    form.reset();
    predictBtn.disabled = true;
  });
});
