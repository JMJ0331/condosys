"""Utilidades compartidas para los formularios del proyecto."""


def placeholder(field, label):
    """Coloca un placeholder (option con value="") como primera opción visible
    de un select y elimina la opción en blanco automática que Django agrega a
    los campos de opciones con choices, evitando que aparezca duplicada.

    Los campos de opciones que provienen de querysets (ModelChoiceField) no
    deben usar esta función: para ellos se usa `empty_label`.
    """
    choices = list(field.choices)
    choices = [c for c in choices if not (isinstance(c, (tuple, list)) and c[0] == '')]
    field.choices = [('', label)] + choices