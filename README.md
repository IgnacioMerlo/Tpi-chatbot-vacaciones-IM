# Chatbot de Solicitud de Vacaciones

## Trabajo Práctico Integrador - Organización Empresarial

**Alumno:** Ignacio Merlo

**Carrera:** Tecnicatura Universitaria en Programación a Distancia (TUPaD)

**Universidad:** Universidad Tecnológica Nacional (UTN)

---

## Descripción del Proyecto

Este proyecto automatiza el proceso de solicitud de vacaciones mediante un chatbot desarrollado en Python.

La solución fue diseñada a partir de un modelo BPMN 2.0 que representa el proceso administrativo de gestión de vacaciones dentro de una organización ficticia llamada TechSolutions S.A.

El chatbot permite validar empleados, consultar saldo disponible de días de vacaciones, registrar solicitudes y gestionar diferentes escenarios de error.

---

## Objetivos

* Automatizar un proceso administrativo.
* Aplicar BPMN 2.0 para modelar procesos de negocio.
* Implementar una máquina de estados.
* Simular una base de datos de empleados.
* Registrar solicitudes de vacaciones.
* Gestionar caminos alternativos y casos de excepción.

---

## Funcionalidades

### Validación de Legajo

El sistema verifica que el legajo exista en la base de datos simulada.

### Consulta de Saldo

Permite visualizar la cantidad de días disponibles para cada empleado.

### Solicitud de Vacaciones

El usuario puede ingresar la cantidad de días deseados.

### Validación de Reglas de Negocio

* Legajo válido.
* Cantidad de días numérica.
* Cantidad mayor a cero.
* Saldo suficiente.

### Registro de Solicitudes

Las solicitudes se almacenan en el archivo:

```text
solicitudes.json
```

### Manejo de Errores

El chatbot contempla:

* Legajos inexistentes.
* Datos no numéricos.
* Cantidades inválidas.
* Saldo insuficiente.
* Cancelación de solicitudes.

---

## Tecnologías Utilizadas

* Python 3
* JSON
* BPMN 2.0
* GitHub
* Visual Studio Code

---

## Estructura del Proyecto

```text
Tpi-chatbot-vacaciones-IM
│
├── chatbot.py
├── empleados.json
├── solicitudes.json
├── requirements.txt
├── README.md
│
└── docs
    └── TPI_OrganizacionEmpresarial_IgnacioMerlo.pdf
```

---

## Ejecución

Abrir una terminal dentro del proyecto y ejecutar:

```bash
python3 chatbot.py
```

---

## Casos de Prueba

### Legajo inexistente

```text
9999
```

### Saldo insuficiente

```text
1005
10
```

### Solicitud aprobada

```text
1002
5
si
```

---

## Relación con BPMN

La lógica del chatbot implementa las decisiones modeladas en BPMN mediante validaciones y estructuras condicionales.

Las principales compuertas implementadas son:

* ¿Existe el legajo?
* ¿El dato ingresado es válido?
* ¿Posee saldo suficiente?
* ¿La solicitud puede continuar?

---

## Documentación

La documentación completa del Trabajo Práctico Integrador se encuentra disponible en la carpeta:

```text
docs/
```

---

## Autor

Ignacio Merlo

Trabajo Práctico Integrador – Organización Empresarial

UTN – TUPaD
