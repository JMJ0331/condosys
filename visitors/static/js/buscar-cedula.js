/**
 * Buscador inteligente por cédula (cámara o archivo).
 *
 * La plantilla debe usar:
 *   - <dialog id="dialog-buscar-cedula">
 *   - <video id="video-cedula"> + <canvas id="lienzo-cedula">
 *   - <input type="file" id="archivo-cedula" data-cedula-archivo>
 *   - <img id="vista-previa-cedula"> + <p id="error-camara-cedula">
 *   - <button id="boton-camara-cedula"> + <button id="boton-capturar-cedula">
 *
 * La foto (capturada o elegida) queda en el input de archivo y el
 * formulario la envía por POST clásico. Sin variables de plantilla.
 */
(() => {
  const dialogo = document.getElementById('dialog-buscar-cedula');
  if (!dialogo) return;

  const botonCamara = document.getElementById('boton-camara-cedula');
  const botonCapturar = document.getElementById('boton-capturar-cedula');
  const video = document.getElementById('video-cedula');
  const lienzo = document.getElementById('lienzo-cedula');
  const inputArchivo = document.getElementById('archivo-cedula');
  const vistaPrevia = document.getElementById('vista-previa-cedula');
  const errorCamara = document.getElementById('error-camara-cedula');
  let flujo = null;
  let urlPrevia = null;

  function mostrarError(mensaje) {
    if (errorCamara) {
      errorCamara.textContent = mensaje;
      errorCamara.hidden = false;
    }
  }

  function ocultarError() {
    if (errorCamara) errorCamara.hidden = true;
  }

  function detenerCamara() {
    if (flujo) {
      flujo.getTracks().forEach((pista) => pista.stop());
      flujo = null;
    }
    if (video) {
      video.pause();
      video.removeAttribute('srcObject');
      video.srcObject = null;
      video.hidden = true;
    }
    if (botonCapturar) botonCapturar.hidden = true;
    if (botonCamara) botonCamara.hidden = false;
  }

  function mostrarVistaPrevia(archivo) {
    if (!archivo || !vistaPrevia) return;
    if (urlPrevia) URL.revokeObjectURL(urlPrevia);
    urlPrevia = URL.createObjectURL(archivo);
    vistaPrevia.src = urlPrevia;
    vistaPrevia.hidden = false;
  }

  if (botonCamara) {
    botonCamara.addEventListener('click', async () => {
      ocultarError();
      if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
        mostrarError('La cámara requiere HTTPS o localhost en este navegador.');
        return;
      }
      try {
        flujo = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' },
        });
        video.srcObject = flujo;
        await video.play();
        video.hidden = false;
        botonCamara.hidden = true;
        if (botonCapturar) botonCapturar.hidden = false;
      } catch (error) {
        mostrarError('No se pudo abrir la cámara. Revisa el permiso del navegador.');
      }
    });
  }

  if (botonCapturar) {
    botonCapturar.addEventListener('click', () => {
      if (!flujo || !video.videoWidth) return;
      ocultarError();
      lienzo.width = video.videoWidth;
      lienzo.height = video.videoHeight;
      lienzo.getContext('2d').drawImage(video, 0, 0);
      lienzo.toBlob((blob) => {
        if (!blob || !inputArchivo) return;
        const archivo = new File([blob], 'cedula.jpg', { type: 'image/jpeg' });
        const transferencia = new DataTransfer();
        transferencia.items.add(archivo);
        inputArchivo.files = transferencia.files;
        mostrarVistaPrevia(archivo);
        detenerCamara();
      }, 'image/jpeg', 0.92);
    });
  }

  if (inputArchivo) {
    inputArchivo.addEventListener('change', () => {
      ocultarError();
      if (inputArchivo.files.length > 0) mostrarVistaPrevia(inputArchivo.files[0]);
    });
  }

  // Al cerrar el diálogo se apaga la cámara si quedó encendida.
  dialogo.addEventListener('close', detenerCamara);
})();
