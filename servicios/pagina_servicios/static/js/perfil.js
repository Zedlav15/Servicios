 // Función para mostrar u ocultar los divs según el fragmento de URL
 function mostrarDivSegunFragmento() {
    var fragmento = window.location.hash; // Obtenemos el fragmento de la URL

    // Mostramos el div correspondiente al fragmento
    switch (fragmento) {
        case '#walletContainer':
            document.getElementById('infoProfileContainer').style.display = 'none';
            document.getElementById('walletContainer').style.display = 'block';
            break;
        case '#pedidosContainer':
            document.getElementById('infoProfileContainer').style.display = 'none';
            document.getElementById('pedidosContainer').style.display = 'block';
            break;
        default:
            document.getElementById('infoProfileContainer').style.display = 'block'; // Mostramos por defecto el primer div
    }
}

// Llamamos a la función cuando la página se carga
window.onload = function() {
    mostrarDivSegunFragmento();
};