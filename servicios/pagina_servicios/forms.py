from django import forms

class LoginForm(forms.Form):
    correo_electronico = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=250)
    correo_electronico = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ComentariosForm(forms.Form):
    comentariosInput = forms.IntegerField(min_value=1, label="Num. de comentarios")
    linkInput = forms.URLField(label="Ingrese el link")

class ReaccionesForm(forms.Form):
    ReaccionesInput = forms.IntegerField(min_value=1, label="Num. de reacciones")
    linkInput = forms.URLField(label="Ingrese el link")

class CompartidasForm(forms.Form):
    compartidasInput = forms.IntegerField(min_value=1, label="Num. de compartidas")
    linkInput = forms.URLField(label="Ingrese el link")

class ReproduccionesForm(forms.Form):
    reproInput = forms.IntegerField(min_value=1, label="Num. de reproducciones")
    linkInput = forms.URLField(label="Ingrese el link")

class SeguidoresForm(forms.Form):
    segInput = forms.IntegerField(min_value=1, label="Num. de seguidores")
    linkInput = forms.URLField(label="Ingrese el link")

class LikesForm(forms.Form):
    likesInput = forms.IntegerField(min_value=1, label="Num. de likes")
    linkInput = forms.URLField(label="Ingrese el link")

class VotosForm(forms.Form):
    FORMATO_VOTO_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        # Puedes añadir más opciones si es necesario
    ]

    formatV = forms.ChoiceField(choices=FORMATO_VOTO_CHOICES, label="Seleccione la opción de voto deseado:")
    votosInput = forms.IntegerField(min_value=1, label="Ingrese el número de votos:")
    linkInput = forms.URLField(label="Ingrese el link:")

class RtForm(forms.Form):
    rtInput = forms.IntegerField(min_value=1, label="Num. de retwitt")
    linkInput = forms.URLField(label="Ingrese el link")

class enVivoForm(forms.Form):
    FORMATO_TIEMPO_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        # Puedes añadir más opciones si es necesario
    ]

    formatV = forms.ChoiceField(choices=FORMATO_TIEMPO_CHOICES, label="Seleccione la opción de voto deseado:")
    especInput = forms.IntegerField(min_value=1, label="Num. de espectadores")
    linkInput = forms.URLField(label="Ingrese el link")