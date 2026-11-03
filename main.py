solicitudes = []
estudiantes = []
responsables = [
    {"id": 1, "nombre": "Bedelia"},
    {"id": 2, "nombre": "Secretaria Academica"},
    {"id": 3, "nombre": "Tutoria"},
]
contador = 0


def registrar(n, l, e, t, p, d):
    global contador
    if n == "" or l == "" or e == "" or d == "":
        print("error")
        return
    if "@" not in e:
        print("error")
        return
    if t != "certificado" and t != "equivalencia" and t != "baja" and t != "otro":
        print("tipo invalido")
        return
    if p != "alta" and p != "media" and p != "baja":
        print("prioridad invalida")
        return
    est = None
    for x in estudiantes:
        if x["legajo"] == l:
            est = x
    if est == None:
        est = {"nombre": n, "legajo": l, "email": e}
        estudiantes.append(est)
    contador = contador + 1
    s = {"id": contador, "est": est, "tipo": t, "prio": p, "desc": d,
         "estado": "pendiente", "resp": None}
    if t == "certificado":
        s["plazo"] = 3
    elif t == "equivalencia":
        s["plazo"] = 15
    elif t == "baja":
        s["plazo"] = 5
    else:
        s["plazo"] = 10
    if p == "alta":
        s["plazo"] = s["plazo"] - 1
    solicitudes.append(s)
    print("Solicitud " + str(contador) + " registrada")


def cambiar_estado(i, nuevo):
    for s in solicitudes:
        if s["id"] == i:
            if s["estado"] == "resuelta" or s["estado"] == "rechazada":
                print("no se puede cambiar")
                return
            if nuevo == "pendiente" or nuevo == "en proceso" or nuevo == "resuelta" or nuevo == "rechazada":
                s["estado"] = nuevo
                print("Estado actualizado")
                return
            else:
                print("estado invalido")
                return
    print("no existe")


def asignar(i, r):
    for s in solicitudes:
        if s["id"] == i:
            for x in responsables:
                if x["id"] == r:
                    s["resp"] = x["nombre"]
                    print("Responsable asignado")
                    return
            print("responsable invalido")
            return
    print("no existe")


def buscar(campo, valor):
    res = []
    if campo == "estado":
        for s in solicitudes:
            if s["estado"] == valor:
                res.append(s)
    elif campo == "tipo":
        for s in solicitudes:
            if s["tipo"] == valor:
                res.append(s)
    elif campo == "prioridad":
        for s in solicitudes:
            if s["prio"] == valor:
                res.append(s)
    elif campo == "legajo":
        for s in solicitudes:
            if s["est"]["legajo"] == valor:
                res.append(s)
    else:
        print("campo invalido")
        return
    if len(res) == 0:
        print("sin resultados")
    for s in res:
        print(str(s["id"]) + " | " + s["est"]["nombre"] + " | " + s["tipo"] +
              " | " + s["prio"] + " | " + s["estado"] + " | " + str(s["resp"]))


def reporte():
    print("=== REPORTE DE SOLICITUDES ===")
    pend = 0
    proc = 0
    res = 0
    rech = 0
    for s in solicitudes:
        if s["estado"] == "pendiente":
            pend = pend + 1
        elif s["estado"] == "en proceso":
            proc = proc + 1
        elif s["estado"] == "resuelta":
            res = res + 1
        else:
            rech = rech + 1
        print(str(s["id"]) + " | " + s["est"]["nombre"] + " | " + s["tipo"] +
              " | " + s["prio"] + " | " + s["estado"] + " | plazo: " + str(s["plazo"]) + " dias")
    print("Total: " + str(len(solicitudes)))
    print("Pendientes: " + str(pend) + " En proceso: " + str(proc) +
          " Resueltas: " + str(res) + " Rechazadas: " + str(rech))
    print("Su reporte ha sido generado")


while True:
    print("\n1.Registrar 2.Cambiar estado 3.Asignar 4.Buscar 5.Reporte 0.Salir")
    op = input("Opcion: ")
    if op == "1":
        n = input("Nombre: ")
        l = input("Legajo: ")
        e = input("Email: ")
        t = input("Tipo (certificado/equivalencia/baja/otro): ")
        p = input("Prioridad (alta/media/baja): ")
        d = input("Descripcion: ")
        registrar(n, l, e, t, p, d)
    elif op == "2":
        try:
            i = int(input("ID: "))
            nuevo = input("Nuevo estado (pendiente/en proceso/resuelta/rechazada): ")
            cambiar_estado(i, nuevo)
        except:
            print("error")
    elif op == "3":
        try:
            i = int(input("ID: "))
            r = int(input("ID responsable (1.Bedelia 2.Secretaria 3.Tutoria): "))
            asignar(i, r)
        except:
            print("error")
    elif op == "4":
        c = input("Campo (estado/tipo/prioridad/legajo): ")
        v = input("Valor: ")
        buscar(c, v)
    elif op == "5":
        reporte()
    elif op == "0":
        break
    else:
        print("opcion invalida")