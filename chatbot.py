import json
from datetime import datetime

ESTADO_LEGAJO = "ESPERANDO_LEGAJO"
ESTADO_DIAS = "ESPERANDO_DIAS"
ESTADO_CONFIRMACION = "CONFIRMACION"

estado = ESTADO_LEGAJO
empleado_actual = None
dias_solicitados = 0


def cargar_empleados():
    with open("empleados.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def cargar_solicitudes():
    with open("solicitudes.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_solicitudes(datos):
    with open("solicitudes.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


print("=" * 50)
print("CHATBOT DE SOLICITUD DE VACACIONES")
print("=" * 50)

empleados = cargar_empleados()

while True:

    if estado == ESTADO_LEGAJO:

        legajo = input("\nIngrese su legajo (o salir): ")

        if legajo.lower() == "salir":
            break

        if not legajo.isdigit():
            print("Error: el legajo debe ser numérico.")
            continue

        encontrado = None

        for emp in empleados:
            if emp["legajo"] == int(legajo):
                encontrado = emp
                break

        if encontrado is None:
            print("Legajo inexistente.")
            continue

        empleado_actual = encontrado

        print(f"\nBienvenido {empleado_actual['nombre']}")
        print(
            f"Días disponibles: {empleado_actual['dias_disponibles']}"
        )

        estado = ESTADO_DIAS

    elif estado == ESTADO_DIAS:

        dias = input(
            "\n¿Cuántos días desea solicitar?: "
        )

        if not dias.isdigit():
            print("Debe ingresar un número.")
            continue

        dias = int(dias)

        if dias <= 0:
            print("La cantidad debe ser mayor a cero.")
            continue

        if dias > empleado_actual["dias_disponibles"]:
            print(
                f"Saldo insuficiente. Disponible: "
                f"{empleado_actual['dias_disponibles']}"
            )
            continue

        dias_solicitados = dias

        estado = ESTADO_CONFIRMACION

    elif estado == ESTADO_CONFIRMACION:

        print("\nResumen")
        print("----------------------")
        print("Empleado:", empleado_actual["nombre"])
        print("Legajo:", empleado_actual["legajo"])
        print("Días solicitados:", dias_solicitados)

        respuesta = input(
            "\n¿Confirmar solicitud? (si/no): "
        )

        if respuesta.lower() != "si":
            print("Solicitud cancelada.")
            estado = ESTADO_LEGAJO
            continue

        solicitudes = cargar_solicitudes()

        solicitud = {
            "legajo": empleado_actual["legajo"],
            "nombre": empleado_actual["nombre"],
            "dias_solicitados": dias_solicitados,
            "fecha": str(datetime.now())
        }

        if dias_solicitados > 15:
            solicitud["estado"] = "PENDIENTE_RRHH"

            print(
                "\nSolicitud enviada a RRHH "
                "para aprobación manual."
            )
        else:
            solicitud["estado"] = "APROBADA"

            print(
                "\nSolicitud aprobada automáticamente."
            )

        solicitudes.append(solicitud)

        guardar_solicitudes(solicitudes)

        print("Solicitud registrada correctamente.")

        estado = ESTADO_LEGAJO