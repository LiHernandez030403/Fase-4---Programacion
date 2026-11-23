
"""
SISTEMA INTEGRAL DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS
Empresa: Software FJ
Curso: Programacion - UNAD
Lizeth Hernandez
"""

from abc import ABC, abstractmethod
import logging


# ==========================================================
# CONFIGURACION DEL ARCHIVO DE REGISTRO
# ==========================================================

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ==========================================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================================

class ErrorSistema(Exception):
    pass


class DatoInvalidoError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class ReservaError(ErrorSistema):
    pass


# ==========================================================
# CLASE ABSTRACTA ENTIDAD
# ==========================================================

class Entidad(ABC):

    def __init__(self, identificacion):
        self._identificacion = identificacion

    def obtener_identificacion(self):
        return self._identificacion

    @abstractmethod
    def validar(self):
        pass


# ==========================================================
# CLASE CLIENTE
# ==========================================================

class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        self._nombre = nombre
        self._correo = correo
        self._telefono = telefono

        self.validar()

    def validar(self):

        if not self._identificacion or not self._identificacion.strip():
            raise DatoInvalidoError("La identificacion es obligatoria.")

        if not self._nombre or not self._nombre.strip():
            raise DatoInvalidoError("El nombre es obligatorio.")

        if "@" not in self._correo or "." not in self._correo:
            raise DatoInvalidoError("El correo no es valido.")

        if not self._telefono.isdigit() or len(self._telefono) < 7:
            raise DatoInvalidoError("El telefono debe tener minimo 7 digitos.")

    def obtener_nombre(self):
        return self._nombre

    def mostrar_datos(self):
        return (
            f"Identificacion: {self._identificacion} | "
            f"Nombre: {self._nombre} | "
            f"Correo: {self._correo} | "
            f"Telefono: {self._telefono}"
        )


# ==========================================================
# CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(ABC):

    def __init__(self, codigo, nombre, tarifa):

        self._codigo = codigo
        self._nombre = nombre
        self._tarifa = tarifa
        self._disponible = True

        self.validar_parametros()

    def validar_parametros(self):

        if not self._codigo or not self._codigo.strip():
            raise DatoInvalidoError("El codigo del servicio es obligatorio.")

        if not self._nombre or not self._nombre.strip():
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")

        if not isinstance(self._tarifa, (int, float)) or self._tarifa <= 0:
            raise DatoInvalidoError("La tarifa debe ser mayor que cero.")

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_duracion(self, duracion):
        pass

    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        self.validar_duracion(duracion)

        if not 0 <= impuesto <= 100:
            raise DatoInvalidoError("El impuesto debe estar entre 0 y 100.")

        if not 0 <= descuento <= 100:
            raise DatoInvalidoError("El descuento debe estar entre 0 y 100.")

        subtotal = self._tarifa * duracion

        valor_impuesto = subtotal * impuesto / 100

        total = subtotal + valor_impuesto

        valor_descuento = total * descuento / 100

        total = total - valor_descuento

        return round(total, 2)

    def obtener_codigo(self):
        return self._codigo

    def cambiar_disponibilidad(self, estado):
        self._disponible = estado

    def esta_disponible(self):
        return self._disponible


# ==========================================================
# SERVICIO 1: RESERVA DE SALAS
# ==========================================================

class ReservaSala(Servicio):

    def __init__(self, codigo, nombre, tarifa, capacidad):

        self._capacidad = capacidad

        super().__init__(codigo, nombre, tarifa)

    def validar_parametros(self):

        super().validar_parametros()

        if not isinstance(self._capacidad, int) or self._capacidad <= 0:
            raise DatoInvalidoError("La capacidad debe ser un entero positivo.")

    def describir_servicio(self):

        return (
            f"Reserva de sala: {self._nombre}. "
            f"Capacidad: {self._capacidad} personas."
        )

    def validar_duracion(self, duracion):

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duracion debe ser mayor que cero.")


# ==========================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# ==========================================================

class AlquilerEquipo(Servicio):

    def __init__(self, codigo, nombre, tarifa, tipo_equipo):

        self._tipo_equipo = tipo_equipo

        super().__init__(codigo, nombre, tarifa)

    def validar_parametros(self):

        super().validar_parametros()

        if not self._tipo_equipo or not self._tipo_equipo.strip():
            raise DatoInvalidoError("Debe indicar el tipo de equipo.")

    def describir_servicio(self):

        return (
            f"Alquiler de equipo: {self._tipo_equipo}. "
            f"Nombre: {self._nombre}."
        )

    def validar_duracion(self, duracion):

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duracion del alquiler no es valida.")


# ==========================================================
# SERVICIO 3: ASESORIAS ESPECIALIZADAS
# ==========================================================

class AsesoriaEspecializada(Servicio):

    def __init__(self, codigo, nombre, tarifa, especialidad):

        self._especialidad = especialidad

        super().__init__(codigo, nombre, tarifa)

    def validar_parametros(self):

        super().validar_parametros()

        if not self._especialidad or not self._especialidad.strip():
            raise DatoInvalidoError("Debe indicar la especialidad.")

    def describir_servicio(self):

        return (
            f"Asesoria especializada en {self._especialidad}: "
            f"{self._nombre}."
        )

    def validar_duracion(self, duracion):

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duracion de la asesoria no es valida.")


# ==========================================================
# CLASE RESERVA
# ==========================================================

class Reserva:

    def __init__(self, codigo, cliente, servicio, duracion):

        if not isinstance(cliente, Cliente):
            raise ReservaError("Debe seleccionar un cliente valido.")

        if not isinstance(servicio, Servicio):
            raise ReservaError("Debe seleccionar un servicio valido.")

        servicio.validar_duracion(duracion)

        if not servicio.esta_disponible():
            raise ServicioNoDisponibleError(
                "El servicio seleccionado no esta disponible."
            )

        self._codigo = codigo
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._valor = 0

    def confirmar(self):

        if self._estado != "Pendiente":
            raise ReservaError("La reserva no esta pendiente.")

        if not self._servicio.esta_disponible():
            raise ServicioNoDisponibleError("El servicio no esta disponible.")

        self._valor = self._servicio.calcular_costo(self._duracion)

        self._estado = "Confirmada"

        self._servicio.cambiar_disponibilidad(False)

        logging.info("Reserva %s confirmada.", self._codigo)

        return self._valor

    def cancelar(self):

        if self._estado == "Cancelada":
            raise ReservaError("La reserva ya esta cancelada.")

        if self._estado == "Procesada":
            raise ReservaError("No se puede cancelar una reserva procesada.")

        if self._estado == "Confirmada":
            self._servicio.cambiar_disponibilidad(True)

        self._estado = "Cancelada"

        logging.info("Reserva %s cancelada.", self._codigo)

    def procesar(self):

        if self._estado != "Confirmada":
            raise ReservaError("Primero debe confirmar la reserva.")

        self._estado = "Procesada"

        logging.info("Reserva %s procesada.", self._codigo)

    def mostrar_reserva(self):

        return (
            f"Reserva: {self._codigo} | "
            f"Cliente: {self._cliente.obtener_nombre()} | "
            f"Servicio: {self._servicio.describir_servicio()} | "
            f"Duracion: {self._duracion} | "
            f"Estado: {self._estado} | "
            f"Valor: ${self._valor:,.2f}"
        )


# ==========================================================
# CLASE PRINCIPAL DEL SISTEMA
# ==========================================================

class SistemaSoftwareFJ:

    def __init__(self):

        self._clientes = []
        self._servicios = []
        self._reservas = []

    # REGISTRAR CLIENTES

    def registrar_cliente(self, cliente):

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("El objeto no es un cliente.")

        for existente in self._clientes:

            if existente.obtener_identificacion() == cliente.obtener_identificacion():

                raise DatoInvalidoError("El cliente ya esta registrado.")

        self._clientes.append(cliente)

        logging.info("Cliente registrado: %s", cliente.obtener_identificacion())

    # REGISTRAR SERVICIOS

    def registrar_servicio(self, servicio):

        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("El objeto no es un servicio.")

        for existente in self._servicios:

            if existente.obtener_codigo() == servicio.obtener_codigo():

                raise DatoInvalidoError("El servicio ya existe.")

        self._servicios.append(servicio)

        logging.info("Servicio registrado: %s", servicio.obtener_codigo())

    # BUSCAR CLIENTES

    def buscar_cliente(self, identificacion):

        for cliente in self._clientes:

            if cliente.obtener_identificacion() == identificacion:

                return cliente

        raise DatoInvalidoError("No se encontro el cliente.")

    # BUSCAR SERVICIOS

    def buscar_servicio(self, codigo):

        for servicio in self._servicios:

            if servicio.obtener_codigo() == codigo:

                return servicio

        raise DatoInvalidoError("No se encontro el servicio.")

    # CREAR RESERVAS

    def crear_reserva(self, codigo, identificacion, codigo_servicio, duracion):

        cliente = self.buscar_cliente(identificacion)

        servicio = self.buscar_servicio(codigo_servicio)

        for reserva in self._reservas:

            if reserva._codigo == codigo:
                raise ReservaError("El codigo de reserva ya existe.")

        reserva = Reserva(codigo, cliente, servicio, duracion)

        self._reservas.append(reserva)

        logging.info("Reserva %s creada.", codigo)

        return reserva

    # MOSTRAR CLIENTES

    def mostrar_clientes(self):

        print("\n========== CLIENTES ==========")

        if not self._clientes:
            print("No hay clientes registrados.")

        for cliente in self._clientes:
            print(cliente.mostrar_datos())

    # MOSTRAR SERVICIOS

    def mostrar_servicios(self):

        print("\n========== SERVICIOS ==========")

        if not self._servicios:
            print("No hay servicios registrados.")

        for servicio in self._servicios:

            print(
                servicio.obtener_codigo(),
                servicio.describir_servicio(),
                "Tarifa: $",
                servicio._tarifa
            )

    # MOSTRAR RESERVAS

    def mostrar_reservas(self):

        print("\n========== RESERVAS ==========")

        if not self._reservas:
            print("No hay reservas registradas.")

        for reserva in self._reservas:
            print(reserva.mostrar_reserva())


# ==========================================================
# FUNCION PARA CONTROLAR ERRORES
# ==========================================================

def ejecutar_operacion(descripcion, funcion):

    print("\n" + descripcion)

    try:

        resultado = funcion()

    except ErrorSistema as error:

        print("Error controlado:", error)

        logging.error("%s: %s", descripcion, error)

    except Exception as error:

        print("Error inesperado:", error)

        logging.exception("%s: error inesperado", descripcion)

    else:

        if resultado is not None:
            print(resultado)

        print("Operacion realizada correctamente.")

    finally:

        print("Fin de la operacion.")


# ==========================================================
# CONVERSION Y ENCADENAMIENTO DE EXCEPCIONES
# ==========================================================

def convertir_duracion(valor):

    try:

        return float(valor)

    except (TypeError, ValueError) as error:

        raise DatoInvalidoError(
            "La duracion debe ser un valor numerico."
        ) from error


# ==========================================================
# EJECUCION DE LAS PRUEBAS
# ==========================================================

def ejecutar_pruebas():

    sistema = SistemaSoftwareFJ()

    print("\n")
    print("=" * 65)
    print(" SOFTWARE FJ - SISTEMA DE GESTION DE CLIENTES Y RESERVAS")
    print("=" * 65)

    # OPERACION 1: CLIENTE VALIDO

    cliente1 = None

    def operacion1():

        nonlocal cliente1

        cliente1 = Cliente(
            "1001",
            "Ana Perez",
            "ana@gmail.com",
            "3001234567"
        )

        sistema.registrar_cliente(cliente1)

        return "Cliente Ana Perez registrado correctamente."

    ejecutar_operacion("OPERACION 1: REGISTRO DE CLIENTE VALIDO", operacion1)

    # OPERACION 2: CLIENTE INVALIDO

    def operacion2():

        cliente = Cliente(
            "1002",
            "",
            "correo_invalido",
            "123"
        )

        sistema.registrar_cliente(cliente)

    ejecutar_operacion("OPERACION 2: REGISTRO DE CLIENTE INVALIDO", operacion2)

    # OPERACION 3: SEGUNDO CLIENTE

    cliente2 = None

    def operacion3():

        nonlocal cliente2

        cliente2 = Cliente(
            "1003",
            "Carlos Gomez",
            "carlos@gmail.com",
            "3107654321"
        )

        sistema.registrar_cliente(cliente2)

        return "Cliente Carlos Gomez registrado correctamente."

    ejecutar_operacion("OPERACION 3: REGISTRO DE SEGUNDO CLIENTE", operacion3)

    # OPERACION 4: RESERVA DE SALA

    sala = None

    def operacion4():

        nonlocal sala

        sala = ReservaSala(
            "S01",
            "Sala de reuniones",
            50000,
            12
        )

        sistema.registrar_servicio(sala)

        return sala.describir_servicio()

    ejecutar_operacion("OPERACION 4: CREACION DE SERVICIO DE SALA", operacion4)

    # OPERACION 5: ALQUILER DE EQUIPO

    equipo = None

    def operacion5():

        nonlocal equipo

        equipo = AlquilerEquipo(
            "E01",
            "Computador portatil",
            20000,
            "Portatil"
        )

        sistema.registrar_servicio(equipo)

        return equipo.describir_servicio()

    ejecutar_operacion("OPERACION 5: CREACION DE SERVICIO DE EQUIPO", operacion5)

    # OPERACION 6: ASESORIA

    asesoria = None

    def operacion6():

        nonlocal asesoria

        asesoria = AsesoriaEspecializada(
            "A01",
            "Asesoria de programacion",
            80000,
            "Programacion"
        )

        sistema.registrar_servicio(asesoria)

        return asesoria.describir_servicio()

    ejecutar_operacion("OPERACION 6: CREACION DE ASESORIA", operacion6)

    # OPERACION 7: SERVICIO INVALIDO

    def operacion7():

        servicio = ReservaSala(
            "S02",
            "Sala invalida",
            -1000,
            0
        )

        sistema.registrar_servicio(servicio)

    ejecutar_operacion("OPERACION 7: CREACION DE SERVICIO INVALIDO", operacion7)

    # OPERACION 8: RESERVA EXITOSA

    reserva1 = None

    def operacion8():

        nonlocal reserva1

        reserva1 = sistema.crear_reserva(
            "R001",
            "1001",
            "S01",
            2
        )

        valor = reserva1.confirmar()

        return f"Reserva confirmada. Valor total: ${valor:,.2f}"

    ejecutar_operacion("OPERACION 8: RESERVA EXITOSA", operacion8)

    # OPERACION 9: SERVICIO NO DISPONIBLE

    def operacion9():

        reserva = sistema.crear_reserva(
            "R002",
            "1003",
            "S01",
            1
        )

        return reserva.confirmar()

    ejecutar_operacion("OPERACION 9: SERVICIO NO DISPONIBLE", operacion9)

    # OPERACION 10: DURACION INVALIDA

    def operacion10():

        duracion = convertir_duracion(-2)

        sistema.crear_reserva(
            "R003",
            "1003",
            "E01",
            duracion
        )

    ejecutar_operacion("OPERACION 10: RESERVA CON DURACION INVALIDA", operacion10)

    # OPERACION 11: PROCESAR RESERVA

    def operacion11():

        reserva1.procesar()

        return "La reserva R001 fue procesada correctamente."

    ejecutar_operacion("OPERACION 11: PROCESAMIENTO DE RESERVA", operacion11)

    # OPERACION 12: CANCELACION NO PERMITIDA

    def operacion12():

        reserva1.cancelar()

    ejecutar_operacion("OPERACION 12: CANCELACION NO PERMITIDA", operacion12)

    # OPERACION 13: CALCULO CON IMPUESTO Y DESCUENTO

    def operacion13():

        valor = asesoria.calcular_costo(2, 19, 10)

        return (
            f"Costo de asesoria por 2 horas, "
            f"con 19% de impuesto y 10% de descuento: ${valor:,.2f}"
        )

    ejecutar_operacion("OPERACION 13: CALCULO DE COSTOS", operacion13)

    # MOSTRAR INFORMACION DEL SISTEMA

    sistema.mostrar_clientes()

    sistema.mostrar_servicios()

    sistema.mostrar_reservas()

    print("\n")
    print("Los eventos y errores se guardaron en software_fj.log.")
    print("El sistema termino correctamente.")


# ==========================================================
# INICIO DEL PROGRAMA
# ==========================================================

if __name__ == "__main__":

    try:

        ejecutar_pruebas()

    except Exception as error:

        logging.exception("Error general: %s", error)

        print("Se presento un error general. Revise el archivo de registro.")

    finally:

        print("\nEJECUCION FINALIZADA.")
