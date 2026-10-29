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
const SUPABASE_URL = "https://nmgpdirswamnkxexutvu.supabase.co";
const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_zdY5JqEz8Nep6AGa2_-wwQ_wFnZk9jO";

// Arrivée par le lien de l'e-mail de bienvenue (compte tout juste créé) : à lire
// avant que le SDK ne retire les jetons de l'adresse, pour inviter l'élève à
// choisir son mot de passe dès cette première visite.
const arrivedViaInvite =
  typeof window !== "undefined" && /(^|[#&])type=invite\b/.test(window.location.hash);

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

  if (arrivedViaInvite) {
    const pwdCard = document.getElementById("password-card");
    const pwdTitle = pwdCard && pwdCard.querySelector("h2");
    const pwdIntro = pwdCard && pwdCard.querySelector("p");
    if (pwdCard && pwdTitle && pwdIntro) {
      pwdTitle.textContent = "Bienvenue ! Choisissez votre mot de passe";
      pwdIntro.textContent =
        "Votre accès est activé. Choisissez dès maintenant un mot de passe pour vous reconnecter facilement. Vous pouvez aussi passer cette étape : un lien de connexion vous sera envoyé par e-mail à chaque visite.";
      pwdCard.classList.add("is-featured");
      pwdCard.parentNode.prepend(pwdCard);
      const pwdInput = pwdCard.querySelector("input[type='password']");
      if (pwdInput) pwdInput.focus({ preventScroll: true });
      pwdCard.scrollIntoView({ block: "center" });
    }
  }
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

    const loginInfo = document.getElementById("login-info");

    // Sans mot de passe : envoi d'un lien de connexion par e-mail. Seuls les
    // comptes existants (créés au paiement) peuvent se connecter.
    if (!password) {
      const { error: otpError } = await supabaseClient.functions.invoke("send-login-link", {
        body: { email },
      });
      if (submitBtn) submitBtn.disabled = false;
      if (otpError) {
        loginError.textContent =
          "Envoi impossible pour le moment. Vérifiez l'adresse saisie et réessayez dans quelques minutes.";
        loginError.classList.add("is-visible");
        return;
      }
      loginError.classList.remove("is-visible");
      if (loginInfo) {
        loginInfo.textContent =
          "Si cette adresse correspond à un abonnement actif, un lien de connexion vient de vous être envoyé. Ouvrez votre boîte mail (et les courriers indésirables).";
        loginInfo.hidden = false;
      }
      return;
    }

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

  // Définir ou changer son mot de passe (facultatif) depuis l'espace connecté.
  const passwordForm = document.getElementById("password-form");
  if (passwordForm) {
    const passwordError = document.getElementById("password-error");
    const passwordInfo = document.getElementById("password-info");
    passwordForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const newPassword = String(new FormData(passwordForm).get("new_password") || "");
      const btn = passwordForm.querySelector("button[type='submit']");
      if (btn) btn.disabled = true;
      passwordError.classList.remove("is-visible");
      passwordInfo.hidden = true;

      const { error } = await supabaseClient.auth.updateUser({ password: newPassword });
      if (btn) btn.disabled = false;

      if (error) {
        passwordError.textContent =
          "Mot de passe refusé : 8 caractères minimum, et différent de l'actuel.";
        passwordError.classList.add("is-visible");
        return;
      }
      passwordForm.reset();
      passwordInfo.textContent = "Mot de passe enregistré. Vous pouvez désormais vous connecter avec.";
      passwordInfo.hidden = false;
    });
  }

  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      await supabaseClient.auth.signOut();
      window.location.reload();
    });
  }
}

// Paiement de la formule : le prix (250 €, paiement unique) est fixé côté
// serveur dans la fonction Edge create-checkout-session, jamais ici — ce
// script ne fait que déclencher la redirection vers Stripe et afficher le
// résultat au retour (voir AUTH-SETUP.md, section Stripe).
const checkoutBtn = document.getElementById("checkout-btn");
const checkoutError = document.getElementById("checkout-error");
const checkoutMessage = document.getElementById("checkout-message");

if (checkoutMessage) {
  const paiement = new URLSearchParams(window.location.search).get("paiement");
  if (paiement === "succes") {
    checkoutMessage.textContent =
      "Paiement reçu, merci ! Un e-mail vous donne accès à votre espace élève (pensez à vérifier vos courriers indésirables).";
    checkoutMessage.classList.add("is-visible", "is-success");
  } else if (paiement === "annule") {
    checkoutMessage.textContent = "Paiement annulé : aucune somme n'a été prélevée.";
    checkoutMessage.classList.add("is-visible");
  }
}

if (checkoutBtn && supabaseClient) {
  checkoutBtn.addEventListener("click", async () => {
    checkoutBtn.disabled = true;
    if (checkoutError) checkoutError.classList.remove("is-visible");

    const { data, error } = await supabaseClient.functions.invoke("create-checkout-session");

    if (error || !(data && data.url)) {
      checkoutBtn.disabled = false;
      if (checkoutError) {
        checkoutError.textContent =
          "Paiement momentanément indisponible. Écrivez-nous à contact@justicia-academie.com.";
        checkoutError.classList.add("is-visible");
      }
      return;
    }

    window.location.href = data.url;
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
      const newTab = window.open("", "_blank");
      if (newTab) newTab.opener = null;

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

      // Supabase Storage sert le HTML en text/plain (protection anti-XSS) :
      // le navigateur afficherait le code source. On télécharge donc la fiche
      // avec l'URL signée et on l'ouvre comme une vraie page HTML.
      let pageUrl = data.signedUrl;
      try {
        const reponse = await fetch(data.signedUrl);
        if (!reponse.ok) throw new Error("fiche indisponible");
        const html = await reponse.text();
        pageUrl = URL.createObjectURL(new Blob([html], { type: "text/html;charset=utf-8" }));
      } catch (err) {
        if (newTab) newTab.close();
        if (ficheError) ficheError.classList.add("is-visible");
        return;
      }

      if (newTab) {
        newTab.location.href = pageUrl;
      } else {
        window.location.href = pageUrl;
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
