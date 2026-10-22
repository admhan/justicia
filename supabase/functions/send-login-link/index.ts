// Justicia Académie — envoie à un élève abonné un lien de connexion par
// e-mail (via Resend), sans mot de passe. La réponse est toujours la même,
// que l'adresse existe ou non, pour ne pas révéler qui est inscrit.

import { createClient } from "npm:@supabase/supabase-js@2";

const SITE_BASE = Deno.env.get("SITE_URL") ?? "https://justicia-fawn.vercel.app";
const REDIRECT_TO = `${SITE_BASE}/espace-eleve.html`;
const MIN_DELAY_MS = 60_000;

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });

async function sendMail(to: string, subject: string, html: string): Promise<boolean> {
  const key = Deno.env.get("RESEND_API_KEY");
  if (!key) {
    console.error("send-login-link: RESEND_API_KEY manquant");
    return false;
  }
  const from = Deno.env.get("MAIL_FROM") ?? "Justicia Académie <justicia@mail.promptheusia.com>";
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from, to: [to], subject, html }),
  });
  if (!res.ok) console.error("send-login-link: Resend", res.status, await res.text());
  return res.ok;
}

function loginEmail(link: string): string {
  return `<!doctype html><html lang="fr"><body style="margin:0;background:#F7F4EC;font-family:Georgia,serif;color:#33322D">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:32px 16px">
<table width="520" cellpadding="0" cellspacing="0" style="background:#FDFCF9;border:1px solid #C9A94E;max-width:100%">
<tr><td style="padding:28px 32px;border-bottom:3px double #16233F;font-size:22px;color:#16233F">Justicia Académie</td></tr>
<tr><td style="padding:28px 32px;font-size:16px;line-height:1.6">
<p style="margin:0 0 16px">Bonjour,</p>
<p style="margin:0 0 24px">Voici votre lien de connexion à l'espace élève. Il est valable une heure et ne sert qu'une fois.</p>
<p style="margin:0 0 24px"><a href="${link}" style="background:#16233F;color:#FDFCF9;text-decoration:none;padding:12px 24px;display:inline-block">Accéder à mon espace</a></p>
<p style="margin:0;font-size:13px;color:#5A6B87">Si vous n'êtes pas à l'origine de cette demande, ignorez simplement cet e-mail.</p>
</td></tr></table></td></tr></table></body></html>`;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: CORS_HEADERS });
  if (req.method !== "POST") return json({ error: "Méthode non autorisée." }, 405);

  let email = "";
  try {
    const body = await req.json();
    email = String(body.email ?? "").trim().toLowerCase();
  } catch {
    return json({ error: "Requête invalide." }, 400);
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254) {
    return json({ error: "Adresse e-mail invalide." }, 400);
  }

  const generic = { ok: true };
  const admin = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  const { data: profile } = await admin
    .from("profiles")
    .select("id, subscription_status")
    .eq("email", email)
    .maybeSingle();
  if (!profile || profile.subscription_status !== "active") return json(generic);

  const { data: last } = await admin
    .from("login_link_requests")
    .select("requested_at")
    .eq("email", email)
    .maybeSingle();
  if (last && Date.now() - new Date(last.requested_at).getTime() < MIN_DELAY_MS) {
    return json(generic);
  }
  await admin
    .from("login_link_requests")
    .upsert({ email, requested_at: new Date().toISOString() });

  const { data: link, error } = await admin.auth.admin.generateLink({
    type: "magiclink",
    email,
    options: { redirectTo: REDIRECT_TO },
  });
  if (error || !link?.properties?.action_link) {
    console.error("send-login-link: generateLink", error);
    return json(generic);
  }

  await sendMail(email, "Votre lien de connexion à Justicia Académie", loginEmail(link.properties.action_link));
  return json(generic);
});
