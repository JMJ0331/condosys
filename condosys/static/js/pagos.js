/**
 * Lógica del formulario de pagos (/pagos/agregar/).
 *
 * La plantilla debe insertar en el formulario:
 *   - un <select> con data-pago-apartamento
 *   - un <select> con data-pago-quien ("Quien paga": propietario/residente)
 *   - un <select> con data-pago-residente
 *     (sus opciones llevan data-apartment y data-tipo)
 *   - un botón opcional con data-url-comprobante="{% url 'generar_comprobante' %}"
 *     (si existe, se habilita al completar el formulario y abre el PDF en otra pestaña)
 *
 * No usa variables de plantilla directamente para poder vivir en static/js.
 */

(() => {
  // Punto de anclaje: el desplegable de apartamento. Si no está, no hay
  // formulario de pago en la página y salimos (sin depender del botón
  // de comprobante, que es opcional y puede no existir).
  const selectApartamento = document.querySelector('[data-pago-apartamento]');
  const formPago = selectApartamento ? selectApartamento.closest('form') : null;
  if (!formPago) return;

  const selectQuien = formPago.querySelector('[data-pago-quien]');
  const selectResidente = formPago.querySelector('[data-pago-residente]');
  const inputComprobante = formPago.querySelector('[data-pago-foto]');
  const btnComprobante = formPago.querySelector('[data-url-comprobante]');

  // Campos que deben tener valor para habilitar el botón "Generar comprobante".
  const camposRequeridos = ['apartment', 'resident', 'amount', 'concept', 'period', 'status'];

  // Muestra solo las personas del departamento elegido y del tipo elegido.
  // Las opciones de residentes declaran su apartamento en data-apartment y su
  // relación en data-tipo (propietario, inquilino, familiar u ocupante);
  // las de propietarios solo declaran data-tipo="propietario" y no se filtran
  // por departamento (el servidor les crea su ficha de residente al guardar).
  // "Quien paga = Residente" muestra todo lo que no sea propietario.
  function filtrarResidentes() {
    if (!selectResidente) return;
    const apartamento = selectApartamento ? selectApartamento.value : '';
    const quien = selectQuien ? selectQuien.value : '';
    selectResidente.querySelectorAll('option[data-tipo]').forEach((opt) => {
      const esPropietario = (opt.dataset.origen || 'residente') === 'propietario';
      const coincideApartamento =
        esPropietario || apartamento === '' || opt.dataset.apartment === apartamento;
      const tipo = opt.dataset.tipo || '';
      const coincideTipo =
        quien === '' ||
        (quien === 'propietario' && tipo === 'propietario') ||
        (quien === 'residente' && tipo !== 'propietario');
      opt.hidden = !(coincideApartamento && coincideTipo);
    });
    const elegida = selectResidente.selectedOptions[0];
    if (elegida && elegida.value !== '' && elegida.hidden) {
      selectResidente.value = '';
    }
  }

  // Textos de la etiqueta y el placeholder del desplegable según quien paga.
  const textosResidente = {
    '': { etiqueta: 'Propietarios/Residentes', placeholder: 'Elegir un propietario/residente' },
    propietario: { etiqueta: 'Propietarios', placeholder: 'Elegir propietario' },
    residente: { etiqueta: 'Residentes', placeholder: 'Elegir residente' },
  };

  // Cambia la etiqueta y el placeholder del desplegable de residentes
  // al mismo tiempo que se filtra (quien paga -> propietario/residente).
  function actualizarTextosResidente() {
    if (!selectResidente || !selectQuien) return;
    const textos = textosResidente[selectQuien.value] || textosResidente[''];
    const campo = selectResidente.closest('.campo-formulario');
    const etiqueta = campo ? campo.querySelector('label') : null;
    if (etiqueta) etiqueta.textContent = textos.etiqueta;
    const placeholder = selectResidente.querySelector('option[value=""]');
    if (placeholder) placeholder.textContent = textos.placeholder;
  }

  // Enlazamos los filtros: apartamento o tipo re-filtran residentes.
  if (selectApartamento) {
    selectApartamento.addEventListener('change', filtrarResidentes);
  }
  if (selectQuien) {
    selectQuien.addEventListener('change', () => {
      actualizarTextosResidente();
      filtrarResidentes();
    });
  }
  actualizarTextosResidente();
  filtrarResidentes();

  // true si todos los campos obligatorios tienen un valor no vacío.
  function formPagoCompleto() {
    return camposRequeridos.every((nombre) => {
      const el = formPago.querySelector(`[name="${nombre}"]`);
      return el && el.value && el.value.trim() !== '';
    });
  }

  // Botón de comprobante opcional: solo se cablea si la plantilla lo incluye.
  // Deshabilita (o habilita) el botón según si el formulario está completo.
  // Así evita generar PDFs con datos faltantes.
  if (btnComprobante) {
    function actualizarBloqueoComprobante() {
      btnComprobante.disabled = !formPagoCompleto();
    }

    // Recalculamos el bloqueo cuando el usuario toque cualquiera de los campos clave.
    camposRequeridos.forEach((nombre) => {
      const el = formPago.querySelector(`[name="${nombre}"]`);
      if (el) {
        el.addEventListener('change', actualizarBloqueoComprobante);
        el.addEventListener('input', actualizarBloqueoComprobante);
      }
    });

    // Estado inicial (por si el formulario ya viene con datos).
    actualizarBloqueoComprobante();

    // Al pulsar "Generar comprobante" enviamos los valores del formulario como
    // query-string a la vista del PDF y lo abrimos en una pestaña nueva.
    btnComprobante.addEventListener('click', () => {
      const params = new URLSearchParams();
      [
        'apartment', 'resident', 'amount', 'concept',
        'period', 'payment_date', 'payment_method', 'status',
      ].forEach((nombre) => {
        const el = formPago.querySelector(`[name="${nombre}"]`);
        if (el && el.value) params.set(nombre, el.value);
      });
      window.open(`${btnComprobante.dataset.urlComprobante}?${params.toString()}`, '_blank');
    });
  }

  // --- Zona de imagen del comprobante: clic, teclado y arrastrar/soltar ---
  const zonaComprobante = document.getElementById('zona-comprobante');
  const vistaPrevia = document.getElementById('vista-previa-comprobante');
  const contenidoZona = document.getElementById('contenido-zona-comprobante');
  const nombreArchivo = document.getElementById('nombre-archivo-comprobante');
  const botonSubir = document.getElementById('boton-subir-comprobante');
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
    if (inputComprobante) inputComprobante.click();
  }

  if (zonaComprobante && inputComprobante) {
    zonaComprobante.addEventListener('click', abrirSelectorImagen);
    zonaComprobante.addEventListener('keydown', (evento) => {
      if (evento.key === 'Enter' || evento.key === ' ') {
        evento.preventDefault();
        abrirSelectorImagen();
      }
    });
    zonaComprobante.addEventListener('dragover', (evento) => {
      evento.preventDefault();
      zonaComprobante.classList.add('zona-activa');
    });
    zonaComprobante.addEventListener('dragleave', () => {
      zonaComprobante.classList.remove('zona-activa');
    });
    zonaComprobante.addEventListener('drop', (evento) => {
      evento.preventDefault();
      zonaComprobante.classList.remove('zona-activa');
      if (evento.dataTransfer.files.length > 0) {
        inputComprobante.files = evento.dataTransfer.files;
        mostrarVistaPrevia(evento.dataTransfer.files[0]);
      }
    });
    inputComprobante.addEventListener('change', () => {
      if (inputComprobante.files.length > 0) mostrarVistaPrevia(inputComprobante.files[0]);
    });
  }

  if (botonSubir) {
    botonSubir.addEventListener('click', abrirSelectorImagen);
  }
})();
