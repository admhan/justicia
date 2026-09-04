// Justicia Académie — interactions

// Adresse de réception des demandes de rendez-vous : provisoire le temps de
// la mise en place définitive, à remplacer ici (un seul endroit) le moment venu.
const RDV_DESTINATION_EMAIL = "adamhannachi8@gmail.com";

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

// Espace élève : authentification réelle via Supabase Auth.
// La clé ci-dessous est publique par conception (protégée par les règles
// RLS côté serveur, voir supabase/schema.sql) : sans danger dans ce fichier.
const SUPABASE_URL = "https://ybpgwhmfxxsugiyevylj.supabase.co";
const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_jAq-sH4QE1ke_KFBWEO7zg_YF1lvkbU";

const supabaseClient =
  typeof window !== "undefined" && window.supabase
    ? window.supabase.createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)
    : null;

const STATUS_LABELS = {
  active: "Abonnement actif",
  inactive: "Abonnement inactif",
  trial: "Période d'essai",
};

const espaceLink = document.querySelector(".nav-espace");

function setNavConnected(connected) {
  if (!espaceLink) return;
  const label = espaceLink.querySelector(".nav-espace-label");
  espaceLink.classList.toggle("is-connected", connected);
  if (label) label.textContent = connected ? "Mon espace" : "Espace élève";
}

// État du lien "Espace élève" dans la navigation, sur toutes les pages
if (supabaseClient) {
  supabaseClient.auth.getSession().then(({ data }) => {
    setNavConnected(Boolean(data.session));
  });
}

// Page espace-eleve : bascule connexion / espace connecté
const loginView = document.getElementById("login-view");
const memberView = document.getElementById("member-view");

async function showMemberView() {
  const { data: authData } = await supabaseClient.auth.getUser();
  if (!authData.user) return;

  const { data: profile } = await supabaseClient
    .from("profiles")
    .select("full_name, formule, subscription_status")
    .eq("id", authData.user.id)
    .single();

  const memberName = document.getElementById("member-name");
  const memberSub = document.querySelector(".member-sub");
  if (memberName) {
    memberName.textContent = (profile && profile.full_name) || authData.user.email;
  }
  if (memberSub) {
    const status = STATUS_LABELS[profile && profile.subscription_status] || "Statut inconnu";
    memberSub.textContent = profile && profile.formule ? `${status} · ${profile.formule}` : status;
  }

  loginView.classList.add("is-hidden");
  memberView.classList.remove("is-hidden");
}

if (loginView && memberView && supabaseClient) {
  supabaseClient.auth.getSession().then(({ data }) => {
    if (data.session) showMemberView();
  });

  const loginForm = document.getElementById("login-form");
  const loginError = document.getElementById("login-error");

  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(loginForm);
    const email = String(data.get("email") || "").trim();
    const password = String(data.get("password") || "");

    const submitBtn = loginForm.querySelector("button[type='submit']");
    if (submitBtn) submitBtn.disabled = true;

    const { error } = await supabaseClient.auth.signInWithPassword({ email, password });

    if (submitBtn) submitBtn.disabled = false;

    if (error) {
      loginError.textContent =
        "Connexion impossible : identifiants incorrects, ou adresse pas encore confirmée (vérifiez votre boîte mail).";
      loginError.classList.add("is-visible");
      return;
    }

    loginError.classList.remove("is-visible");
    setNavConnected(true);
    await showMemberView();
  });

  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      await supabaseClient.auth.signOut();
      window.location.reload();
    });
  }
}

// Calendrier du semestre : chaque fiche porte sa date de mise à disposition
// (data-date, posée à la génération depuis _fiches_metadata.json) et arrive
// verrouillée dans le HTML. On ne lève le verrou que pour les dates échues,
// à l'ouverture de la page — la page étant servie en statique, c'est le
// navigateur qui fait avancer le calendrier, sans regénérer le site.
const ficheItems = document.querySelectorAll(".fiche-item");

function formatJour(date) {
  const mois = date.toLocaleDateString("fr-FR", { month: "long" });
  const jour = date.getDate();
  // En français, le premier du mois s'écrit « 1er », les autres en chiffre nu.
  return `${jour === 1 ? "1er" : jour} ${mois} ${date.getFullYear()}`;
}

if (ficheItems.length) {
  // Minuit du jour courant : une fiche datée d'aujourd'hui s'ouvre dès le
  // matin, et non à l'heure exacte du chargement.
  const aujourdhui = new Date();
  aujourdhui.setHours(0, 0, 0, 0);

  ficheItems.forEach((item) => {
    const brut = item.dataset.date;
    const jour = brut ? new Date(brut + "T00:00:00") : null;
    const label = item.querySelector(".fiche-date");
    const link = item.querySelector(".fiche-link");

    // Date absente ou illisible : la fiche reste verrouillée, sans date
    // affichée. Le silence vaut mieux qu'une promesse fausse.
    if (!jour || Number.isNaN(jour.getTime())) {
      if (label) label.textContent = "Bientôt disponible";
      return;
    }

    if (jour <= aujourdhui) {
      item.classList.remove("is-locked");
      if (label) label.remove();
      if (link) {
        link.removeAttribute("aria-disabled");
        link.removeAttribute("tabindex");
      }
    } else if (label) {
      label.textContent = "Disponible le " + formatJour(jour);
    }
  });

  // « 3 fiches sur 10 disponibles » sous chaque titre de matière.
  document.querySelectorAll(".fiche-count").forEach((count) => {
    const section = count.closest("section");
    const total = Number(count.dataset.total || 0);
    const ouvertes = section.querySelectorAll(
      ".fiche-item:not(.is-locked)"
    ).length;
    if (!total) return;
    count.textContent =
      ouvertes === total
        ? `${total} fiches de cours, toutes disponibles.`
        : `${ouvertes} fiche${ouvertes > 1 ? "s" : ""} disponible${ouvertes > 1 ? "s" : ""} sur ${total}.`;
  });
}

// Fiches de cours protégées : aucun lien statique, une URL signée est
// générée à la demande et n'est valable que 60 secondes. L'accès réel est
// tranché côté serveur par la politique RLS du compartiment (abonnement
// actif), pas par ce script : un refus ici reflète toujours un vrai refus.
const ficheLinks = document.querySelectorAll(".fiche-item:not(.is-locked) .fiche-link");

if (ficheLinks.length && supabaseClient) {
  const ficheError = document.getElementById("fiche-access-error");

  ficheLinks.forEach((link) => {
    link.addEventListener("click", async (event) => {
      event.preventDefault();
      if (ficheError) ficheError.classList.remove("is-visible");

      // Ouvert tout de suite, dans le geste de clic : un navigateur bloque
      // window.open() appelé après un await, la fenêtre doit donc déjà
      // exister avant les appels réseau qui suivent.
      const newTab = window.open("", "_blank", "noopener");

      const { data: sessionData } = await supabaseClient.auth.getSession();
      if (!sessionData.session) {
        if (newTab) newTab.close();
        window.location.href = "../espace-eleve.html";
        return;
      }

      const path = link.dataset.path;
      const { data, error } = await supabaseClient.storage.from("fiches").createSignedUrl(path, 60);

      if (error || !data) {
        if (newTab) newTab.close();
        if (ficheError) ficheError.classList.add("is-visible");
        return;
      }

      if (newTab) {
        newTab.location.href = data.signedUrl;
      } else {
        window.location.href = data.signedUrl;
      }
    });
  });
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
      "mailto:" + RDV_DESTINATION_EMAIL +
      "?subject=" + encodeURIComponent("Demande de rendez-vous") +
      "&body=" + encodeURIComponent(lignes.join("\n"));
    window.location.href = url;
  });
}
