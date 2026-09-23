/**
 * Menús flotantes de la cuenta: sidebar en PC y barra superior en móvil.
 * Cada botón [data-boton-cuenta] alterna el menú indicado en su
 * aria-controls; clic fuera o tecla Escape los cierra.
 * Solo actúa si existen; no usa etiquetas Django.
 */

(() => {
  function botones() {
    return document.querySelectorAll('[data-boton-cuenta]');
  }

  function botonDe(menu) {
    return document.querySelector(`[aria-controls="${menu.id}"]`);
  }

  function cerrarTodos() {
    document.querySelectorAll('.menu-usuario').forEach((menu) => {
      menu.hidden = true;
      const boton = botonDe(menu);
      if (boton) boton.setAttribute('aria-expanded', 'false');
    });
  }

  botones().forEach((boton) => {
    boton.addEventListener('click', (evento) => {
      evento.stopPropagation();
      const menu = document.getElementById(boton.getAttribute('aria-controls'));
      if (!menu) return;
      const abrir = menu.hidden;
      cerrarTodos();
      menu.hidden = !abrir;
      boton.setAttribute('aria-expanded', String(abrir));
    });
  });

  document.addEventListener('click', (evento) => {
    if (!evento.target.closest('.usuario-sidebar, .barra-movil')) cerrarTodos();
  });

  document.addEventListener('keydown', (evento) => {
    if (evento.key !== 'Escape') return;
    const abiertos = document.querySelectorAll('.menu-usuario:not([hidden])');
    cerrarTodos();
    abiertos.forEach((menu) => {
      const boton = botonDe(menu);
      if (boton) boton.focus();
    });
  });
})();
