# client_api.py
import argparse
import json
import sys
from typing import Dict, Optional

import requests


def get_tokens(base: str, username: str, password: str, timeout=10) -> Dict[str, str]:
    url = f"{base}/api/token/"
    r = requests.post(url, json={"username": username, "password": password}, timeout=timeout)
    if r.status_code != 200:
        raise SystemExit(f"[token] {r.status_code}: {r.text}")
    data = r.json()
    return {"access": data["access"], "refresh": data["refresh"]}


def refresh_access(base: str, refresh: str, timeout=10) -> str:
    url = f"{base}/api/token/refresh/"
    r = requests.post(url, json={"refresh": refresh}, timeout=timeout)
    if r.status_code != 200:
        raise SystemExit(f"[refresh] {r.status_code}: {r.text}")
    return r.json()["access"]


def auth_headers(access: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {access}"}


def get_my_profile(base: str, access: str, timeout=10) -> requests.Response:
    url = f"{base}/api/perfiles/me/"
    return requests.get(url, headers=auth_headers(access), timeout=timeout)


def patch_my_profile(base: str, access: str, payload: Dict, timeout=10) -> requests.Response:
    url = f"{base}/api/perfiles/me/"
    return requests.patch(url, headers={**auth_headers(access), "Content-Type": "application/json"},
                          json=payload, timeout=timeout)


def pretty(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Cliente sencillo para la API de Campus (DRF + JWT).")
    parser.add_argument("--base", default="http://127.0.0.1:8000", help="Base URL del backend (sin slash final)")
    parser.add_argument("--username", required=True, help="Usuario")
    parser.add_argument("--password", required=True, help="Contraseña")
    parser.add_argument("--patch", default=None,
                        help="JSON con campos a actualizar en tu perfil (ej: '{\"carrera\":\"Informática\",\"semestre\":6}')")
    args = parser.parse_args()

    # 1) Obtener tokens
    tokens = get_tokens(args.base, args.username, args.password)
    access = tokens["access"]
    refresh = tokens["refresh"]

    # 2) GET /me (con un refresco automático si expira)
    r = get_my_profile(args.base, access)
    if r.status_code == 401:
        # access vencido: refrescar y reintentar una vez
        access = refresh_access(args.base, refresh)
        r = get_my_profile(args.base, access)
    if r.status_code != 200:
        raise SystemExit(f"[GET /me] {r.status_code}: {r.text}")

    print("=== Perfil (GET /api/perfiles/me/) ===")
    pretty(r.json())

    # 3) PATCH opcional
    if args.patch:
        try:
            payload = json.loads(args.patch)
        except json.JSONDecodeError as e:
            raise SystemExit(f"JSON inválido en --patch: {e}")

        r = patch_my_profile(args.base, access, payload)
        if r.status_code == 401:
            access = refresh_access(args.base, refresh)
            r = patch_my_profile(args.base, access, payload)

        if r.status_code not in (200, 202):
            raise SystemExit(f"[PATCH /me] {r.status_code}: {r.text}")

        print("\n=== Perfil actualizado (PATCH /api/perfiles/me/) ===")
        pretty(r.json())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
