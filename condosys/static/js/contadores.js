/**
 * Contador de caracteres para textareas (global).
 * A cada <textarea maxlength> le inserta debajo un "0 / 400 caracteres"
 * que se actualiza con cada tecla y al cargar (útil al editar con texto).
 * Sin etiquetas de plantilla Django: lee el límite del propio maxlength.
 */
(() => {
  document.querySelectorAll('textarea[maxlength]').forEach((campo) => {
    const limite = Number.parseInt(campo.getAttribute('maxlength'), 10);
    if (Number.isNaN(limite)) return;

    const contador = document.createElement('p');
    contador.className = 'contador-caracteres';
    contador.setAttribute('role', 'status');
    const numero = document.createElement('span');
    const maximo = document.createElement('span');
    contador.append(numero, ' / ', maximo, ' caracteres');
    campo.after(contador);

    function actualizar() {
      numero.textContent = String(campo.value.length);
      maximo.textContent = String(limite);
      contador.classList.toggle('limite-alcanzado', campo.value.length >= limite);
    }

    campo.addEventListener('input', actualizar);
    actualizar();
  });
})();
