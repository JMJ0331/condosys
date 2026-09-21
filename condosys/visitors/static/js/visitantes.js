/**
 * Lógica del formulario de visitantes (agregar/actualizar).
 *
 * La plantilla agregar.html debe usar:
 *   - un input[type="file"] con data-documento-visitante
 *   - <div id="zona-imagen"> + <img id="vista-previa-imagen"> + <span id="contenido-zona">
 *   - <button id="boton-subir-imagen"> + <span id="nombre-archivo">
 *
 * Gestiona la zona de foto del documento (clic, teclado y
 * arrastrar/soltar) con vista previa. No usa variables de plantilla.
 */
(() => {
  const formulario = document.querySelector('.formulario-agregar');
  if (!formulario) return;

  const inputDocumento = formulario.querySelector('[data-documento-visitante]');
  const zonaImagen = document.getElementById('zona-imagen');
  const vistaPrevia = document.getElementById('vista-previa-imagen');
  const contenidoZona = document.getElementById('contenido-zona');
  const nombreArchivo = document.getElementById('nombre-archivo');
  const botonSubir = document.getElementById('boton-subir-imagen');
  let urlPrevia = null;

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
