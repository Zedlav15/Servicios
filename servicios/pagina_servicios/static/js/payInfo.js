function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getLanguagePrefix() {
    const pathName = window.location.pathname;
    const languagePrefix = pathName.split('/')[1]; 
    console.log('Language Prefix:', languagePrefix); // Esto debería imprimir "es"
    return languagePrefix;
}

$(document).ready(function() {

    const languagePrefix = getLanguagePrefix();

    $.ajax({
        url: '/' + languagePrefix + "/payInfo/",  // Asegúrate de que la URL coincide con la definida en Django
        type: "GET",
        dataType: "json", // Indicar que esperamos un JSON como respuesta
        success: function(data) {
            // Manipular los datos recibidos
            $("#product-description").text(data.servicio);
            $("#quantity").text(data.numeroTotal);
            $("#unit-price").text(data.precioUnitario);
            $('#total').text(data.precioTotal);
        },
        error: function(xhr, status, error) {
            console.error('Error al obtener datos de pago:', error);
        }
    });
});