"""Inicio de sesion local: nunca pasar credenciales como argumentos."""
import json
from datetime import datetime, timezone
from pathlib import Path

import earthaccess


def main():
    print('Introduce tus credenciales solo en esta terminal local.')
    print('La biblioteca guardara el acceso en _netrc/.netrc de tu perfil, fuera del repositorio.')
    auth = earthaccess.login(strategy='interactive', persist=True)
    if not auth.authenticated:
        raise SystemExit('No se pudo autenticar. No se guardara un estado exitoso.')
    target = Path(__file__).parent / 'metadatos' / 'autenticacion_estado.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps({
        'authenticated_at_utc': datetime.now(timezone.utc).isoformat(),
        'earthdata_login_verified': True,
        'note': 'No contiene credenciales. No confirma acceso a todos los servicios ni descarga de datos.'
    }, indent=2), encoding='utf-8')
    print('Autenticacion correcta. Puedes avisar a Codex para continuar.')


if __name__ == '__main__':
    main()
