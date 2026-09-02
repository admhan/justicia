// Justicia Académie — intégration Supabase Auth (à activer une fois le
// projet créé). Ce fichier est un exemple documenté, pas branché au site :
// la connexion de démonstration actuelle (script.js) reste active tant
// qu'il n'est pas repris.
//
// Étapes pour l'activer réellement :
//   1. Créer le projet Supabase et exécuter supabase/schema.sql (voir
//      AUTH-SETUP.md).
//   2. Remplacer SUPABASE_URL et SUPABASE_ANON_KEY ci-dessous par les
//      vraies valeurs (Project Settings > API). La clé "anon" est publique
//      par conception, protégée par les règles RLS côté serveur : elle
//      peut rester dans le code livré au navigateur, contrairement à la
//      "service_role key" qui ne doit jamais quitter Supabase.
//   3. Charger le SDK dans le <head> des pages concernées :
//      <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
//   4. Remplacer la logique de script.js (section "Espace élève") par les
//      fonctions ci-dessous.

const SUPABASE_URL = "https://VOTRE-PROJET.supabase.co";
const SUPABASE_ANON_KEY = "VOTRE_CLE_ANON_PUBLIQUE";

const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Inscription
async function inscrire(email, password) {
  const { data, error } = await supabase.auth.signUp({ email, password });
  if (error) throw error;
  return data;
}

// Connexion
async function seConnecter(email, password) {
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) throw error;
  return data;
}

// Déconnexion
async function seDeconnecter() {
  await supabase.auth.signOut();
}

// Session courante (à appeler au chargement de chaque page pour savoir si
// l'utilisateur est connecté, sans devoir relire localStorage soi-même).
async function recupererSession() {
  const { data } = await supabase.auth.getSession();
  return data.session; // null si non connecté
}

// Profil + statut d'abonnement de l'utilisateur connecté
async function recupererProfil() {
  const { data: auth } = await supabase.auth.getUser();
  if (!auth.user) return null;
  const { data, error } = await supabase
    .from("profiles")
    .select("*")
    .eq("id", auth.user.id)
    .single();
  if (error) throw error;
  return data; // { full_name, formule, subscription_status, ... }
}

// Récupérer une fiche protégée (bucket Storage privé "fiches") : ne
// réussit que si la politique RLS de supabase/schema.sql autorise l'accès
// (abonnement actif), sinon Supabase renvoie une erreur d'autorisation.
async function recupererFiche(cheminDansLeBucket) {
  const { data, error } = await supabase.storage
    .from("fiches")
    .createSignedUrl(cheminDansLeBucket, 60); // lien valable 60 secondes
  if (error) throw error;
  return data.signedUrl;
}
