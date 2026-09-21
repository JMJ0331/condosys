/**
 * Lógica específica del módulo Residencial.
 * - Filtra el select de municipio/ciudad según la provincia elegida
 *   (las opciones llevan data-provincia desde la plantilla).
 * - Cambia las etiquetas de cantidad según la distribución elegida
 *   (Torres: "Cantidad de torres" / "Cantidad de pisos por torre";
 *   Edificios: "Cantidad de edificios" / "Cantidad de pisos por edificio").
 * - Muestra la vista previa del iframe de Google Maps al pegar el
 *   código en el textarea (data-residencial="mapa").
 * - El botón Cancelar limpia el formulario y la vista previa.
 * - Con data-solo-lectura="1" el formulario se deshabilita
 *   (usuarios sin rol admin/manager).
 */
(() => {
  const formulario = document.getElementById('formulario-residencial');
  if (!formulario) return;

  const selectProvincia = formulario.querySelector('[data-residencial="provincia"]');
  const selectMunicipio = formulario.querySelector('[data-residencial="municipio"]');
  const selectDistribucion = formulario.querySelector('[data-residencial="distribucion"]');
  const etiquetaEdificios = document.getElementById('etiqueta-cantidad-edificios');
  const etiquetaPisos = document.getElementById('etiqueta-cantidad-pisos');
  const campoMapa = formulario.querySelector('[data-residencial="mapa"]');
  const zonaMapa = document.getElementById('zona-mapa');
  const vistaPrevia = document.getElementById('vista-previa-mapa');
  const contenidoZona = document.getElementById('contenido-zona-mapa');
  const botonCancelar = document.getElementById('boton-cancelar-residencial');

  // Recuerda el municipio guardado aunque no esté en el catálogo
  // (el servidor lo acepta y aquí se conserva como opción).
  let municipioGuardado = selectMunicipio ? selectMunicipio.value : '';

  function asegurarOpcionMunicipio(valor) {
    if (!selectMunicipio || !valor) return;
    const existe = [...selectMunicipio.options].some((opt) => opt.value === valor);
    if (!existe) {
      const opt = document.createElement('option');
      opt.value = valor;
      opt.textContent = valor;
      opt.dataset.provincia = selectProvincia ? selectProvincia.value : '';
      selectMunicipio.appendChild(opt);
    }
  }

  function filtrarMunicipios() {
    if (!selectProvincia || !selectMunicipio) return;
    const provincia = selectProvincia.value;
    asegurarOpcionMunicipio(municipioGuardado);
    selectMunicipio.querySelectorAll('option[data-provincia]').forEach((opt) => {
      opt.hidden = provincia !== '' && opt.dataset.provincia !== provincia;
    });
    const elegida = selectMunicipio.selectedOptions[0];
    if (elegida && elegida.hidden) selectMunicipio.value = '';
  }

  // Etiquetas de cantidad según la distribución elegida.
  const ETIQUETAS_DISTRIBUCION = {
    torres: ['Cantidad de torres', 'Cantidad de pisos por torre'],
    edificios: ['Cantidad de edificios', 'Cantidad de pisos por edificio'],
  };

  function actualizarEtiquetasEstructura() {
    if (!selectDistribucion) return;
    const textos = ETIQUETAS_DISTRIBUCION[selectDistribucion.value];
    if (etiquetaEdificios) {
      etiquetaEdificios.textContent = textos ? textos[0] : 'Cantidad de edificios/torres';
    }
    if (etiquetaPisos) {
      etiquetaPisos.textContent = textos ? textos[1] : 'Cantidad de pisos por edificio/torre';
    }
  }

  function actualizarVistaPrevia() {
    if (!campoMapa || !zonaMapa || !vistaPrevia) return;
    const codigo = (campoMapa.value || '').trim();
    const esIframe = codigo.toLowerCase().includes('<iframe');
    if (esIframe) {
      vistaPrevia.innerHTML = codigo;
      vistaPrevia.hidden = false;
      if (contenidoZona) contenidoZona.hidden = true;
      zonaMapa.classList.add('con-mapa');
    } else {
      vistaPrevia.innerHTML = '';
      vistaPrevia.hidden = true;
      if (contenidoZona) contenidoZona.hidden = false;
      zonaMapa.classList.remove('con-mapa');
    }
  }

  if (selectProvincia && selectMunicipio) {
    selectProvincia.addEventListener('change', filtrarMunicipios);
    filtrarMunicipios();
  }

  if (selectDistribucion) {
    selectDistribucion.addEventListener('change', actualizarEtiquetasEstructura);
    actualizarEtiquetasEstructura();
  }

  if (campoMapa) {
    campoMapa.addEventListener('input', actualizarVistaPrevia);
    actualizarVistaPrevia();
  }

  if (botonCancelar) {
    botonCancelar.addEventListener('click', () => {
      window.setTimeout(() => {
        filtrarMunicipios();
        actualizarEtiquetasEstructura();
        actualizarVistaPrevia();
      }, 0);
    });
  }

  // Solo lectura: deshabilita todo el formulario.
  if (formulario.dataset.soloLectura === '1') {
    formulario.querySelectorAll('input, select, textarea, button').forEach((el) => {
      el.disabled = true;
    });
  }
})();
