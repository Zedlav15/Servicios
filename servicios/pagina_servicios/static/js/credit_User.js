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

$(document).ready(function () {
    const languagePrefix = getLanguagePrefix();

    $.ajax({
        url: '/' + languagePrefix + '/creditos-usuario/',
        method: "GET",
        dataType: "json",  // Indicar que esperamos un JSON como respuesta
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); // Añadir el token CSRF
        },
        success: function(response){
            console.log(response)
            var creditNumber = parseFloat(response.creditos).toFixed(2)
            $('#pSaldo').html(creditNumber + ' USD')
        },
        error: function(response){
            // Manejar el error
            console.error("Error al obtener los créditos del usuario");
        }
    });
});