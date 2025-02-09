document.addEventListener("DOMContentLoaded", function() {
    // Dark/Light Toggle Functionality
    const themeToggle = document.getElementById("themeToggle");
    const themeLabel = document.getElementById("themeLabel");
  
    // Apply saved theme from localStorage
    if (localStorage.getItem("theme") === "dark") {
      document.body.classList.add("dark-mode");
      themeToggle.checked = true;
      themeLabel.textContent = "Dark Mode";
    } else {
      themeLabel.textContent = "Light Mode";
    }
  
    themeToggle.addEventListener("change", function() {
      if (this.checked) {
        document.body.classList.add("dark-mode");
        localStorage.setItem("theme", "dark");
        themeLabel.textContent = "Dark Mode";
      } else {
        document.body.classList.remove("dark-mode");
        localStorage.setItem("theme", "light");
        themeLabel.textContent = "Light Mode";
      }
    });
  
    // Prediction History Functionality
    const historyTableBody = document.querySelector("#historyTable tbody");
    const clearHistoryBtn = document.getElementById("clearHistoryBtn");
  
    function loadHistory() {
      historyTableBody.innerHTML = "";
      const history = JSON.parse(localStorage.getItem("predictionHistory")) || [];
      history.forEach(entry => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${entry.sqft_living}</td>
          <td>${entry.no_of_bedrooms}</td>
          <td>${entry.no_of_bathrooms}</td>
          <td>${entry.sqft_lot}</td>
          <td>${entry.no_of_floors}</td>
          <td>${entry.house_age}</td>
          <td>${entry.zipcode}</td>
          <td>$${entry.predicted_price}</td>
        `;
        historyTableBody.appendChild(row);
      });
    }
  
    loadHistory();
  
    clearHistoryBtn.addEventListener("click", function() {
      localStorage.removeItem("predictionHistory");
      loadHistory();
    });
  
    // After form submission, if a prediction result is present,
    // save the prediction along with input features to localStorage.
    const resultSection = document.getElementById("result-section");
    if (resultSection && resultSection.querySelector(".result-message")) {
      // Extract predicted price from the result message.
      // Here we assume the result message contains the price in a format like "$123,456"
      const resultMessage = resultSection.querySelector(".result-message p").textContent;
      const priceMatch = resultMessage.match(/\$([\d,\.]+)/);
      if (priceMatch) {
        const predictedPrice = priceMatch[1];
  
        // Retrieve form values from the input fields
        const sqftLiving = document.getElementById("sqft_living").value;
        const bedrooms = document.getElementById("no_of_bedrooms").value;
        const bathrooms = document.getElementById("no_of_bathrooms").value;
        const sqftLot = document.getElementById("sqft_lot").value;
        const floors = document.getElementById("no_of_floors").value;
        const houseAge = document.getElementById("house_age").value;
        const zipcode = document.getElementById("zipcode").value;
  
        const newEntry = {
          sqft_living: sqftLiving,
          no_of_bedrooms: bedrooms,
          no_of_bathrooms: bathrooms,
          sqft_lot: sqftLot,
          no_of_floors: floors,
          house_age: houseAge,
          zipcode: zipcode,
          predicted_price: predictedPrice
        };
  
        let history = JSON.parse(localStorage.getItem("predictionHistory")) || [];
        history.push(newEntry);
        localStorage.setItem("predictionHistory", JSON.stringify(history));
        loadHistory();
      }
    }
  });
  