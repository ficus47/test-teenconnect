const text = document.getElementById("rainbow-text");
const content = text.textContent;
text.innerHTML = ""; // On efface le contenu initial
// On divise le texte en spans pour appliquer l'effet à chaque lettre
[...content].forEach((letter, i) => {
  const span = document.createElement("span");
  span.textContent = letter;
  span.style.animationDelay = `${i * 0.1}s`; // Décalage de l'effet pour chaque lettre
  text.appendChild(span);
});