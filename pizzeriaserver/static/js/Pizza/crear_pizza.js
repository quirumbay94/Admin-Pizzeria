$("#tamano-select").change(function() {
	var tamano = $(this).val()
	habilitarMasas(tamano)
	habilitarBordes(tamano)
	habilitarIngredientes(tamano)
	habilitarPorciones(tamano)

	//CAMBIANDO LOS SELECTS A VALORES INICIALES
	$("#masa-select").val("")
	$("#borde-select").val("")
	$(".ingrediente-select").val("")
	$(".porcion-select").val("")
})

function agregarIngrediente() {
	var select = document.getElementsByClassName("select-wrapper")[0]
	var select_nuevo = select.cloneNode(true)
	document.getElementById("ingrediente-main-container").appendChild(select_nuevo)
}

function removerIngrediente(elem) {
	var padre = elem.parentNode
	padre.remove()
}

function habilitarMasas(nombre) {
	var masas = $(".pizza-masas")
	for (i=0; i < masas.length; i++) {
		var obj = $(masas[i]) 
		if (nombre === obj.attr("tipo")) {
			obj.removeClass("pizza-componente-seleccion-bloqueado")
			obj.addClass("pizza-componente-seleccion-disponible")
		} else {
			obj.removeClass("pizza-componente-seleccion-disponible")
			obj.addClass("pizza-componente-seleccion-bloqueado")
		}
	}
}

function habilitarBordes(nombre) {
	var bordes = $(".pizza-bordes")
	for (i=0; i < bordes.length; i++) {
		var obj = $(bordes[i]) 
		if (nombre === obj.attr("tipo")) {
			obj.removeClass("pizza-componente-seleccion-bloqueado")
			obj.addClass("pizza-componente-seleccion-disponible")
		} else {
			obj.removeClass("pizza-componente-seleccion-disponible")
			obj.addClass("pizza-componente-seleccion-bloqueado")
		}
	}
}

function habilitarIngredientes(nombre) {
	var ingredientes = document.getElementsByClassName("pizza-ingredientes")

	console.log(ingredientes.length)

	for (i=0; i < ingredientes.length; i++) {
		var ingrediente = ingredientes[i]
		var tipo = ingrediente.getAttribute("tipo")

		console.log(ingrediente)
		console.log(tipo)

		if (nombre === tipo) {
			ingrediente.classList.remove("pizza-componente-seleccion-bloqueado")
			ingrediente.classList.add("pizza-componente-seleccion-disponible")
		} else {
			ingrediente.classList.remove("pizza-componente-seleccion-disponible")
			ingrediente.classList.add("pizza-componente-seleccion-bloqueado")
		}
	}
}

function habilitarPorciones(nombre) {
	var porciones = $(".pizza-porciones")
	for (i=0; i < porciones.length; i++) {
		var obj = $(porciones[i]) 
		if (nombre != "") {
			obj.removeClass("pizza-componente-seleccion-bloqueado")
			obj.addClass("pizza-componente-seleccion-disponible")
		} else {
			obj.removeClass("pizza-componente-seleccion-disponible")
			obj.addClass("pizza-componente-seleccion-bloqueado")
		}
	}
}



