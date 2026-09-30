/**
 * Máscaras de entrada compartidas.
 * - data-mascara="telefono": (000)-000-0000 (solo dígitos, máximo 10).
 * - data-mascara="telefono-admin": 000-000-0000 (solo dígitos, máximo 10).
 * - data-mascara="cedula": 000-0000000-0 (solo dígitos, máximo 11).
 * - data-mascara="rnc": 000-00000-0 (solo dígitos, máximo 9).
 *
 * La plantilla debe marcar los inputs con data-mascara="...".
 * No usa variables de plantilla directamente para poder vivir en static/js.
 */
(() => {
  const MAX_DIGITOS_TELEFONO = 10;
  const MAX_DIGITOS_TELEFONO_ADMIN = 10;
  const MAX_DIGITOS_CEDULA = 11;
  const MAX_DIGITOS_RNC = 9;

  function formatearTelefono(digitos) {
    const d = digitos.slice(0, MAX_DIGITOS_TELEFONO);
    if (d.length <= 3) return d.length > 0 ? `(${d}` : '';
    if (d.length <= 6) return `(${d.slice(0, 3)})-${d.slice(3)}`;
    return `(${d.slice(0, 3)})-${d.slice(3, 6)}-${d.slice(6)}`;
  }

  function formatearTelefonoAdmin(digitos) {
    const d = digitos.slice(0, MAX_DIGITOS_TELEFONO_ADMIN);
    if (d.length <= 3) return d;
    if (d.length <= 6) return `${d.slice(0, 3)}-${d.slice(3)}`;
    return `${d.slice(0, 3)}-${d.slice(3, 6)}-${d.slice(6)}`;
  }

  function formatearCedula(digitos) {
    const d = digitos.slice(0, MAX_DIGITOS_CEDULA);
    if (d.length <= 3) return d;
    if (d.length <= 10) return `${d.slice(0, 3)}-${d.slice(3)}`;
    return `${d.slice(0, 3)}-${d.slice(3, 10)}-${d.slice(10)}`;
  }

  function formatearRnc(digitos) {
    const d = digitos.slice(0, MAX_DIGITOS_RNC);
    if (d.length <= 3) return d;
    if (d.length <= 8) return `${d.slice(0, 3)}-${d.slice(3)}`;
    return `${d.slice(0, 3)}-${d.slice(3, 8)}-${d.slice(8)}`;
  }

  document.querySelectorAll('[data-mascara="telefono"]').forEach((input) => {
    const aplicar = () => {
      input.value = formatearTelefono(input.value.replace(/\D/g, ''));
    };
    aplicar();
    input.addEventListener('input', aplicar);
  });

  document.querySelectorAll('[data-mascara="telefono-admin"]').forEach((input) => {
    const aplicar = () => {
      input.value = formatearTelefonoAdmin(input.value.replace(/\D/g, ''));
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

  document.querySelectorAll('[data-mascara="rnc"]').forEach((input) => {
    const aplicar = () => {
      input.value = formatearRnc(input.value.replace(/\D/g, ''));
    };
    aplicar();
    input.addEventListener('input', aplicar);
  });
})();
