document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictForm');
    const resultsModal = document.getElementById('resultsModal');
    const closeButton = document.getElementById('closeButton');
    const predictionResults = document.getElementById('predictionResults');
    const loadingOverlay = document.getElementById('loadingOverlay');

    resultsModal.style.display = 'none';

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        loadingOverlay.style.display = 'flex';

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            loadingOverlay.style.display = 'none';
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            const predictedRevenue = data.results;
            const expectedBudget = data.expected_budget;

            if (predictedRevenue > expectedBudget) {
                predictionResults.innerHTML = `
                    <p style="color: green;">Predicted Revenue: $${predictedRevenue.toFixed(2)}</p>
                    <p>!!! Your filim can recover the expected budget !!!</p>
                `;
            } else {
                predictionResults.innerHTML = `
                    <p style="color: red;">Predicted Revenue: $${predictedRevenue.toFixed(2)}</p>
                    <p>Your filim may not recover the expected budget try reducing it</p>
                `;
            }

            resultsModal.style.display = 'flex';
        })
        .catch(error => {
            loadingOverlay.style.display = 'none';
            alert('An error occurred. Please try again.');
            console.error('Error:', error);
        });
    });

    closeButton.addEventListener('click', () => {
        resultsModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == resultsModal) {
            resultsModal.style.display = 'none';
        }
    });
});
