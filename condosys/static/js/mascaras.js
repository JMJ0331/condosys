/**
 * Máscaras de entrada compartidas.
 * Formatea los campos con data-mascara="telefono" como (000)-000-0000
 * mientras se escribe (solo dígitos, máximo 10).
 *
 * La plantilla debe marcar los inputs con data-mascara="telefono".
 * No usa variables de plantilla directamente para poder vivir en static/js.
 */
(() => {
  const MAX_DIGITOS = 10;

  function formatearTelefono(digitos) {
    const d = digitos.slice(0, MAX_DIGITOS);
    if (d.length <= 3) return d.length > 0 ? `(${d}` : '';
    if (d.length <= 6) return `(${d.slice(0, 3)})-${d.slice(3)}`;
    return `(${d.slice(0, 3)})-${d.slice(3, 6)}-${d.slice(6)}`;
  }

  function aplicarMascara(input) {
    const digitos = input.value.replace(/\D/g, '');
    input.value = formatearTelefono(digitos);
  }

  document.querySelectorAll('[data-mascara="telefono"]').forEach((input) => {
    aplicarMascara(input);
    input.addEventListener('input', () => aplicarMascara(input));
  });
})();
