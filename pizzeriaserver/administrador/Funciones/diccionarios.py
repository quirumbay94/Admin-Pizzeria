from rest.models import *
##			GENERAL 		##
##DICCIONARIO CON DATOS PERSONALES PARA BARRA DE NAV
def diccionarioBarraNav(request, paquete):
	##NOMBRE DEL USUARIO
	paquete_ = paquete
	paquete_['NOMBRE'] = request.session["DETALLES_PERSONALES"]['NOMBRE']
	return paquete_

##DICCIONARIO CON MENSAJE PERSONALIZADO
def diccionarioMensaje(paquete, mensaje):
	paquete_ = paquete
	paquete_['MENSAJE'] = mensaje
	return paquete_

##			USUARIOS 		##
##DICCIONARIO CON TODOS LOS USUARIOS DEL SISTEMA
def diccionarioUsuarios(paquete):
	paquete_ = paquete
	paquete_['USUARIOS'] = Detalles_Personales.objects.all()
	return paquete_

##DICCIONARIO CON INFORMACION PARA LA SUBBARRA DE NAV DE UN USUARIO ESPECIFICO
def diccionarioDatosSubBarraUsuario(paquete, usuario_id):
	usuario = Detalles_Personales.objects.get(pk=usuario_id)
	paquete_ = paquete
	paquete_['USUARIO'] = usuario
	paquete_['URL'] = 'usuario'
	paquete_['TITULO'] = 'USUARIOS'
	return paquete_

##			COMPONENTES 		##
##DICCIONARIO CON INFORMACION PARA LA SUBBARRA DE NAV DE UN COMPONENTE
def diccionarioDatosSubBarraComponente(paquete, tipo):
	paquete_ = paquete
	paquete_['URL'] = 'componentes/' + tipo.upper()
	paquete_['TITULO'] = tipo.upper()
	paquete_["TIPO"] = tipo.upper()
	return paquete_

##DICCIONARIO CON INFORMACION DE COMPONENTE
def diccionarioDatosComponente(paquete, componente_id):
	paquete_ = paquete
	##BUSCANDO COMPONENTE
	componente = Componente.objects.get(pk=componente_id)
	t_i = Tamano_Ingrediente.objects.filter(ingrediente=componente)
	paquete_['COMPONENTE'] = componente
	paquete_['COSTOS'] = t_i
	return paquete_

##			PIZZAS TRADICIONALES		##
##DICCIONARIO CON INFORMACION DE TODAS LAS PIZZAS TRADICIONALES
def diccionarioPizzasTradicionales(paquete):
	## BUSCANDO PIZZAS TRADICIONALES
	paquete_ = paquete
	paquete_["PIZZAS_T"] = Pizza_Tradicional.objects.all()
	return paquete_

##DICCIONARIO CON INFORMACION PARA LA SUBBARRA DE NAV DE UNA PIZZA TRADICIONAL
def diccionarioDatosSubBarraPizza_T(paquete):
	paquete_ = paquete
	paquete_['URL'] = "pizzas_tradicionales"
	paquete_['TITULO'] = "PIZZAS TRADICIONALES"
	return paquete_

##DICCIONARIO CON INFORMACION DE PIZZA TRADICIONAL
def diccionarioDatoPizza_T(paquete, pizza_t_id):
	paquete_ = paquete

	##OBTENIENDO DATOS DE PIZZA
	pizza_trad = Pizza_Tradicional.objects.get(pk=pizza_t_id)
	ingrediente_porcion = Pizza_Tamano_Ingrediente.objects.filter(pizza=pizza_trad.pizza)
	paquete_["PIZZA_T"] = pizza_trad
	paquete_["INGREDIENTE_PORCION"] = ingrediente_porcion
	return paquete_

##DICCIONARIO CON INFORMACION DE TIPOS DE MASAS Y BORDES
def diccionarioMasasBordesIngredientes(paquete):
	paquete_ = paquete
	paquete_["TAMANOS"] = Tamano.objects.all()
	paquete_["MASAS"] = Tamano_Masa.objects.all()
	paquete_["BORDES"] = Tamano_Borde.objects.all()
	paquete_["INGREDIENTES"] = Tamano_Ingrediente.objects.all()
	paquete_["PORCIONES"] = Porcion.objects.all()
	return paquete_

##DICCIONARIO CON TODOS LOS TAMANOS EN DB
def diccionarioTamanos(paquete):
	paquete_ = paquete
	paquete_["TAMANOS"] = Tamano.objects.all()
	return paquete_

##DICCIONARIO CON COMBOS PROMOCIONALES
def diccionarioCombosPromocionales(paquete):
	paquete_ = paquete
	paquete_["COMBOS"] = Combos_Promocionales.objects.all()
	return paquete_
def diccionarioOpcionesParaComboPromocional(paquete):
	paquete_ = paquete
	##COLECTANDO BEBIDAS
	bebidas = Componente.objects.filter(tipo="BEBIDA")
	paquete_["BEBIDAS"] = Tamano_Ingrediente.objects.filter(ingrediente__in=bebidas)

	##COLECTANDO ADICIONALES
	adicionales = Componente.objects.filter(tipo="ADICIONAL")
	paquete_["ADICIONALES"] = Tamano_Ingrediente.objects.filter(ingrediente__in=adicionales)

	##COLECTANDO PIZZAS
	paquete_["PIZZAS"] = Pizza.objects.filter(de_admin=True)

	return paquete_	










