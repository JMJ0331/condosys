/**
 * Máscaras de entrada compartidas.
 * - data-mascara="telefono": (000)-000-0000 (solo dígitos, máximo 10).
 * - data-mascara="cedula": 000-0000000-0 (solo dígitos, máximo 11).
 *
 * La plantilla debe marcar los inputs con data-mascara="...".
 * No usa variables de plantilla directamente para poder vivir en static/js.
 */
(() => {
  const MAX_DIGITOS_TELEFONO = 10;
  const MAX_DIGITOS_CEDULA = 11;

  function formatearTelefono(digitos) {
    const d = digitos.slice(0, MAX_DIGITOS_TELEFONO);
    if (d.length <= 3) return d.length > 0 ? `(${d}` : '';
    if (d.length <= 6) return `(${d.slice(0, 3)})-${d.slice(3)}`;
    return `(${d.slice(0, 3)})-${d.slice(3, 6)}-${d.slice(6)}`;
  }

  function formatearCedula(digitos) {
    const d = digitos.slice(0, MAX_DIGITOS_CEDULA);
    if (d.length <= 3) return d;
    if (d.length <= 10) return `${d.slice(0, 3)}-${d.slice(3)}`;
    return `${d.slice(0, 3)}-${d.slice(3, 10)}-${d.slice(10)}`;
  }

  document.querySelectorAll('[data-mascara="telefono"]').forEach((input) => {
    const aplicar = () => {
      input.value = formatearTelefono(input.value.replace(/\D/g, ''));
    };
    aplicar();
    input.addEventListener('input', aplicar);
  });

  document.querySelectorAll('[data-mascara="cedula"]').forEach((input) => {
    const aplicar = () => {
      input.value = formatearCedula(input.value.replace(/\D/g, ''));
    };
    aplicar();
    input.addEventListener('input', aplicar);
  });
})();
