// Justicia Académie — reçoit les notifications de paiement de Stripe,
// enregistre chaque paiement confirmé dans public.payments, crée le compte de
// l'élève s'il n'existe pas, active son abonnement pour un an et lui envoie
// par e-mail (Resend) son lien d'accès à l'espace élève.
//
// Si l'envoi de l'e-mail échoue, la fonction répond 500 : Stripe renvoie alors
// la notification plus tard, et tout le traitement est rejouable sans doublon.

import Stripe from "npm:stripe@17.7.0";
import { createClient } from "npm:@supabase/supabase-js@2";

const SITE_BASE = Deno.env.get("SITE_URL") ?? "https://justicia-fawn.vercel.app";
const REDIRECT_TO = `${SITE_BASE}/espace-eleve.html`;

async function sendMail(to: string, subject: string, html: string): Promise<boolean> {
  const key = Deno.env.get("RESEND_API_KEY");
  if (!key) {
    console.error("stripe-webhook: RESEND_API_KEY manquant");
    return false;
  }
  const from = Deno.env.get("MAIL_FROM") ?? "Justicia Académie <justicia@mail.promptheusia.com>";
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from, to: [to], subject, html }),
  });
  if (!res.ok) console.error("stripe-webhook: Resend", res.status, await res.text());
  return res.ok;
}

function welcomeEmail(link: string): string {
  return `<!doctype html><html lang="fr"><body style="margin:0;background:#F7F4EC;font-family:Georgia,serif;color:#33322D">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:32px 16px">
<table width="520" cellpadding="0" cellspacing="0" style="background:#FDFCF9;border:1px solid #C9A94E;max-width:100%">
<tr><td style="padding:28px 32px;border-bottom:3px double #16233F;font-size:22px;color:#16233F">Justicia Académie</td></tr>
<tr><td style="padding:28px 32px;font-size:16px;line-height:1.6">
<p style="margin:0 0 16px">Bonjour,</p>
<p style="margin:0 0 16px">Merci pour votre confiance : votre paiement est bien reçu et votre accès pour l'année est activé.</p>
<p style="margin:0 0 24px">Cliquez ci-dessous pour ouvrir votre espace élève : vous y choisirez tout de suite votre mot de passe. Si vous préférez ne pas en avoir, il suffira de saisir votre adresse e-mail sur la page de connexion pour recevoir un nouveau lien à chaque visite.</p>
<p style="margin:0 0 24px"><a href="${link}" style="background:#16233F;color:#FDFCF9;text-decoration:none;padding:12px 24px;display:inline-block">Accéder à mon espace</a></p>
<p style="margin:0;font-size:13px;color:#5A6B87">Ce lien est valable une heure. Une question : répondez simplement à cet e-mail.</p>
</td></tr></table></td></tr></table></body></html>`;
}

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
    // et modifie les profils, jamais le navigateur.
    const admin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    const email = session.customer_details?.email?.toLowerCase() ?? null;

    // Stripe peut renvoyer le même événement : l'enregistrement est idempotent.
    const { error: payError } = await admin.from("payments").upsert(
      {
        stripe_session_id: session.id,
        customer_email: email,
        amount_total: session.amount_total,
        currency: session.currency,
        status: "paye",
      },
      { onConflict: "stripe_session_id", ignoreDuplicates: true },
    );
    if (payError) {
      console.error("stripe-webhook: insertion payments", payError);
      return new Response("Erreur d'enregistrement.", { status: 500 });
    }

    if (email && session.payment_status === "paid") {
      const { data: existing } = await admin
        .from("profiles")
        .select("id")
        .eq("email", email)
        .maybeSingle();

      // "invite" crée le compte (le déclencheur handle_new_user crée le
      // profil) ; "magiclink" sert à un élève qui a déjà un compte.
      const { data: link, error: linkError } = await admin.auth.admin.generateLink({
        type: existing ? "magiclink" : "invite",
        email,
        options: { redirectTo: REDIRECT_TO },
      });
      if (linkError || !link?.user || !link.properties?.action_link) {
        console.error("stripe-webhook: generateLink", linkError);
        return new Response("Erreur de création du compte.", { status: 500 });
      }

      const expires = new Date();
      expires.setFullYear(expires.getFullYear() + 1);
      const { error: activateError } = await admin
        .from("profiles")
        .update({
          subscription_status: "active",
          subscription_expires_at: expires.toISOString(),
          formule: session.metadata?.formule ?? "annuelle",
        })
        .eq("id", link.user.id);
      if (activateError) {
        console.error("stripe-webhook: activation", activateError);
        return new Response("Erreur d'activation.", { status: 500 });
      }

      const sent = await sendMail(
        email,
        "Bienvenue chez Justicia Académie : votre accès est activé",
        welcomeEmail(link.properties.action_link),
      );
      if (!sent) return new Response("Envoi de l'e-mail impossible.", { status: 500 });
    }
  }

  return new Response(JSON.stringify({ received: true }), {
    headers: { "Content-Type": "application/json" },
  });
});
