/**
 * Lógica de la página Mi perfil.
 * - Interruptor Activo: sincroniza el hidden `status` (active/inactive).
 * - Zona de imagen circular: clic, teclado, arrastrar y vista previa
 *   + nombre del archivo elegido.
 *
 * La plantilla debe usar:
 *   - <input type="checkbox" id="toggle-activo">
 *   - <input type="hidden" id="id_status">
 *   - <input type="file" data-perfil-foto>
 *   - <div id="zona-imagen"> + <img id="vista-previa-imagen">
 *     + <span id="contenido-zona">
 *   - <button id="boton-subir-imagen">
 *   - <span id="nombre-archivo">
 */

(() => {
  const toggleActivo = document.getElementById('toggle-activo');
  const inputStatus = document.getElementById('id_status');

  function sincronizarEstado() {
    if (toggleActivo && inputStatus) {
      inputStatus.value = toggleActivo.checked ? 'active' : 'inactive';
    }
  }

  if (toggleActivo && inputStatus) {
    toggleActivo.addEventListener('change', sincronizarEstado);
    sincronizarEstado();
  }

  const inputFoto = document.querySelector('[data-perfil-foto]');
  const zonaImagen = document.getElementById('zona-imagen');
  const vistaPrevia = document.getElementById('vista-previa-imagen');
  const contenidoZona = document.getElementById('contenido-zona');
  const nombreArchivo = document.getElementById('nombre-archivo');
  const botonSubir = document.getElementById('boton-subir-imagen');
  let urlPrevia = null;

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
    if (inputFoto) inputFoto.click();
  }

  if (zonaImagen && inputFoto) {
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
