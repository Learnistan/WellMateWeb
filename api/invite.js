// Vercel serverless function — receives invite requests from the site and
// emails them to the team. Set RESEND_API_KEY in the Vercel project settings
// (Settings → Environment Variables) and this goes live; until then the site
// falls back to opening the visitor's mail app.
const TO = 'admin@learnistan.ai';
const FROM = 'WellMate <onboarding@resend.dev>'; // swap for a verified domain sender

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }
  if (!process.env.RESEND_API_KEY) {
    // Not configured yet — tell the client so it can fall back to mailto.
    return res.status(503).json({ error: 'Email not configured' });
  }

  let payload = req.body;
  if (typeof payload === 'string') {
    try { payload = JSON.parse(payload); } catch (e) { payload = {}; }
  }
  const { name = '', contact = '', language = '', message = '' } = payload || {};
  const clean = s => String(s).slice(0, 2000);

  if (clean(name).trim().length < 2 || !clean(contact).trim()) {
    return res.status(400).json({ error: 'Name and contact are required' });
  }

  const text =
    `New WellMate invite request\n\n` +
    `Name:     ${clean(name)}\n` +
    `Contact:  ${clean(contact)}\n` +
    `Language: ${clean(language)}\n\n` +
    `${clean(message) || '(no message)'}\n`;

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: FROM,
        to: [TO],
        reply_to: /\S+@\S+\.\S+/.test(clean(contact)) ? clean(contact) : undefined,
        subject: `WellMate invite request — ${clean(name)}`,
        text
      })
    });
    if (!r.ok) {
      const detail = await r.text();
      console.error('Resend rejected the request:', detail);
      return res.status(502).json({ error: 'Upstream email provider failed' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Invite send failed:', err);
    return res.status(500).json({ error: 'Send failed' });
  }
};
