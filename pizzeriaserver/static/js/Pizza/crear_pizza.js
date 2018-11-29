$("#tamano-select").change(function() {
	var nombre = $(this).val()
	habilitarMasas(nombre)
	habilitarBordes(nombre)

	//CAMBIANDO LOS SELECTS A VALORES INICIALES
	$("#masa-select").val("")
	$("#borde-select").val("")
})

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