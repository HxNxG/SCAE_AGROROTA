import { createServer, request as httpRequest } from 'node:http';
import { request as httpsRequest } from 'node:https';
import { readFile } from 'node:fs/promises';
import { extname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('.', import.meta.url));
const types = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json',
  '.png': 'image/png',
};
const backend = new URL(process.env.BACKEND_URL || 'http://127.0.0.1:8000');
const aiBackend = new URL(process.env.AI_BACKEND_URL || 'http://127.0.0.1:8000');
const aiRoutes = new Set(['/api/recomendar', '/api/aportar-datos']);

function proxyApi(req, res, requestUrl, upstreamUrl) {
  const target = new URL(upstreamUrl.origin);
  const requestBackend = target.protocol === 'https:' ? httpsRequest : httpRequest;
  target.pathname = requestUrl.pathname;
  target.search = requestUrl.search;
  const headers = {};
  for (const name of ['accept', 'content-type', 'content-length']) {
    if (req.headers[name]) headers[name] = req.headers[name];
  }

  const upstream = requestBackend(target, { method: req.method, headers }, response => {
    const contentType = response.headers['content-type'] || 'application/json';
    res.writeHead(response.statusCode, { 'Content-Type': contentType });
    response.on('error', error => res.destroy(error));
    response.pipe(res);
  });
  upstream.setTimeout(15000, () => upstream.destroy());
  upstream.on('error', () => {
    if (res.destroyed) return;
    if (res.headersSent) {
      res.destroy();
      return;
    }
    res.writeHead(502, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ detail: 'El servicio de BioTinder no está disponible.' }));
  });
  res.on('close', () => {
    if (!res.writableFinished) upstream.destroy();
  });
  req.on('error', () => upstream.destroy());
  req.pipe(upstream);
}

createServer(async (req, res) => {
  try {
    const requestUrl = new URL(req.url, 'http://localhost');
    if (aiRoutes.has(requestUrl.pathname) || requestUrl.pathname.startsWith('/api/v1/')) {
      proxyApi(req, res, requestUrl, aiRoutes.has(requestUrl.pathname) ? aiBackend : backend);
      return;
    }
    const pathname = decodeURIComponent(requestUrl.pathname);
    const file = resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
    if (!file.startsWith(root.endsWith(sep) ? root : root + sep)) throw new Error('invalid path');
    const content = await readFile(file);
    res.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream' });
    res.end(content);
  } catch {
    res.writeHead(404);
    res.end('No encontrado');
  }
}).listen(process.env.PORT || 5173, '127.0.0.1', () => console.log(`BioTinder: http://127.0.0.1:${process.env.PORT || 5173}`));
