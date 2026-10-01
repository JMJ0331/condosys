/**
 * Navegación compacta (<=768px): el botón hamburguesa abre el sidebar
 * como cajón lateral. Se cierra al elegir un enlace, con clic fuera
 * o tecla Escape. No usa etiquetas Django.
 */

(() => {
  const boton = document.getElementById('boton-menu-movil');
  const lateral = document.getElementById('menu-lateral');
  if (!boton || !lateral) return;

  function alternar(mostrar) {
    const abrir = mostrar !== undefined ? mostrar : !lateral.classList.contains('abierto');
    lateral.classList.toggle('abierto', abrir);
    boton.setAttribute('aria-expanded', String(abrir));
    document.body.classList.toggle('sin-desplazar', abrir);
  }

  boton.addEventListener('click', (evento) => {
    evento.stopPropagation();
    alternar();
  });

  lateral.addEventListener('click', (evento) => {
    if (evento.target.closest('a')) alternar(false);
  });

  document.addEventListener('click', (evento) => {
    if (lateral.classList.contains('abierto') && !evento.target.closest('#menu-lateral, #boton-menu-movil')) {
      alternar(false);
    }
  });

  document.addEventListener('keydown', (evento) => {
    if (evento.key === 'Escape' && lateral.classList.contains('abierto')) {
      alternar(false);
      boton.focus();
    }
  });

  window.matchMedia('(max-width: 768px)').addEventListener('change', (evento) => {
    if (!evento.matches) alternar(false);
  });
})();
