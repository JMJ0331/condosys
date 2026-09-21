/**
 * Lógica del formulario de solicitudes (agregar/actualizar).
 *
 * La plantilla agregar.html debe usar:
 *   - un <select> con data-solicitud-apartamento
 *   - un <select> con data-solicitud-residente (sus opciones llevan data-apartment)
 *   - un input[type="file"] con data-solicitud-documento
 *   - <div id="zona-imagen"> + <img id="vista-previa-imagen"> + <span id="contenido-zona">
 *   - <button id="boton-subir-imagen"> + <span id="nombre-archivo">
 *
 * Filtra residentes por apartamento y gestiona la zona de documento
 * (clic, teclado y arrastrar/soltar) con vista previa para imágenes
 * (los PDF solo muestran su nombre). No usa variables de plantilla.
 */
(() => {
  const formulario = document.querySelector('.formulario-agregar');
  if (!formulario) return;

  const selectApartamento = formulario.querySelector('[data-solicitud-apartamento]');
  const selectResidente = formulario.querySelector('[data-solicitud-residente]');
  const inputDocumento = formulario.querySelector('[data-solicitud-documento]');
  const zonaImagen = document.getElementById('zona-imagen');
  const vistaPrevia = document.getElementById('vista-previa-imagen');
  const contenidoZona = document.getElementById('contenido-zona');
  const nombreArchivo = document.getElementById('nombre-archivo');
  const botonSubir = document.getElementById('boton-subir-imagen');
  let urlPrevia = null;

  // Muestra solo los residentes del apartamento elegido (cada <option>
  // declara su apartamento en data-apartment).
  function filtrarResidentes() {
    if (!selectApartamento || !selectResidente) return;
    const apartamento = selectApartamento.value;
    selectResidente.querySelectorAll('option[data-apartment]').forEach((opt) => {
      opt.hidden = apartamento !== '' && opt.dataset.apartment !== apartamento;
    });
    const elegida = selectResidente.selectedOptions[0];
    if (elegida && elegida.value !== '' && (elegida.dataset.apartment || '') !== apartamento && apartamento !== '') {
      selectResidente.value = '';
    }
  }

  if (selectApartamento && selectResidente) {
    selectApartamento.addEventListener('change', filtrarResidentes);
    filtrarResidentes();
  }

  function mostrarNombreArchivo(archivo) {
    if (!nombreArchivo || !archivo) return;
    nombreArchivo.textContent = archivo.name;
    nombreArchivo.hidden = false;
  }

  function mostrarVistaPrevia(archivo) {
    if (!archivo) return;
    mostrarNombreArchivo(archivo);
    if (!vistaPrevia) return;
    const esImagen = (archivo.type || '').startsWith('image/');
    if (esImagen) {
      if (urlPrevia) URL.revokeObjectURL(urlPrevia);
      urlPrevia = URL.createObjectURL(archivo);
      vistaPrevia.src = urlPrevia;
      vistaPrevia.hidden = false;
      if (contenidoZona) contenidoZona.hidden = true;
    } else {
      vistaPrevia.removeAttribute('src');
      vistaPrevia.hidden = true;
      if (contenidoZona) contenidoZona.hidden = false;
    }
  }

  function abrirSelectorDocumento() {
    if (inputDocumento) inputDocumento.click();
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
