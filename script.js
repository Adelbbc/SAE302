// Page d'accueil - Redirection vers la page de création de compte
document.getElementById("commencerBtn").addEventListener("click", function() {
    window.location.href = "create-account.html"; // Redirection vers la page de création de compte
});

// Validation du formulaire de création de compte
document.getElementById("createAccountForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Empêche l'envoi du formulaire par défaut

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (validateEmail(email) && validatePassword(password)) {
        // Effectuer l'inscription (vous pouvez envoyer les données au serveur ici)
        alert("Inscription réussie !");
        window.location.href = "quiz.html"; // Redirige vers la page du quiz après l'inscription
    } else {
        alert("Veuillez vérifier vos informations.");
    }
});

