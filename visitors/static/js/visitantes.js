/**
 * Lógica del formulario de visitantes (agregar/actualizar).
 *
 * La plantilla agregar.html debe usar:
 *   - un input[type="file"] con data-documento-visitante
 *   - un <select data-visitante="departamento"> cuyas opciones llevan
 *     data-autorizado-ids con los usuarios vinculados a ese departamento
 *   - un <select data-visitante="autorizado">
 *   - <div id="zona-imagen"> + <img id="vista-previa-imagen"> + <span id="contenido-zona">
 *   - <button id="boton-subir-imagen"> + <span id="nombre-archivo">
 *
 * Gestiona el filtro de "Autorizado por" según el departamento elegido y la
 * zona de foto del documento (clic, teclado y arrastrar/soltar) con vista
 * previa. No usa variables de plantilla.
 */
(() => {
  const formulario = document.querySelector('.formulario-agregar');
  if (!formulario) return;

  const inputDocumento = formulario.querySelector('[data-documento-visitante]');
  const selectDepartamento = formulario.querySelector('[data-visitante="departamento"]');
  const selectAutorizado = formulario.querySelector('[data-visitante="autorizado"]');
  const zonaImagen = document.getElementById('zona-imagen');
  const vistaPrevia = document.getElementById('vista-previa-imagen');
  const contenidoZona = document.getElementById('contenido-zona');
  const nombreArchivo = document.getElementById('nombre-archivo');
  const botonSubir = document.getElementById('boton-subir-imagen');
  let urlPrevia = null;

  // --- Autorizado por: solo propietario y residentes del departamento elegido ---

  const SIN_DEPARTAMENTO = 'Elige primero el departamento a visitar';
  const SIN_VINCULO = 'Sin personas vinculadas a este departamento';

  // Copia de las opciones que trae el servidor (id -> texto). El select se
  // reconstruye en cada cambio, así que no puede releerse de sí mismo.
  const personas = new Map();
  const opcionVacia = selectAutorizado
    ? selectAutorizado.querySelector('option[value=""]')
    : null;
  const textoPlaceholder = (opcionVacia && opcionVacia.textContent.trim())
    || 'Elegir quién autorizó';
  if (selectAutorizado) {
    selectAutorizado.querySelectorAll('option').forEach((opcion) => {
      if (opcion.value !== '') personas.set(opcion.value, opcion.textContent.trim());
    });
  }

  // Ids de usuarios vinculados al departamento elegido, leídos de la opción
  // seleccionada (data-autorizado-ids los arma el formulario).
  function vinculadosElegidos() {
    const elegida = selectDepartamento ? selectDepartamento.selectedOptions[0] : null;
    const datos = (elegida && elegida.dataset.autorizadoIds) || '';
    return new Set(datos.split(/\s+/).filter(Boolean));
  }

  function filtrarAutorizado() {
    if (!selectDepartamento || !selectAutorizado) return;
    const vinculados = vinculadosElegidos();
    const elegida = selectAutorizado.value;

    const vacia = document.createElement('option');
    vacia.value = '';
    selectAutorizado.innerHTML = '';
    selectAutorizado.append(vacia);

    const opciones = [...personas]
      .filter(([id]) => vinculados.has(id))
      .map(([id, texto]) => {
        const opcion = document.createElement('option');
        opcion.value = id;
        opcion.textContent = texto;
        return opcion;
      });

    if (opciones.length === 0) {
      vacia.textContent = selectDepartamento.value === '' ? SIN_DEPARTAMENTO : SIN_VINCULO;
      selectAutorizado.disabled = true;
      return;
    }
    vacia.textContent = textoPlaceholder;
    const fragmento = document.createDocumentFragment();
    opciones.forEach((opcion) => fragmento.append(opcion));
    selectAutorizado.appendChild(fragmento);
    selectAutorizado.disabled = false;
    selectAutorizado.value = opciones.some((opcion) => opcion.value === elegida)
      ? elegida
      : '';
  }

  // --- Zona de foto del documento ---

  function mostrarVistaPrevia(archivo) {
    if (!archivo || !vistaPrevia) return;
    if (nombreArchivo) {
      nombreArchivo.textContent = archivo.name;
      nombreArchivo.hidden = false;
    }
    if (urlPrevia) URL.revokeObjectURL(urlPrevia);
    urlPrevia = URL.createObjectURL(archivo);
    vistaPrevia.src = urlPrevia;
    vistaPrevia.hidden = false;
    if (contenidoZona) contenidoZona.hidden = true;
  }

  function abrirSelectorDocumento() {
    if (inputDocumento) inputDocumento.click();
  }

  if (selectDepartamento && selectAutorizado) {
    selectDepartamento.addEventListener('change', filtrarAutorizado);
    filtrarAutorizado();
  }

  if (zonaImagen && inputDocumento) {
    zonaImagen.addEventListener('click', abrirSelectorDocumento);
    zonaImagen.addEventListener('keydown', (evento) => {
      if (evento.key === 'Enter' || evento.key === ' ') {
        evento.preventDefault();
        abrirSelectorDocumento();
      }
    });
    zonaImagen.addEventListener('dragover', (evento) => {
      evento.preventDefault();
      zonaImagen.classList.add('zona-activa');
    });
    zonaImagen.addEventListener('dragleave', () => {
      zonaImagen.classList.remove('zona-activa');
    });
    zonaImagen.addEventListener('drop', (evento) => {
      evento.preventDefault();
      zonaImagen.classList.remove('zona-activa');
      if (evento.dataTransfer.files.length > 0) {
        inputDocumento.files = evento.dataTransfer.files;
        mostrarVistaPrevia(evento.dataTransfer.files[0]);
      }
    });
    inputDocumento.addEventListener('change', () => {
      if (inputDocumento.files.length > 0) mostrarVistaPrevia(inputDocumento.files[0]);
    });
  }

  if (botonSubir) {
    botonSubir.addEventListener('click', abrirSelectorDocumento);
  }
})();
