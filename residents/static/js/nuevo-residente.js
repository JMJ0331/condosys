/**
 * Lógica de la página "Agregar residente".
 * Zona de foto con arrastrar/soltar, vista previa y validación
 * de tipo y tamaño (JPG/PNG/WEBP, máx. 2 MB, igual que forms.py).
 *
 * La plantilla nuevo.html debe usar:
 *   - <div id="zona-imagen"> + <img id="vista-previa-imagen"> + <span id="contenido-zona">
 *   - <input type="file" data-residente="foto">
 *   - <button id="boton-subir-imagen">
 *   - <span id="nombre-archivo">
 */
(() => {
  const MAX_MB = 2;
  const TIPOS_PERMITIDOS = ['image/jpeg', 'image/png', 'image/webp'];

  const zonaImagen = document.getElementById('zona-imagen');
  const inputFoto = document.querySelector('[data-residente="foto"]');
  const botonSubir = document.getElementById('boton-subir-imagen');
  const vistaPrevia = document.getElementById('vista-previa-imagen');
  const contenidoZona = document.getElementById('contenido-zona');
  const nombreArchivo = document.getElementById('nombre-archivo');
  let urlPrevia = null;

  if (!zonaImagen || !inputFoto) return;

  function mostrarError(mensaje) {
    if (!nombreArchivo) return;
    nombreArchivo.textContent = mensaje;
    nombreArchivo.hidden = false;
    nombreArchivo.classList.add('error-subida');
  }

  function limpiarError() {
    if (!nombreArchivo) return;
    nombreArchivo.classList.remove('error-subida');
  }

  function mostrarVistaPrevia(archivo) {
    if (!archivo || !vistaPrevia) return;
    if (!TIPOS_PERMITIDOS.includes(archivo.type)) {
      mostrarError('Solo se permiten imágenes JPG, PNG o WEBP.');
      return;
    }
    if (archivo.size > MAX_MB * 1024 * 1024) {
      mostrarError('La imagen no puede superar 2 MB.');
      return;
    }
    limpiarError();
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

  if (botonSubir) {
    botonSubir.addEventListener('click', abrirSelectorImagen);
  }
})();
