# Consultas en vivo desde GitHub Pages

El mapa público de BioTinder usa archivos estáticos. Render solo necesita ejecutar la API de recomendaciones. El ejemplo etiquetado de Pimocha queda disponible aunque no se haya configurado un servicio.

1. Abre [Deploy to Render](https://render.com/deploy?repo=https%3A%2F%2Fgithub.com%2FHxNxG%2FSCAE_AGROROTA), inicia sesión y revisa el Blueprint antes de aplicarlo. El archivo [render.yaml](../render.yaml) define un servicio Python en el plan Free. Asegúrate de que la pantalla de Render indique **Free** antes de crear el servicio.
2. Copia la URL HTTPS que Render asigna al servicio. Abre `/healthz` en esa URL y comprueba que devuelva `{"status":"ok"}`. Usa esa misma URL base, sin `/docs` ni `/api/recomendar`.
3. Crea una variable de repositorio llamada `BIOTINDER_API_URL` en [Settings → Secrets and variables → Actions → Variables](https://github.com/HxNxG/SCAE_AGROROTA/settings/variables/actions). Pega la URL base del servicio, como `https://biotinder-fastapi.onrender.com` si Render asignó exactamente ese dominio.
4. Ejecuta [BioTinder Pages](https://github.com/HxNxG/SCAE_AGROROTA/actions/workflows/pages.yml) desde `main`. Abre el [sitio público](https://hxnxg.github.io/SCAE_AGROROTA/), completa el cuestionario y prueba dos sectores o escenarios. Cada consulta debe mostrar el sector enviado, con tres estrategias y 18 meses de simulación por estrategia.

El navegador solicita `POST /api/recomendar` en el servicio externo. La configuración de Render permite el origen `https://hxnxg.github.io` y desactiva el registro de observaciones. La URL de la API es pública. Nunca pongas un token o clave en esa variable. La versión local conserva su flujo de observaciones.

Una instancia gratuita se suspende tras 15 minutos sin tráfico. La primera consulta posterior puede tardar alrededor de un minuto. El plan no ofrece disco persistente. [Límites del plan Free](https://render.com/docs/free)

Si retiras la variable y vuelves a ejecutar el workflow, la página vuelve al modo de mapa y ejemplo guardado. GitHub Pages no necesita cambios para seguir mostrando las capas climáticas.
