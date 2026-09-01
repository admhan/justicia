// Justicia Académie — interactions

// Menu mobile
const toggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".site-nav");

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  nav.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    }
  });
}

// Révélation au défilement
const revealed = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );
  revealed.forEach((el) => observer.observe(el));
} else {
  revealed.forEach((el) => el.classList.add("is-visible"));
}

// Espace élève : session de démonstration côté client.
// En production, remplacer par un vrai backend d'authentification
// (l'interface et les états connecté/déconnecté sont déjà en place).
const SESSION_KEY = "justicia_session";
const DEMO_ACCOUNT = { email: "eleve@justicia-academie.com", password: "demo2026", name: "Camille" };

function getSession() {
  try {
    return JSON.parse(localStorage.getItem(SESSION_KEY));
  } catch (e) {
    return null;
  }
}

// État du lien "Espace élève" dans la navigation, sur toutes les pages
const espaceLink = document.querySelector(".nav-espace");
const session = getSession();

if (espaceLink && session) {
  espaceLink.classList.add("is-connected");
  const label = espaceLink.querySelector(".nav-espace-label");
  if (label) label.textContent = "Mon espace";
}

// Page espace-eleve : bascule connexion / espace connecté
const loginView = document.getElementById("login-view");
const memberView = document.getElementById("member-view");

function showMemberView(name) {
  const memberName = document.getElementById("member-name");
  if (memberName) memberName.textContent = name;
  loginView.classList.add("is-hidden");
  memberView.classList.remove("is-hidden");
}

if (loginView && memberView) {
  if (session) showMemberView(session.name);

  const loginForm = document.getElementById("login-form");
  const loginError = document.getElementById("login-error");

  loginForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(loginForm);
    const email = String(data.get("email") || "").trim().toLowerCase();
    const password = String(data.get("password") || "");
    if (email === DEMO_ACCOUNT.email && password === DEMO_ACCOUNT.password) {
      localStorage.setItem(SESSION_KEY, JSON.stringify({ name: DEMO_ACCOUNT.name }));
      loginError.classList.remove("is-visible");
      if (espaceLink) {
        espaceLink.classList.add("is-connected");
        const label = espaceLink.querySelector(".nav-espace-label");
        if (label) label.textContent = "Mon espace";
      }
      showMemberView(DEMO_ACCOUNT.name);
    } else {
      loginError.classList.add("is-visible");
    }
  });

  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.removeItem(SESSION_KEY);
      window.location.reload();
    });
  }
}

// Capsules vidéo : une seule lecture à la fois
const videos = document.querySelectorAll(".video-card video");

videos.forEach((video) => {
  video.addEventListener("play", () => {
    videos.forEach((other) => {
      if (other !== video) other.pause();
    });
  });
});

// Formulaire de rendez-vous : ouvre le client mail avec la demande pré-remplie
const form = document.getElementById("rdv-form");

if (form) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const lignes = [
      "Demande de rendez-vous — Justicia Académie",
      "",
      "Nom : " + (data.get("nom") || ""),
      "Statut : " + (data.get("statut") || ""),
      "E-mail : " + (data.get("email") || ""),
      "Téléphone : " + (data.get("telephone") || ""),
      "",
      "Situation :",
      data.get("message") || "",
    ];
    const url =
      "mailto:contact@justicia-academie.com" +
      "?subject=" + encodeURIComponent("Demande de rendez-vous") +
      "&body=" + encodeURIComponent(lignes.join("\n"));
    window.location.href = url;
  });
}
