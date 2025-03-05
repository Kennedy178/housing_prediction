document.addEventListener("DOMContentLoaded", function () {
    const recommendationsContainer = document.getElementById("recommendations-container");

    function typeText(element, text, delay = 50) {
        let index = 0;
        function type() {
            if (index < text.length) {
                element.innerHTML += text.charAt(index);
                index++;
                setTimeout(type, delay);
            }
        }
        type();
    }

    function displayRecommendations(recommendations) {
        recommendationsContainer.innerHTML = ""; // Clear old content

        if (recommendations && recommendations.length > 0) {
            recommendations.forEach((rec, index) => {
                setTimeout(() => {
                    const messageDiv = document.createElement("div");
                    messageDiv.classList.add("chatbot-message");
                    recommendationsContainer.appendChild(messageDiv);
                    typeText(messageDiv, rec);
                }, index * 1000); // Delay each message
            });
        } else {
            recommendationsContainer.innerHTML = `<p class="chatbot-message">No specific recommendations available.</p>`;
        }
    }

    // Modify this function inside script.js to pass recommendations to chatbot.js
    window.updateChatbotRecommendations = function (recommendations) {
        displayRecommendations(recommendations);
    };
});
