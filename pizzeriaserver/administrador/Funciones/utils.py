from rest.models import Pizza_Tamano_Ingrediente, Coordenada

def limpiarRegistros_Ingredientes(pizza_obj):
	ingredientes = Pizza_Tamano_Ingrediente.objects.filter(pizza=pizza_obj)
	for ingrediente in ingredientes:
		try:
			ingrediente.delete()
		except:
			return False
	return True

def crearPosiciones(posiciones):
	exito = True

	##BORRANDO TODAS LAS INSTANCIAS ANTERIORES
	Coordenada.objects.all().delete()

	##CREANDO NUEVAS INSTANCIAS
	for posicion in posiciones:
		p = posicion.split("|")
		lat = p[0]
		lng = p[1]
		coordenada = Coordenada().crear(lat,lng)
		if not coordenada: 
			exito = False
			break
	return exito

def cedulaRepetida(cedula):
	cedulas = Detalles_Personales.objects.filter(cedula=cedula)
	if len(cedulas) > 1:
		return True
	return False