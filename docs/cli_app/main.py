import json
import getpass
from pathlib import Path
import sys

# Permite importar cliente_api.py desde docs
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cliente_api import get_tokens, refresh_access, get_my_profile, patch_my_profile  # reutilizamos funciones

BASE_URL = "http://127.0.0.1:8000"

def pause():
    input("\n[Enter] para continuar...")

def pedir_credenciales():
    print("== Login ==")
    username = input("Usuario: ").strip()
    password = getpass.getpass("Contraseña: ")
    return username, password

def mostrar_perfil(base, access):
    r = get_my_profile(base, access)
    if r.status_code == 200:
        print("\n=== Tu perfil ===")
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
        return True
    elif r.status_code == 401:
        print("error Access token vencido.")
        return False
    else:
        print(f"Error [{r.status_code}]: {r.text}")
        return None

def editar_perfil(base, access):
    print("\n== Editar perfil (deja vacío para no cambiar) ==")
    carrera = input("Nueva carrera: ").strip()
    semestre = input("Nuevo semestre (número): ").strip()
    notas = {}
    for i in range(1,5):
        v = input(f"Nota{i} (ej 6.2): ").strip()
        if v:
            try:
                notas[f"nota{i}"] = float(v)
            except ValueError:
                print(f"  - '{v}' no es número válido, se ignora.")

    payload = {}
    if carrera: payload["carrera"] = carrera
    if semestre:
        try:
            payload["semestre"] = int(semestre)
        except ValueError:
            print("  - semestre inválido, se ignora.")
    payload.update(notas)

    if not payload:
        print("No hay cambios.")
        return True

    r = patch_my_profile(base, access, payload)
    if r.status_code in (200, 202):
        print("\n=== Perfil actualizado ===")
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
        return True
    elif r.status_code == 401:
        print(" Access token vencido.")
        return False
    else:
        print(f"Error [{r.status_code}]: {r.text}")
        return None

def main():
    base = BASE_URL
    print("== Cliente de API Campus (DRF + JWT) ==")
    username, password = pedir_credenciales()

    # 1) tokens
    try:
        tokens = get_tokens(base, username, password)
        access, refresh = tokens["access"], tokens["refresh"]
    except SystemExit as e:
        print(e)
        return

    while True:
        print("\nMenú:")
        print("  1) Ver mi perfil")
        print("  2) Editar mi perfil (carrera/semestre/notas)")
        print("  3) Refrescar access token")
        print("  0) Salir")
        op = input("Opción: ").strip()

        if op == "1":
            ok = mostrar_perfil(base, access)
            if ok is False:  # 401
                try:
                    access = refresh_access(base, refresh)
                    print("Access token renovado. Reintentando...")
                    mostrar_perfil(base, access)
                except SystemExit as e:
                    print(e)
            pause()

        elif op == "2":
            ok = editar_perfil(base, access)
            if ok is False:  # 401
                try:
                    access = refresh_access(base, refresh)
                    print("Access token renovado. Reintentando...")
                    editar_perfil(base, access)
                except SystemExit as e:
                    print(e)
            pause()

        elif op == "3":
            try:
                access = refresh_access(base, refresh)
                print("Access token renovado.")
            except SystemExit as e:
                print(e)
            pause()

        elif op == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
