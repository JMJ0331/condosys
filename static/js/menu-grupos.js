/**
 * Grupos desplegables del menú lateral (p. ej. "Estructura": jardines,
 * bloques y edificios). El servidor pinta `.abierto` cuando la página
 * actual es uno de los hijos; aquí solo se alterna al hacer clic.
 * No usa etiquetas Django.
 */

(() => {
  document.querySelectorAll('[data-grupo-menu]').forEach((grupo) => {
    const boton = grupo.querySelector('[data-boton-grupo]');
    if (!boton) return;

    boton.addEventListener('click', () => {
      const abierto = grupo.classList.toggle('abierto');
      boton.setAttribute('aria-expanded', String(abierto));
    });
  });
})();
