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
    function calcularMonto() {
        var inputVal = $("#id_Input").val(); // Asegúrate de usar el ID correcto del input
        
        var number = inputVal ? parseFloat(inputVal) : 0; // Parsea a float sólo si hay valor

        if (number <= 0 || number == null) {
            $("#dolarContainerID").html('El total es: 0 USD'); // Establecer en 0 si el campo está vacío o es inválido
            return; // Termina la función si no hay número válido
        }

        const languagePrefix = getLanguagePrefix();

        $.ajax({
            url: '/' + languagePrefix + "/calcular-costo/",  // Asegúrate de usar la URL correcta definida en Django
            type: "POST",
            data: {
                'numero': number,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()  // Incluir el CSRF token
            },
            success: function(response) {
                if (response.total) {
                    $("#dolarContainerID").html('El total es: ' + parseFloat(response.total).toFixed(2) + ' USD');
                } else if (response.error) {
                    $("#dolarContainerID").html(response.error);  // Mostrar mensaje de error
                }
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
                $("#dolarContainerID").html("Error al formular el resultado");
            }
        });
    }

    $("#id_Input").on('input', calcularMonto);  // Asegúrate de usar el selector correcto
});
