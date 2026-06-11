document.addEventListener('DOMContentLoaded', () => {
    // API server base URL
    const API_URL = 'http://127.0.0.1:5000';

    // Screen elements
    const authScreen = document.getElementById('auth-screen');
    const mainMenuScreen = document.getElementById('main-menu-screen');
    const gameScreen = document.getElementById('game-screen');

    // Form elements
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    // Links to switch between login/register
    const showRegisterLink = document.getElementById('show-register-link');
    const showLoginLink = document.getElementById('show-login-link');

    // Buttons
    const loginBtn = document.getElementById('login-btn');
    const registerBtn = document.getElementById('register-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const showScoresBtn = document.getElementById('show-scores-btn');
    const backToMenuBtn = document.getElementById('back-to-menu-btn');

    // Global state
    let currentUser = null;

    // --- Screen Navigation ---
    function showScreen(screen) {
        authScreen.classList.add('hidden');
        mainMenuScreen.classList.add('hidden');
        gameScreen.classList.add('hidden');
        screen.classList.remove('hidden');
    }

    showRegisterLink.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
    });

    showLoginLink.addEventListener('click', (e) => {
        e.preventDefault();
        registerForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
    });

    // --- API Communication ---
    async function apiRequest(endpoint, method, body = null) {
        try {
            const options = {
                method: method,
                headers: { 'Content-Type': 'application/json' },
            };
            if (body) {
                options.body = JSON.stringify(body);
            }
            const response = await fetch(`${API_URL}${endpoint}`, options);
            return response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            alert('Could not connect to the server. Make sure the backend is running.');
        }
    }

    // --- Event Listeners ---
    registerBtn.addEventListener('click', async () => {
        const username = document.getElementById('register-username').value;
        const password = document.getElementById('register-password').value;
        const result = await apiRequest('/register', 'POST', { username, password });
        alert(result.message);
        if (result.success) {
            showLoginLink.click();
        }
    });

    loginBtn.addEventListener('click', async () => {
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        const result = await apiRequest('/login', 'POST', { username, password });
        if (result.success) {
            currentUser = username;
            document.getElementById('welcome-message').innerText = `Welcome, ${currentUser}!`;
            showScreen(mainMenuScreen);
        } else {
            alert(result.message);
        }
    });

    logoutBtn.addEventListener('click', () => {
        currentUser = null;
        showScreen(authScreen);
    });

    showScoresBtn.addEventListener('click', async () => {
        const result = await apiRequest(`/scores/${currentUser}`, 'GET');
        if (result.success) {
            const scores = result.scores;
            alert(
                `Your Scores:\n` +
                `Number Guessing: ${scores.game1_number_guess}\n` +
                `Rock Paper Scissors: ${scores.game2_rps}`
            );
        }
    });
    
    backToMenuBtn.addEventListener('click', () => showScreen(mainMenuScreen));

    // --- Game Logic (Example: Number Guessing) ---
    document.querySelectorAll('.game-btn').forEach(button => {
        button.addEventListener('click', () => {
            const gameId = button.dataset.game;
            if (gameId === 'number_guess') {
                startNumberGuessingGame();
            }
            // Add logic for other games here...
        });
    });

    function startNumberGuessingGame() {
        document.getElementById('game-title').innerText = 'Number Guessing Game';
        const gameContent = document.getElementById('game-content');
        
        const secret = Math.floor(Math.random() * 50) + 1;
        let attempts = 0;
        
        gameContent.innerHTML = `
            <p>I'm thinking of a number between 1 and 50.</p>
            <input type="number" id="guess-input" placeholder="Enter your guess">
            <button id="submit-guess-btn">Submit Guess</button>
            <p id="feedback-text"></p>
        `;
        
        showScreen(gameScreen);

        document.getElementById('submit-guess-btn').addEventListener('click', async () => {
            const guess = parseInt(document.getElementById('guess-input').value);
            const feedbackText = document.getElementById('feedback-text');
            attempts++;

            if (guess < secret) {
                feedbackText.innerText = 'Too low!';
            } else if (guess > secret) {
                feedbackText.innerText = 'Too high!';
            } else {
                feedbackText.innerText = `Correct! You found it in ${attempts} attempts.`;
                // Update score on the backend
                await apiRequest('/update_score', 'POST', { username: currentUser, game_id: 'game1_number_guess', score: attempts });
                document.getElementById('submit-guess-btn').disabled = true;
            }
        });
    }

    // Note: The Snake game cannot be run this way. It would need to be rebuilt
    // using HTML5 Canvas and JavaScript.
});