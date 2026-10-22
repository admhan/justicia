// Justicia Académie — crée une session de paiement Stripe pour la formule
// (250 €, paiement unique, accès pour l'année). Le bouton "Réserver ma place"
// de index.html appelle cette fonction et redirige vers l'URL renvoyée.
//
// Déploiement et configuration : voir AUTH-SETUP.md, section Stripe.

import Stripe from "npm:stripe@17.7.0";

// Prix créé dans Stripe (mode test). En production, définir le secret
// STRIPE_PRICE_ID avec l'identifiant du prix live : le code n'a pas à changer.
const DEFAULT_PRICE_ID = "price_1UTGR9QtGUTsMKkWDJWCIzdX";

const ALLOWED_ORIGINS = [
  "https://www.justicia-academie.com",
  "https://justicia-academie.com",
  "https://justicia-fawn.vercel.app",
  "https://admhan.github.io",
];

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: CORS_HEADERS });
  }

  const stripeSecretKey = Deno.env.get("STRIPE_SECRET_KEY");
  if (!stripeSecretKey) {
    return new Response(
      JSON.stringify({ error: "Paiement pas encore configuré." }),
      { status: 503, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } },
    );
  }

  const stripe = new Stripe(stripeSecretKey, { apiVersion: "2024-06-20" });

  // Retour après paiement : uniquement vers un domaine du site, pour qu'un
  // tiers ne puisse pas faire rediriger un acheteur vers une page piégée.
  const requestOrigin = req.headers.get("origin") ?? "";
  const siteBase = ALLOWED_ORIGINS.includes(requestOrigin)
    ? requestOrigin + (requestOrigin.includes("github.io") ? "/justicia" : "")
    : (Deno.env.get("SITE_URL") ?? "https://justicia-fawn.vercel.app");

  try {
    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      locale: "fr",
      line_items: [
        { price: Deno.env.get("STRIPE_PRICE_ID") ?? DEFAULT_PRICE_ID, quantity: 1 },
      ],
      // L'e-mail saisi ici sert à créer et activer le compte élève (webhook).
      customer_creation: "always",
      billing_address_collection: "auto",
      allow_promotion_codes: true,
      metadata: { formule: "annuelle" },
      custom_text: {
        submit: {
          message:
            `En payant, vous acceptez les [conditions générales de vente](${siteBase}/cgv.html) et demandez l'accès immédiat à votre espace élève.`,
        },
      },
      success_url: `${siteBase}/index.html?paiement=succes#formules`,
      cancel_url: `${siteBase}/index.html?paiement=annule#formules`,
    });

    return new Response(JSON.stringify({ url: session.url }), {
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("create-checkout-session:", error);
    return new Response(
      JSON.stringify({ error: "Impossible de créer la session de paiement." }),
      { status: 500, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } },
    );
  }
});
