const openBtn = document.getElementById("checkout-btn");
const closeBtn = document.getElementById("closeModal");
const modal = document.getElementById("modal");
const modalCan = document.getElementById("modalCan");
const closeBtnCan = document.getElementById("closeModalCan");

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

openBtn.addEventListener("click", () => {
    const languagePrefix = getLanguagePrefix();
    
    $.ajax({
        url: '/' + languagePrefix + "/validateOperation/",  // Asegúrate de que la URL coincide con la definida en Django
        type: "GET",
        dataType: "json", // Indicar que esperamos un JSON como respuesta
        success: function(data) {
            // Manipular los datos recibidos
            var creditos = parseFloat(data.creditos)
            var precioTotal = parseFloat(data.precioTotal)

            if (creditos < precioTotal){
                console.log(creditos);
                console.log(precioTotal);
                modalCan.classList.add("open");
            }else{
                console.log(creditos);
                console.log(precioTotal);
                modal.classList.add("open");
            }
        },
        error: function(xhr, status, error) {
            console.error('Error al obtener datos de pago:', error);
        }
    });
});

closeBtn.addEventListener("click", () => {
    const languagePrefix = getLanguagePrefix();
    modal.classList.remove("open");

    $.ajax({
        url: '/' + languagePrefix + "/agregar-transaccion/",  // Actualizado para apuntar a la vista Django
        type: "POST",
        dataType: "json", // Asegúrate de que tu vista Django devuelva una respuesta JSON
        // Incluir el token CSRF en la solicitud
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        success: function (response) {
            if (response.redirect_url) {
                // Redirige a la URL especificada en la respuesta
                window.location.href = response.redirect_url;
            } else {
                // Manejar casos donde no hay URL de redirección, si es necesario
                alert("La operación se completó, pero no se proporcionó URL de redirección.");
            }  // Actualizado para usar rutas relativas
        },
        error: function(xhr, status, error) {
            // Manejar posibles errores aquí
            console.error("Error al realizar la compra:", error);
        }
    });
})

closeBtnCan.addEventListener("click", () => {
    modalCan.classList.remove("open");
})