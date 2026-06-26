"""
Simulador de consola — Chatbot de Vacaciones
TechSolutions S.A. | Organización Empresarial | TUP UTN
Repositorio: https://github.com/IgnacioMerlo/Tpi-chatbot-vacaciones-IM

Base de datos : empleados.json + solicitudes.json
Ejecutar      : python chatbot.py
"""

import json
import os
from datetime import date

# ── Rutas de archivos ─────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
EMPLEADOS_PATH  = os.path.join(BASE_DIR, "empleados.json")
SOLICITUDES_PATH= os.path.join(BASE_DIR, "solicitudes.json")

# ── Límites de robustez ───────────────────────────────────────────────────────
MAX_INT_LEGAJO = 3   # intentos máximos para legajo inválido   (robustez 9.1 / 9.3)
MAX_INT_DIAS   = 5   # intentos máximos para días inválidos    (robustez 9.3)


# ══════════════════════════════════════════════════════════════════════════════
# ACCESO A LA BASE DE DATOS (JSON)
# ══════════════════════════════════════════════════════════════════════════════

def cargar_empleados():
    with open(EMPLEADOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_empleados(data):
    with open(EMPLEADOS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def cargar_solicitudes():
    with open(SOLICITUDES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_solicitudes(data):
    with open(SOLICITUDES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def obtener_empleado(legajo: int):
    """Busca un empleado por legajo. Retorna dict o None."""
    for emp in cargar_empleados():
        if emp["legajo"] == legajo:
            return emp
    return None

def registrar_solicitud(legajo, nombre, dias, resultado, requiere_rrhh):
    """
    Registra la solicitud en solicitudes.json y
    descuenta los días del empleado en empleados.json.
    Retorna el ID de solicitud generado.
    """
    solicitudes = cargar_solicitudes()
    id_sol = f"SOL-{len(solicitudes)+1:04d}"

    solicitudes.append({
        "id_solicitud":  id_sol,
        "legajo":        legajo,
        "nombre":        nombre,
        "dias_solicitados": dias,
        "fecha_solicitud":  date.today().isoformat(),
        "resultado":     resultado,
        "requiere_rrhh": "Sí" if requiere_rrhh else "No",
    })
    guardar_solicitudes(solicitudes)

    # Descontar días del empleado si la solicitud fue aceptada
    if resultado in ("APROBADO", "PENDIENTE_RRHH"):
        empleados = cargar_empleados()
        for emp in empleados:
            if emp["legajo"] == legajo:
                emp["dias_disponibles"] = max(0, emp["dias_disponibles"] - dias)
                break
        guardar_empleados(empleados)

    return id_sol


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS DE PRESENTACIÓN
# ══════════════════════════════════════════════════════════════════════════════

def sep():
    print("\n" + "-" * 52)

def bot(msg):
    print("\n[BOT]  " + msg)

def encabezado():
    sep()
    print("  BOT DE VACACIONES — TechSolutions S.A.")
    sep()
    print("""
  Comandos disponibles en cualquier momento:
    /cancelar  →  cancela la operación actual
    /start     →  reinicia el proceso desde el inicio

  Empleados de prueba:
    1001 Juan Pérez       (15 días)
    1002 María Gómez      (10 días)
    1003 Pedro Fernández  ( 0 días — sin saldo)
    1004 Ana López        (20 días)
    1005 Carlos Ruiz      ( 5 días)
""")


# ══════════════════════════════════════════════════════════════════════════════
# MÁQUINA DE ESTADOS — FLUJO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def correr_flujo():
    """
    Ejecuta el flujo completo del chatbot siguiendo el BPMN TO-BE:

    INICIO
      ↓
    ESPERANDO_LEGAJO    ← GW1: ¿Legajo existe? (con bucle de reintento)
      ↓
    ESPERANDO_CANT_DIAS ← GW2: ¿Formato válido? / GW3: ¿Saldo suficiente?
      ↓
    CONFIRMANDO
      ↓
    REGISTRANDO
      ↓
    FIN_APROBADO / FIN_PENDIENTE_RRHH   ← GW4: ¿Supera 15 días?
    """

    # ── ESTADO: ESPERANDO_LEGAJO ──────────────────────────────────────────────
    sep()
    bot("¡Hola! Ingresá tu número de legajo para comenzar:")

    int_legajo = 0
    empleado   = None

    while True:
        entrada = input("\n👤  Legajo: ").strip()

        # Comandos globales
        if entrada == "/cancelar":
            bot("❌ Operación cancelada.")
            return
        if entrada == "/start":
            bot("🔄 Reiniciando...")
            correr_flujo()
            return

        # ── GW1 — Robustez 9.3: dato no numérico ─────────────────────────────
        if not entrada.isdigit():
            int_legajo += 1
            print(f"\n⚠️   El legajo debe ser un número entero. Ejemplo: 1002")
            print(f"     (Intento {int_legajo} de {MAX_INT_LEGAJO})")
            if int_legajo >= MAX_INT_LEGAJO:
                bot("⛔ Superaste el límite de intentos. Sesión bloqueada.\n"
                    "   Escribí /start para intentarlo de nuevo.")
                return
            continue

        legajo = int(entrada)

        # ── GW1 — Robustez 9.1: legajo inexistente ───────────────────────────
        empleado = obtener_empleado(legajo)
        if empleado is None:
            int_legajo += 1
            print(f"\n❌  El legajo {legajo} no está registrado en el sistema.")
            print(f"     (Intento {int_legajo} de {MAX_INT_LEGAJO})")
            if int_legajo >= MAX_INT_LEGAJO:
                bot("⛔ Legajo no encontrado 3 veces. Sesión bloqueada.\n"
                    "   Escribí /start para intentarlo de nuevo.")
                return
            continue

        # Robustez: saldo agotado
        if empleado["dias_disponibles"] == 0:
            bot(f"✅ Empleado: {empleado['nombre']} — Área: {empleado['area']}\n"
                f"\n   😔 No tenés días disponibles para vacaciones.\n"
                f"   Comunicate con RRHH para más información.")
            return

        # ── Legajo válido ─────────────────────────────────────────────────────
        bot(f"✅ Empleado verificado\n"
            f"   👤  {empleado['nombre']} — Área: {empleado['area']}\n"
            f"   📅  Días disponibles: {empleado['dias_disponibles']}")
        break

    # ── ESTADO: ESPERANDO_CANTIDAD_DIAS ──────────────────────────────────────
    bot("¿Cuántos días de vacaciones querés solicitar?")

    int_dias     = 0
    dias_pedidos = None
    saldo        = empleado["dias_disponibles"]

    while True:
        entrada = input("\n📅  Días: ").strip()

        if entrada == "/cancelar":
            bot("❌ Operación cancelada.")
            return
        if entrada == "/start":
            bot("🔄 Reiniciando...")
            correr_flujo()
            return

        # ── GW2 — Robustez 9.3: dato no numérico ─────────────────────────────
        if not entrada.lstrip("-").isdigit():
            int_dias += 1
            print(f"\n⚠️   La cantidad debe ser un número entero mayor a cero. Ejemplo: 5")
            print(f"     (Intento {int_dias} de {MAX_INT_DIAS})")
            if int_dias >= MAX_INT_DIAS:
                bot("⛔ Demasiados intentos inválidos. Sesión cancelada.\n"
                    "   Escribí /start para comenzar de nuevo.")
                return
            continue

        dias = int(entrada)

        # ── GW2 — valor cero o negativo ───────────────────────────────────────
        if dias <= 0:
            print("\n⚠️   La cantidad de días debe ser mayor a cero.")
            continue

        # ── GW3 — Robustez 9.2: saldo insuficiente ───────────────────────────
        if dias > saldo:
            print(f"\n❌  Saldo insuficiente.")
            print(f"     Pediste {dias} días pero tenés {saldo} disponibles.")
            print(f"     Ingresá una cantidad ≤ {saldo} o escribí /cancelar para salir.")
            continue

        dias_pedidos = dias
        break

    # ── ESTADO: CONFIRMANDO ───────────────────────────────────────────────────
    requiere_rrhh = dias_pedidos > 15
    nota = (
        "⚠️  SUPERA 15 DÍAS → Será enviada al jefe de área para\n"
        "       aprobación manual. (Lane RRHH del BPMN)"
        if requiere_rrhh else
        "✅  Será APROBADA AUTOMÁTICAMENTE."
    )

    sep()
    print(f"""
  📋  RESUMEN DE SOLICITUD
  ──────────────────────────────────
  👤  Empleado  : {empleado['nombre']}
  🏢  Área      : {empleado['area']}
  📅  Días ped. : {dias_pedidos}
  💼  Saldo     : {saldo} días disponibles

  {nota}
""")

    while True:
        conf = input("  ¿Confirmás? (s = confirmar / n = cancelar): ").strip().lower()

        if conf in ("n", "/cancelar"):
            bot("❌ Solicitud cancelada.")
            return
        if conf == "/start":
            bot("🔄 Reiniciando...")
            correr_flujo()
            return
        if conf != "s":
            print("  Por favor ingresá 's' para confirmar o 'n' para cancelar.")
            continue
        break

    # ── ESTADO: REGISTRANDO ───────────────────────────────────────────────────
    resultado = "PENDIENTE_RRHH" if requiere_rrhh else "APROBADO"
    id_sol    = registrar_solicitud(
        legajo        = empleado["legajo"],
        nombre        = empleado["nombre"],
        dias          = dias_pedidos,
        resultado     = resultado,
        requiere_rrhh = requiere_rrhh,
    )

    # ── FIN ───────────────────────────────────────────────────────────────────
    sep()
    if requiere_rrhh:
        # FIN_PENDIENTE_RRHH — GW4: supera 15 días
        bot(f"📨 Solicitud registrada — ID: {id_sol}\n"
            f"\n   Tu solicitud de {dias_pedidos} días fue enviada al jefe de\n"
            f"   {empleado['area']} para aprobación manual.\n"
            f"   Recibirás respuesta por correo electrónico.")
    else:
        # FIN_APROBADO — GW4: hasta 15 días
        saldo_nuevo = saldo - dias_pedidos
        bot(f"🎉 ¡Solicitud APROBADA! — ID: {id_sol}\n"
            f"\n   Días aprobados  : {dias_pedidos}\n"
            f"   Saldo restante  : {saldo_nuevo} días\n"
            f"   ¡Que disfrutes tus vacaciones! 🏖️")


# ══════════════════════════════════════════════════════════════════════════════
# ENTRADA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def main():
    encabezado()
    while True:
        correr_flujo()
        print()
        otra = input("  ¿Querés hacer otra consulta? (s/n): ").strip().lower()
        if otra != "s":
            bot("¡Hasta luego! 👋")
            break
        sep()


if __name__ == "__main__":
    main()