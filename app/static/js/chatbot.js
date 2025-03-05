document.addEventListener("DOMContentLoaded", function () {
    const recommendationsContainer = document.getElementById("recommendations-container");

    function typeText(element, text, delay = 0, onComplete = () => {}) {
        let index = 0;
        function type() {
            if (index < text.length) {
                element.innerHTML += text.charAt(index);
                index++;
                setTimeout(type, delay - 10 + Math.floor(Math.random() * 20)); // Slightly faster by reducing delay
            } else {
                onComplete(); // Call when typing is finished
            }
        }
        type();
    }


    function addRecommendationsTitle(onComplete = () => {}) {
        const titleElement = document.getElementById("recommendations-title");
        
        if (titleElement) {
            titleElement.innerHTML = ""; // Clear any existing text
            typeText(titleElement, "📈 Smart Moves: Market Insights Tailored for You!", 50, onComplete);
        }
    }
    
    

    function showLoadingIndicator() {
        const loadingDiv = document.createElement("div");
        loadingDiv.classList.add("chatbot-loading");
        loadingDiv.innerHTML = "...";
    
        // Find the last recommendation message
        const lastMessage = recommendationsContainer.lastElementChild;
    
        if (lastMessage) {
            // Match the width of the last message
            loadingDiv.style.width = getComputedStyle(lastMessage).width;
            loadingDiv.style.marginLeft = getComputedStyle(lastMessage).marginLeft;
    
            // Insert loading indicator right after the last message
            lastMessage.insertAdjacentElement("afterend", loadingDiv);
        } else {
            // If no messages exist, just add it normally
            recommendationsContainer.appendChild(loadingDiv);
        }
    
        let dots = 0;
        const interval = setInterval(() => {
            dots = (dots + 1) % 4; // Cycle between "", ".", "..", "..."
            loadingDiv.innerHTML = ".".repeat(dots);
        }, 500);
    
        return { element: loadingDiv, stop: () => clearInterval(interval) };
    }
    

    function displayRecommendations(recommendations) {
        recommendationsContainer.innerHTML = ""; // Clear old content
        
        addRecommendationsTitle(() => {
            // Once title finishes typing, proceed with recommendations
            let delayBeforeStart = 1000; // 1s delay before first message
        
            if (recommendations && recommendations.length > 0) {
                let messageIndex = 0;
    
                function typeNextMessage() {
                    if (messageIndex < recommendations.length) {
                        const rec = recommendations[messageIndex];
                        const loadingIndicator = showLoadingIndicator();
    
                        setTimeout(() => {
                            loadingIndicator.stop();
                            recommendationsContainer.removeChild(loadingIndicator.element);
    
                            const messageDiv = document.createElement("div");
                            messageDiv.classList.add("chatbot-message");
                            recommendationsContainer.appendChild(messageDiv);
    
                            typeText(messageDiv, rec, 50, () => {
                                recommendationsContainer.scrollTop = recommendationsContainer.scrollHeight;
    
                                messageIndex++;
                                typeNextMessage();
                            });
                        }, 1000);
                    } else {
                        setTimeout(() => {
                            const closingDiv = document.createElement("div");
                            closingDiv.classList.add("chatbot-message", "closing-message");
                            recommendationsContainer.appendChild(closingDiv);
                            typeText(closingDiv, "I hope these insights help! 😊 If you need more tailored advice, try tweaking one of the house features above and click ‘Predict’—I'll refine my recommendations for you!");
                        }, 1000);
                    }
                }
    
                typeNextMessage();
            } else {
                recommendationsContainer.innerHTML = `<p class="chatbot-message">No specific recommendations available.</p>`;
            }
        });
    }
    
    

    // Expose function to update recommendations
    window.updateChatbotRecommendations = function (recommendations) {
        displayRecommendations(recommendations);
    };
});
   