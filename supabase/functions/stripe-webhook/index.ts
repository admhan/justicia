// Justicia Académie — reçoit les notifications de paiement de Stripe,
// enregistre chaque paiement confirmé dans public.payments (voir
// supabase/paiements.sql) et active automatiquement l'abonnement de l'élève :
// si aucun compte n'existe pour l'e-mail du paiement, une invitation est
// envoyée (l'élève choisit son mot de passe) ; le profil passe à "active"
// pour un an.
//
// Déploiement et configuration : voir AUTH-SETUP.md, section Stripe.

import Stripe from "npm:stripe@17.7.0";
import { createClient } from "npm:@supabase/supabase-js@2";

// Adresse du site : Vercel tant que le domaine justicia-academie.com n'est pas
// actif ; ensuite, définir le secret SITE_URL (ex. https://www.justicia-academie.com).
const SITE_URL = `${Deno.env.get("SITE_URL") ?? "https://justicia-fawn.vercel.app"}/espace-eleve.html`;

Deno.serve(async (req) => {
  const stripeSecretKey = Deno.env.get("STRIPE_SECRET_KEY");
  const webhookSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET");
  const signature = req.headers.get("stripe-signature");

  if (!stripeSecretKey || !webhookSecret || !signature) {
    return new Response("Webhook pas encore configuré.", { status: 503 });
  }

  const stripe = new Stripe(stripeSecretKey, { apiVersion: "2024-06-20" });
  const body = await req.text();

  let event: Stripe.Event;
  try {
    event = await stripe.webhooks.constructEventAsync(body, signature, webhookSecret);
  } catch (error) {
    console.error("stripe-webhook: signature invalide", error);
    return new Response("Signature invalide.", { status: 400 });
  }

  if (event.type === "checkout.session.completed") {
    const session = event.data.object as Stripe.Checkout.Session;

    // Clé de service : seule cette fonction, côté serveur, écrit dans payments
    // et modifie les profils — jamais le navigateur.
    const supabaseAdmin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    const email = session.customer_details?.email?.toLowerCase() ?? null;

    // Stripe peut renvoyer le même événement : l'enregistrement est idempotent.
    const { error: payError } = await supabaseAdmin.from("payments").upsert(
      {
        stripe_session_id: session.id,
        customer_email: email,
        amount_total: session.amount_total,
        currency: session.currency,
        status: "paye",
      },
      { onConflict: "stripe_session_id", ignoreDuplicates: true },
    );
    if (payError) console.error("stripe-webhook: insertion payments", payError);

    if (email && session.payment_status === "paid") {
      // Compte existant ? Sinon on invite l'élève : le déclencheur
      // handle_new_user crée alors son profil.
      let { data: profile } = await supabaseAdmin
        .from("profiles")
        .select("id")
        .eq("email", email)
        .maybeSingle();

      if (!profile) {
        const { data: invited, error: inviteError } =
          await supabaseAdmin.auth.admin.inviteUserByEmail(email, { redirectTo: SITE_URL });
        if (inviteError) {
          console.error("stripe-webhook: invitation", inviteError);
        } else {
          profile = { id: invited.user.id };
        }
      }

      if (profile) {
        const expires = new Date();
        expires.setFullYear(expires.getFullYear() + 1);
        const { error: activateError } = await supabaseAdmin
          .from("profiles")
          .update({
            subscription_status: "active",
            subscription_expires_at: expires.toISOString(),
            formule: session.metadata?.formule ?? "annuelle",
          })
          .eq("id", profile.id);
        if (activateError) console.error("stripe-webhook: activation", activateError);
      }
    }
  }

  return new Response(JSON.stringify({ received: true }), {
    headers: { "Content-Type": "application/json" },
  });
});
