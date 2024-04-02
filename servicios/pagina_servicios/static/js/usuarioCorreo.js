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
    const languagePrefix = getLanguagePrefix(); // Asegúrate de obtener el prefijo de idioma correctamente

    $.ajax({
        url: '/' + languagePrefix + '/user-data/',  // Actualiza con la URL de tu vista en Django
        type: "GET",
        dataType: "json",  // Indicar que esperamos un JSON como respuesta
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); // Añadir el token CSRF
        },
        success: function(data) {
            // Manipular los datos recibidos
            $("#pUser").text(data.nombre);
            $("#pAddress").text(data.correo); // Mostrar el correo electrónico
        },
        error: function(xhr, status, error) {
            console.error("Ha ocurrido un error: ", error);
        }
    });
});
