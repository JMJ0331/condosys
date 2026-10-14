/**
 * Sidebar colapsable (solo escritorio): el botón junto al logo alterna
 * entre sidebar completo y solo iconos. La preferencia vive en la cookie
 * `sidebar_colapsado` para que el servidor pinte `body.colapsado` desde
 * el primer byte y no parpadee al cambiar de sección. En móvil (<=768px)
 * el botón está oculto y esta lógica no aplica. No usa etiquetas Django.
 */

(() => {
  const COOKIE = 'sidebar_colapsado';
  const CLAVE_LOCAL = 'sidebar-colapsado';
  const boton = document.getElementById('boton-colapsar');
  if (!boton) return;

  const esMovil = () => window.matchMedia('(max-width: 768px)').matches;

  function leerCookie() {
    const partes = document.cookie ? document.cookie.split('; ') : [];
    for (const parte of partes) {
      const indice = parte.indexOf('=');
      if (parte.slice(0, indice) === COOKIE) return parte.slice(indice + 1);
    }
    return null;
  }

  function guardar(colapsado) {
    const valor = colapsado ? '1' : '0';
    try {
      localStorage.setItem(CLAVE_LOCAL, valor);
    } catch (error) {
      /* almacenamiento no disponible: la cookie sigue guardando */
    }
    document.cookie = `${COOKIE}=${valor}; path=/; max-age=31536000; SameSite=Lax`;
  }

  function sincronizarBoton(colapsado) {
    boton.setAttribute('aria-expanded', String(!colapsado));
    boton.setAttribute(
      'aria-label',
      colapsado ? 'Ampliar menú' : 'Minimizar menú'
    );
  }

  function aplicar(colapsado) {
    document.body.classList.toggle('colapsado', colapsado);
    sincronizarBoton(colapsado);
    guardar(colapsado);
  }

  // El servidor ya pintó la clase desde la cookie: solo se sincroniza
  // el botón. Migración por única vez del valor viejo en localStorage.
  if (!document.body.classList.contains('colapsado') && leerCookie() === null) {
    let heredado = false;
    try {
      heredado = localStorage.getItem(CLAVE_LOCAL) === '1';
    } catch (error) {
      heredado = false;
    }
    if (heredado && !esMovil()) {
      document.body.classList.add('colapsado');
      guardar(true);
    }
  }
  sincronizarBoton(document.body.classList.contains('colapsado'));

  boton.addEventListener('click', (evento) => {
    evento.stopPropagation();
    if (esMovil()) return;
    aplicar(!document.body.classList.contains('colapsado'));
  });
})();
