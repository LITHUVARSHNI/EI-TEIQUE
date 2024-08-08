document.addEventListener('DOMContentLoaded', function () {
    const predictButton = document.getElementById('predict-button');
    const predictionsDiv = document.getElementById('predictions');
    const errorMessageDiv = document.getElementById('error-message');

    predictButton.addEventListener('click', function () {
        // Hide the error message and predictions div
        errorMessageDiv.style.display = 'none';
        predictionsDiv.style.display = 'none';

        // Collect user responses from the form
        const formData = new FormData(document.getElementById('section1-form'));

        // Convert form data to JSON
        const userResponses = {};
        formData.forEach(function (value, key) {
            userResponses[key] = value;
        });

        // Send a POST request to the Flask server for predictions
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userResponses),
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            // Display predictions in the "predictions" div
            const wellBeingPrediction = document.getElementById('well-being-prediction');
            const socialityPrediction = document.getElementById('sociality-prediction');
            const emotionalityPrediction = document.getElementById('emotionality-prediction');
            const selfControlPrediction = document.getElementById('self-control-prediction');

            wellBeingPrediction.textContent = data.well_being;
            socialityPrediction.textContent = data.sociality;
            emotionalityPrediction.textContent = data.emotionality;
            selfControlPrediction.textContent = data.self_control;

            predictionsDiv.style.display = 'block';
        })
        .catch((error) => {
            // Display error message
            errorMessageDiv.textContent = 'An error occurred. Please try again.';
            errorMessageDiv.style.display = 'block';
        });
    });
});
