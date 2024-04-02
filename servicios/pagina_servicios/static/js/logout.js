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
    console.log('Language Prefix:', languagePrefix);
    return languagePrefix;
}
function cerrarSesion(){
    $.ajax({
        url: "../php/logout.php",
        method:"POST",
        success: function(data){
            window.location.href = "../index.html";
        },
        error: function(xhr, status, error){
            console.error("Error al cerrar sesion:", error);
        }
    });
}

$(document).ready(function(){
    $("#logout").on("click", cerrarSesion);
});