    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // ¿Este cookie es el cookie CSRFToken que estamos buscando?
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

    function loadLoggedInState() {
        var xhr = new XMLHttpRequest();
        var csrftoken = getCookie('csrftoken');
        var languagePrefix = getLanguagePrefix();

        var url = '/' + languagePrefix + '/check-logged-in/';
        console.log('Request URL:', url); // Esto te permitirá ver la URL completa en la consola

        xhr.open('GET', url, true);
        xhr.setRequestHeader('X-CSRFToken', csrftoken);

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                updateMenu(response.loggedIn);
            } else {
                console.error('Request failed with status:', xhr.status);
            }
        };

        xhr.onerror = function() {
            console.error('Request failed');
        };

        xhr.send();
    }


    function updateMenu(isLoggedIn) {
        if (isLoggedIn) {
            document.getElementById("perfilLink").classList.remove('hidden');
            document.getElementById("saldoLink").classList.remove('hidden');
            document.getElementById("iniciarLink").classList.add('hidden');
            document.getElementById("registrarLink").classList.add('hidden');
        } else {
            document.getElementById("perfilLink").classList.add('hidden');
            document.getElementById("saldoLink").classList.add('hidden');
            document.getElementById("iniciarLink").classList.remove('hidden');
            document.getElementById("registrarLink").classList.remove('hidden');
        }
    }

    window.onload = loadLoggedInState;
