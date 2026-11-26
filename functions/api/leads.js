const CRM_BASE = "https://tsdigitais-central-astro.tiagocxs-tdb.workers.dev";
const CRM_FORM_ID = "bbf61b2cbd9e4c4ba39c913c7bf9b8fc";
const VERIFIED_ORIGIN = "https://brunoviniciusinteriordesign.tsdigitais.com";

export async function onRequestPost({ request }) {
  try {
    const body = await request.json();
    const name = String(body.name || "").trim().slice(0, 160);
    const email = String(body.email || "").trim().toLowerCase().slice(0, 254);
    const type = String(body.type || "").trim().slice(0, 160);
    const message = String(body.message || "").trim().slice(0, 5000);

    if (!name || !email || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return Response.json({ success: false, error: "Informe nome, e-mail válido e mensagem." }, { status: 400 });
    }

    const sourceUrl = request.headers.get("referer") || VERIFIED_ORIGIN + "/";
    const referrerUrl = request.headers.get("referer") || "";

    const response = await fetch(CRM_BASE + "/api/public/forms/" + CRM_FORM_ID + "/submissions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        data: { name, email, type, message },
        sourceUrl,
        referrerUrl,
        parentOrigin: VERIFIED_ORIGIN,
      }),
      signal: AbortSignal.timeout(15000),
    });

    const result = await response.json().catch(() => ({}));
    if (!response.ok || result.ok !== true) {
      return Response.json(
        { success: false, error: result.error || "Não foi possível registrar sua mensagem no CRM." },
        { status: 502 },
      );
    }

    return Response.json({
      success: true,
      crmSynced: true,
      submissionId: result.submissionId || null,
      notifications: result.notifications || {},
    });
  } catch (error) {
    console.error("Bruno contact form CRM error:", error);
    return Response.json({ success: false, error: "Não foi possível registrar sua mensagem. Tente novamente." }, { status: 502 });
  }
}
