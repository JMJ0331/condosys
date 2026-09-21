/**
 * Lógica del formulario de cargo de mantenimiento.
 *
 * La plantilla agregar.html debe usar:
 *   - <input type="file" data-foto-mantenimiento>
 *   - <div id="zona-imagen"> + <img id="vista-previa-imagen"> + <span id="contenido-zona">
 *   - <button id="boton-subir-imagen">
 *   - <span id="nombre-archivo">
 *
 * Abre el selector al pulsar la zona o el botón, muestra la vista previa
 * (en actualizar ya viene con la foto guardada) y acepta arrastrar/soltar.
 * No usa variables de plantilla directamente para poder vivir en static/js.
 */
(() => {
  const inputFoto = document.querySelector('[data-foto-mantenimiento]');
  if (!inputFoto) return;

  const zonaImagen = document.getElementById('zona-imagen');
  const vistaPrevia = document.getElementById('vista-previa-imagen');
  const contenidoZona = document.getElementById('contenido-zona');
  const nombreArchivo = document.getElementById('nombre-archivo');
  const botonSubir = document.getElementById('boton-subir-imagen');
  let urlPrevia = null;

  // En actualizar, si ya hay foto guardada la zona arranca con vista previa.
  if (vistaPrevia && vistaPrevia.getAttribute('src')) {
    vistaPrevia.hidden = false;
    if (contenidoZona) contenidoZona.hidden = true;
  }

  function mostrarVistaPrevia(archivo) {
    if (!archivo || !vistaPrevia) return;
    if (urlPrevia) URL.revokeObjectURL(urlPrevia);
    urlPrevia = URL.createObjectURL(archivo);
    vistaPrevia.src = urlPrevia;
    vistaPrevia.hidden = false;
    if (contenidoZona) contenidoZona.hidden = true;
    if (nombreArchivo) {
      nombreArchivo.textContent = archivo.name;
      nombreArchivo.hidden = false;
    }
  }

  function abrirSelectorImagen() {
    inputFoto.click();
  }

  if (zonaImagen) {
    zonaImagen.addEventListener('click', abrirSelectorImagen);
    zonaImagen.addEventListener('keydown', (evento) => {
      if (evento.key === 'Enter' || evento.key === ' ') {
        evento.preventDefault();
        abrirSelectorImagen();
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
        inputFoto.files = evento.dataTransfer.files;
        mostrarVistaPrevia(evento.dataTransfer.files[0]);
      }
    });
    inputFoto.addEventListener('change', () => {
      if (inputFoto.files.length > 0) mostrarVistaPrevia(inputFoto.files[0]);
    });
  }

  if (botonSubir) {
    botonSubir.addEventListener('click', abrirSelectorImagen);
  }
})();
