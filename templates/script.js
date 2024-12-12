
document.getElementById('register-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Empêche le rechargement de la page

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    // Vérifier si les mots de passe correspondent
    if (password !== confirmPassword) {
        alert("Les mots de passe ne correspondent pas !");
        return; // Arrête l'exécution si les mots de passe ne correspondent pas
    }

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const result = await response.json();
        if (response.ok) {
            alert('Inscription réussie ! Vous pouvez maintenant vous connecter.');
            window.location.href = "/connexion";  // Redirige vers la page de connexion
        } else {
            alert(result.error || 'Erreur lors de l\'inscription.');
        }
    } catch (error) {
        alert('Une erreur est survenue. Veuillez réessayer.');
    }
});

