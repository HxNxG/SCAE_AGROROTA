async function post(path, payload, apiOrigin) {
  const hosted = Boolean(apiOrigin);
  let response;
  try {
    response = await fetch(hosted ? new URL(path, apiOrigin) : path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      ...(hosted && {
        credentials: 'omit',
        signal: AbortSignal.timeout(90_000),
      }),
    });
  } catch (error) {
    if (hosted) {
      throw new Error(error.name === 'TimeoutError'
        ? 'El servicio todavía está arrancando. Pulsa Generar diagnóstico para reintentar.'
        : 'No se pudo conectar con el motor de recomendaciones. Comprueba tu conexión y reintenta.');
    }
    throw new Error('No se pudo conectar con el servidor.');
  }
  if (hosted && [502, 503, 504].includes(response.status)) {
    throw new Error('El motor de recomendaciones no está disponible. Espera un momento y reintenta.');
  }
  if (response.status === 502) throw new Error('El servidor de recomendaciones no está disponible.');
  if (!response.ok) throw new Error(`La API no pudo completar la solicitud (HTTP ${response.status}).`);
  try {
    return await response.json();
  } catch {
    throw new Error(hosted
      ? 'El servicio todavía está arrancando o no devolvió un resultado válido. Espera un momento y reintenta.'
      : 'El servidor no devolvió un resultado válido.');
  }
}

export const recommend = (payload, apiOrigin) => post('/api/recomendar', payload, apiOrigin);
export const submitObservation = payload => post('/api/aportar-datos', payload);
