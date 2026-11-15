import { mountRecommendations } from './src/components/recommendations.js';

const section = document.querySelector('#recommendations');
try {
  const response = await fetch(new URL('./pimocha-demo.json', import.meta.url));
  if (!response.ok) throw new Error('Demo no disponible');
  const data = await response.json();
  section.replaceChildren();
  mountRecommendations(section, data);
} catch {
  const message = document.createElement('p');
  message.setAttribute('role', 'status');
  message.textContent = 'No se pudo abrir el ejemplo. Recarga la página.';
  section.replaceChildren(message);
}
