async function post(path, payload) {
  let response;
  try {
    response = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  } catch {
    throw new Error('No se pudo conectar con el servidor.');
  }
  if (response.status === 502) throw new Error('El servidor de recomendaciones no está disponible.');
  if (!response.ok) throw new Error(`La API no pudo completar la solicitud (HTTP ${response.status}).`);
  return response.json();
}

export const recommend = payload => post('/api/recomendar', payload);
export const submitObservation = payload => post('/api/aportar-datos', payload);
