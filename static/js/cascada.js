/**
 * Selects en cascada de la jerarquía Jardín → Bloque → Edificio → Departamento
 * (ver structure/widgets.py). Dentro de cada <form>:
 *   - Los selects (o casillas) llevan data-cascada="jardin|bloque|edificio|departamento".
 *   - Sus opciones llevan data-jardin / data-bloque / data-edificio con los
 *     ids de sus ancestros (y data-propietario en los departamentos).
 * Al elegir un nivel se ocultan las opciones de los niveles inferiores que
 * no le pertenecen; al elegir un nivel inferior se rellenan sus ancestros.
 * Un elemento opcional [data-cascada-propietario] muestra el propietario
 * del departamento elegido. No usa etiquetas Django.
 */

(() => {
  const NIVELES = ['jardin', 'bloque', 'edificio', 'departamento'];

  function iniciarGrupo(grupo) {
    const selects = {};
    NIVELES.forEach((nivel) => {
      const select = grupo.querySelector(`select[data-cascada="${nivel}"]`);
      if (select) selects[nivel] = select;
    });
    const casillas = Array.from(grupo.querySelectorAll('input[type="checkbox"][data-cascada]'));
    const infoPropietario = grupo.querySelector('[data-cascada-propietario]');
    if (Object.keys(selects).length === 0) return;

    // Valor elegido en cada nivel superior al indicado.
    function ancestrosElegidos(nivel) {
      const elegidos = {};
      NIVELES.slice(0, NIVELES.indexOf(nivel)).forEach((superior) => {
        if (selects[superior] && selects[superior].value) {
          elegidos[superior] = selects[superior].value;
        }
      });
      return elegidos;
    }

    function coincide(elemento, elegidos) {
      return Object.entries(elegidos).every(([nivel, valor]) => elemento.dataset[nivel] === valor);
    }

    function filtrar() {
      NIVELES.forEach((nivel) => {
        const select = selects[nivel];
        if (!select) return;
        const elegidos = ancestrosElegidos(nivel);
        select.querySelectorAll('option').forEach((opcion) => {
          if (opcion.value === '') return;
          opcion.hidden = !coincide(opcion, elegidos);
        });
        const elegida = select.selectedOptions[0];
        if (elegida && elegida.hidden) select.value = '';
      });

      casillas.forEach((casilla) => {
        const fila = casilla.closest('label') ? casilla.closest('label').parentElement : casilla.parentElement;
        // Las casillas marcadas siempre se ven para poder desmarcarlas.
        fila.hidden = !casilla.checked && !coincide(casilla, ancestrosElegidos(casilla.dataset.cascada));
      });

      mostrarPropietario();
    }

    // Al elegir un nivel inferior se completan sus ancestros desde la opción.
    function rellenarAncestros(nivel) {
      const opcion = selects[nivel].selectedOptions[0];
      if (!opcion || opcion.value === '') return;
      NIVELES.slice(0, NIVELES.indexOf(nivel)).forEach((superior) => {
        const valor = opcion.dataset[superior];
        if (selects[superior] && valor) selects[superior].value = valor;
      });
    }

    function mostrarPropietario() {
      if (!infoPropietario || !selects.departamento) return;
      const opcion = selects.departamento.selectedOptions[0];
      infoPropietario.textContent = opcion && opcion.value ? (opcion.dataset.propietario || 'Sin propietario') : '—';
    }

    Object.entries(selects).forEach(([nivel, select]) => {
      select.addEventListener('change', () => {
        rellenarAncestros(nivel);
        filtrar();
      });
    });
    casillas.forEach((casilla) => casilla.addEventListener('change', filtrar));

    filtrar();
  }

  document.querySelectorAll('form').forEach(iniciarGrupo);
})();
