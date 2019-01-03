function agregarBloque(tipo) {
	if (tipo=="PIZZA") {
		var select = document.getElementsByClassName("pizza-select-subcontainer")[0]
		var select_nuevo = select.cloneNode(true)
		document.getElementById("pizza-select-contianer").appendChild(select_nuevo)
	} else if (tipo=="ADICIONAL") {
		var select = document.getElementsByClassName("adicional-select-subcontainer")[0]
		var select_nuevo = select.cloneNode(true)
		document.getElementById("adicional-select-contianer").appendChild(select_nuevo)
	} else if (tipo=="BEBIDA") {
		var select = document.getElementsByClassName("bebida-select-subcontainer")[0]
		var select_nuevo = select.cloneNode(true)
		document.getElementById("bebida-select-contianer").appendChild(select_nuevo)
	}	
}

function removerOpcion(elem) {
	var padre = elem.parentNode
	padre.remove()
}


