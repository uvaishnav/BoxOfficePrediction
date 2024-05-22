document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictForm');
    const resultsModal = document.getElementById('resultsModal');
    const closeButton = document.getElementById('closeButton');
    const predictionResults = document.getElementById('predictionResults');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingIcons = document.getElementById('loadingIcons')
    const formSection = document.querySelector('.form-bg');
    const navBar = document.getElementById('navBar');
    const mainSection = document.querySelector('main'); 
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    resultsModal.style.display = 'none';

    document.getElementById('predictButton').addEventListener('click', function() {
        document.getElementById('predictFormContainer').scrollIntoView({ behavior: 'smooth' });
        navBar.classList.add('hide-nav');
    });

    // Toggle the collapsed class on click
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('collapsed');
    });

    // Show modal with animation
    function showModal() {
        resultsModal.classList.add('show');
    }
    // Hide modal with animation
    function hideModal() {
        resultsModal.classList.remove('show');
        setTimeout(() => {
            resultsModal.style.display = 'none';
        }, 300); // Match the transition duration
    }

    closeButton.addEventListener('click', hideModal);
    window.addEventListener('click', (event) => {
        if (event.target == resultsModal) {
            hideModal();
        }
    });

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        loadingOverlay.style.display = 'flex';
        loadingIcons.style.display = 'flex';

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
            loadingIcons.style.display = 'none'
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
            setTimeout(showModal, 10); // Allow a short delay to ensure display: flex is applied
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

    window.addEventListener('scroll', function() {
        if (isHalfInViewport(mainSection)) {
            navBar.classList.remove('hide-nav');
        } else if (isHalfInViewport(formSection)) {
            navBar.classList.add('hide-nav');
        }
    });

    // Helper function to check if an element is at least half in the viewport
    function isHalfInViewport(element) {
        const rect = element.getBoundingClientRect();
        const windowHeight = (window.innerHeight || document.documentElement.clientHeight);
        const windowWidth = (window.innerWidth || document.documentElement.clientWidth);

        const vertInView = (rect.top <= windowHeight / 2) && ((rect.bottom - (rect.height / 2)) >= 0);
        const horInView = (rect.left <= windowWidth / 2) && ((rect.right - (rect.width / 2)) >= 0);

        return (vertInView && horInView);
    }

});