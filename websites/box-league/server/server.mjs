/**
 * BOX LEAGUE optional signaling server. Node.js >= 22. No npm packages.
 * Only opaque AES-GCM-encrypted invitations/answers are stored, in memory.
 * No game packets, database, account system, telemetry or room listing.
 * Public use: HTTPS reverse proxy, ALLOWED_ORIGINS, capacity/rate limiting.
 */
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { createHash, timingSafeEqual } from 'node:crypto';

const port = Number(process.env.PORT || 8787);
const host = process.env.HOST || '127.0.0.1';
const ttl = 10 * 60 * 1000;
const maxRooms = Number(process.env.MAX_ROOMS || 200);
const allowed = (process.env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
const rooms = new Map();
const limits = new Map();
const tokenRE = /^[A-Za-z0-9_-]{32}$/;
const blobRE = /^[A-Za-z0-9_-]{16}\.[A-Za-z0-9_-]{20,119980}$/;
const hash = value => createHash('sha256').update(value).digest();
const equal = (value, expected) => timingSafeEqual(hash(value), expected);
const game = await readFile(new URL('../public/index.html', import.meta.url));

function reply(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(data));
}
function collect(req) {
  return new Promise((resolve, reject) => {
    let size = 0, chunks = [];
    req.on('data', chunk => {
      size += chunk.length;
      if (size > 130000) { chunks = []; reject(Object.assign(new Error('Payload too large'), { status: 413 })); req.resume(); }
      else chunks.push(chunk);
    });
    req.on('end', () => {
      try { resolve(JSON.parse(Buffer.concat(chunks).toString('utf8'))); }
      catch { reject(Object.assign(new Error('Invalid JSON'), { status: 400 })); }
    });
    req.on('error', reject);
  });
}
function limited(req) {
  // Deliberately ignore user-controlled X-Forwarded-For.
  const ip = req.socket.remoteAddress || 'unknown', now = Date.now();
  let bucket = limits.get(ip);
  if (!bucket || now - bucket.at > 60000) {
    if (!bucket && limits.size >= 5000) return true;
    bucket = { at: now, requests: 0, creates: 0 };
    limits.set(ip, bucket);
  }
  bucket.requests++;
  if (req.method === 'POST') bucket.creates++;
  return bucket.requests > 240 || bucket.creates > 20;
}
const server = http.createServer(async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'no-referrer');
  res.setHeader('Cross-Origin-Resource-Policy', 'cross-origin');
  const origin = req.headers.origin;
  if (origin) {
    if (allowed.length && !allowed.includes(origin)) return reply(res, 403, { error: 'Origin not allowed' });
    res.setHeader('Access-Control-Allow-Origin', allowed.length ? origin : '*');
    res.setHeader('Vary', 'Origin');
    res.setHeader('Access-Control-Allow-Headers', 'Authorization, Content-Type');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  }
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  let pathname;
  try { pathname = new URL(req.url, 'http://localhost').pathname; }
  catch { return reply(res, 400, { error: 'Invalid path' }); }
  if (req.method === 'GET' && (pathname === '/' || pathname === '/index.html')) {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Content-Length': game.length }); res.end(game); return;
  }
  if (req.method === 'GET' && pathname === '/health') return reply(res, 200, { app: 'BOX-LEAGUE-SIGNAL', version: 1, ttlSeconds: ttl / 1000 });
  if (limited(req)) return reply(res, 429, { error: 'Rate limit' });
  const match = /^\/signal\/([A-Za-z0-9_-]{22})$/.exec(pathname);
  if (!match) return reply(res, 404, { error: 'Not found' });
  const id = match[1], token = (req.headers.authorization || '').replace(/^Bearer /, '');
  if (!tokenRE.test(token)) return reply(res, 401, { error: 'Authorization required' });
  let room = rooms.get(id);
  if (room && room.expires <= Date.now()) { rooms.delete(id); room = null; }
  try {
    if (req.method === 'POST') {
      if (room) return reply(res, 409, { error: 'Room exists' });
      if (rooms.size >= maxRooms) return reply(res, 429, { error: 'Capacity reached' });
      const body = await collect(req);
      if (!body || !tokenRE.test(body.guest) || body.guest === token || typeof body.offer !== 'string' || !blobRE.test(body.offer)) return reply(res, 400, { error: 'Invalid invitation' });
      // Recheck after asynchronous body collection to avoid create races.
      if (rooms.has(id)) return reply(res, 409, { error: 'Room exists' });
      if (rooms.size >= maxRooms) return reply(res, 429, { error: 'Capacity reached' });
      room = { host: hash(token), guest: hash(body.guest), offer: body.offer, answer: null, expires: Date.now() + ttl };
      rooms.set(id, room);
      return reply(res, 201, { ok: true, expires: room.expires });
    }
    if (!room) return reply(res, 404, { error: 'Room expired or missing' });
    const isHost = equal(token, room.host), isGuest = equal(token, room.guest);
    if (!isHost && !isGuest) return reply(res, 404, { error: 'Room expired or missing' });
    if (req.method === 'GET') return reply(res, 200, isHost ? { answer: room.answer, expires: room.expires } : { offer: room.offer, answered: !!room.answer, expires: room.expires });
    if (req.method === 'DELETE' && isHost) { rooms.delete(id); return reply(res, 200, { ok: true }); }
    if (req.method === 'PUT' && isGuest) {
      const body = await collect(req);
      if (!body || typeof body.answer !== 'string' || !blobRE.test(body.answer)) return reply(res, 400, { error: 'Invalid answer' });
      if (rooms.get(id) !== room || room.expires <= Date.now()) return reply(res, 404, { error: 'Room expired or missing' });
      if (room.answer && room.answer !== body.answer) return reply(res, 409, { error: 'Room already joined' });
      room.answer = body.answer;
      return reply(res, 200, { ok: true });
    }
    return reply(res, 405, { error: 'Method not permitted' });
  } catch (error) {
    if (!res.headersSent) reply(res, error.status || 500, { error: error.status ? error.message : 'Request failed' });
  }
});
server.requestTimeout = 20000;
server.headersTimeout = 10000;
server.maxRequestsPerSocket = 300;
setInterval(() => {
  const now = Date.now();
  for (const [id, room] of rooms) if (room.expires <= now) rooms.delete(id);
  for (const [id, limit] of limits) if (now - limit.at > 60000) limits.delete(id);
}, 30000).unref();
server.listen(port, host, () => console.log(`BOX LEAGUE: http://${host}:${port} (use HTTPS reverse proxy for public use)`));
for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => { rooms.clear(); server.close(() => process.exit(0)); setTimeout(() => process.exit(1), 3000).unref(); });
