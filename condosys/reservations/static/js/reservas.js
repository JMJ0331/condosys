/**
 * Lógica del formulario de reservas.
 *
 * La plantilla debe insertar en el formulario:
 *   - un <select> con data-reserva-apartamento
 *   - un <select> con data-reserva-residente (sus opciones llevan data-apartment)
 *
 * Filtra los propietarios/residentes según el apartamento elegido.
 */

(() => {
  const form = document.querySelector('form[data-form-reserva]');
  if (!form) return;

  const selectApartamento = form.querySelector('[data-reserva-apartamento]');
  const selectResidente = form.querySelector('[data-reserva-residente]');
  if (!selectApartamento || !selectResidente) return;

  function filtrarResidentes() {
    const apartamento = selectApartamento.value;
    selectResidente.querySelectorAll('option[data-apartment]').forEach((opt) => {
      opt.hidden = apartamento !== '' && opt.dataset.apartment !== apartamento;
    });
    if (
      selectResidente.selectedOptions[0]?.dataset.apartment &&
      selectResidente.value !== '' &&
      selectResidente.selectedOptions[0].dataset.apartment !== apartamento
    ) {
      selectResidente.value = '';
    }
  }

  selectApartamento.addEventListener('change', filtrarResidentes);
  filtrarResidentes();
})();