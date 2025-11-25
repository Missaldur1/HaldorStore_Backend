# 🚀 Guía de Inicio Rápido del Backend

Esta guía te ayudará a configurar y ejecutar el proyecto del backend en tu máquina local. Seguir estos pasos asegura que tengas el entorno de trabajo adecuado para desarrollar sin problemas.

---

### 📦 Paso 1: Configuración del Entorno Virtual (Recomendado)

Trabajar dentro de un **entorno virtual** es fundamental para aislar las dependencias de este proyecto de las librerías instaladas globalmente en tu sistema.

1.  **Crear el Entorno Virtual:**
    Abre tu terminal o línea de comandos en la carpeta raíz del proyecto y ejecuta:

    ```bash
    py -m venv venv
    ```

    > **Nota:** El segundo `venv` es el nombre de la carpeta que se creará para tu entorno.

2.  **Activar el Entorno Virtual:**
    Debes "entrar" a este entorno antes de instalar dependencias.

    * **Para Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    * **Para Windows (CMD):**
        ```bash
        .\venv\Scripts\activate
        ```
    * **Verificación:** Si la activación fue exitosa, verás el nombre de tu entorno (`(venv)`) al inicio de la línea de comandos.

3.  **Seleccionar Intérprete (VS Code - Opcional):**
    Si usas Visual Studio Code, presiona `F1`, busca **"Python: Select Interpreter"** y selecciona el que está dentro de la carpeta `venv`.

---

### 🛠️ Paso 2: Instalación de Dependencias

Con el entorno virtual **activo**, instala todas las librerías necesarias listadas en el archivo `requirements.txt`.

* **Comando de Instalación:**

    ```bash
    pip install -r .\requirements.txt
    ```

---

### 🟢 Paso 3: Ejecución del Proyecto

Una vez instaladas las dependencias, puedes iniciar el servidor de desarrollo local.

1.  **Comando para Iniciar el Servidor:**

    ```bash
    py .\manage.py runserver
    ```

2.  **Acceder al Proyecto:**
    La terminal te proporcionará una dirección web local (ej: `http://127.0.0.1:8000/`). Mantén presionada la tecla **`Ctrl`** (o `Cmd` en Mac) y haz **clic** en la URL para abrir el proyecto en tu navegador.

---

### 🔑 Paso 4: Acceso a la Interfaz de Administración

Para acceder a la consola de administración del backend (si está configurada):

1.  **Dirígete a la URL del proyecto** que se abrió en el paso anterior.
2.  **Añade `/admin`** al final de la dirección en la barra del navegador.
    * **Ejemplo:** `http://127.0.0.1:8000/admin`
3.  Ingresa tus credenciales de administrador (usuario y contraseña).

---

### 🛑 Para Detener el Servidor

Cuando termines de trabajar, vuelve a la terminal donde se está ejecutando el servidor y presiona **`Ctrl + C`**.

**Para Desactivar el Entorno Virtual:**
Simplemente escribe `deactivate` en la terminal.

```bash
deactivate