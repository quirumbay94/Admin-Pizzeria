from rest.models import Pizza_Tamano_Ingrediente

def limpiarRegistros_Ingredientes(pizza_obj):
	ingredientes = Pizza_Tamano_Ingrediente.objects.filter(pizza=pizza_obj)
	for ingrediente in ingredientes:
		try:
			ingrediente.delete()
		except:
			return False
	return True