/**
 * Buscador con autocompletado para selects de departamento.
 *
 * Mejora progresiva: parte de un <select data-autocompletar> nativo, lo oculta
 * y construye una entrada de texto con lista filtrable. El select original se
 * conserva como fuente de verdad y, al elegir una opción, el componente fija su
 * valor y dispara un evento `change` para que el resto de la lógica (filtrado
 * de residentes, autorizaciones, etc.) siga funcionando sin cambios.
 *
 * La lista se inserta en el <body> y se posiciona con coordenadas fijas para
 * no quedar recortada por el `overflow: hidden` de las tarjetas del formulario.
 */
(() => {
  'use strict';

  const normalizar = (valor) =>
    (valor || '')
      .toString()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .trim();

  const instancias = [];
  let contador = 0;

  function inicializar(select) {
    if (select.dataset.autocompletadoActivo === '1') return;

    const opciones = Array.from(select.options);
    const placeholder = (opciones.find((o) => o.value === '') || {}).textContent;
    const reales = opciones
      .filter((o) => o.value !== '')
      .map((o) => ({ valor: o.value, texto: o.textContent.trim() }));

    // Envolvemos el select para conservar su sitio en el formulario.
    const contenedor = document.createElement('div');
    contenedor.className = 'autocompletado';
    select.parentNode.insertBefore(contenedor, select);
    contenedor.appendChild(select);
    select.classList.add('autocompletado-select');

    // La etiqueta (label for) y la obligatoriedad pasan al control visible.
    const idOriginal = select.id;
    const requerido = select.required;
    if (idOriginal) select.removeAttribute('id');
    if (requerido) select.required = false;

    const entrada = document.createElement('input');
    entrada.type = 'text';
    entrada.className = 'autocompletado-entrada';
    entrada.autocomplete = 'off';
    entrada.spellcheck = false;
    entrada.setAttribute('role', 'combobox');
    entrada.setAttribute('aria-autocomplete', 'list');
    entrada.setAttribute('aria-expanded', 'false');
    if (idOriginal) entrada.id = idOriginal;
    if (requerido) entrada.required = true;
    if (placeholder) entrada.placeholder = placeholder || '';
    contenedor.appendChild(entrada);

    const lista = document.createElement('ul');
    lista.className = 'autocompletado-lista';
    lista.setAttribute('role', 'listbox');
    lista.hidden = true;
    const idLista = `lista-autocompletado-${contador++}`;
    lista.id = idLista;
    entrada.setAttribute('aria-controls', idLista);
    document.body.appendChild(lista);

    let visibles = [];
    let indiceActivo = -1;
    let textoSeleccionado = '';
    let eventoInterno = false;

    const seleccionada = opciones.find(
      (o) => o.value === select.value && o.value !== ''
    );
    if (seleccionada) {
      textoSeleccionado = seleccionada.textContent.trim();
      entrada.value = textoSeleccionado;
    }

    const emitirCambio = () => {
      eventoInterno = true;
      select.dispatchEvent(new Event('change', { bubbles: true }));
      eventoInterno = false;
    };

    const estaAbierto = () => !lista.hidden;

    function pintar(filtro) {
      const busqueda = normalizar(filtro);
      visibles = busqueda
        ? reales.filter((o) => normalizar(o.texto).includes(busqueda))
        : reales;

      lista.textContent = '';
      indiceActivo = -1;
      entrada.removeAttribute('aria-activedescendant');

      if (visibles.length === 0) {
        const vacio = document.createElement('li');
        vacio.className = 'autocompletado-vacio';
        vacio.textContent = 'No se encontraron resultados';
        lista.appendChild(vacio);
        return;
      }

      visibles.forEach((opcion, indice) => {
        const item = document.createElement('li');
        item.className = 'autocompletado-opcion';
        item.setAttribute('role', 'option');
        item.id = `${idLista}-${indice}`;
        item.dataset.valor = opcion.valor;
        item.textContent = opcion.texto;
        lista.appendChild(item);
      });
    }

    function posicionar() {
      if (!estaAbierto()) return;
      const rect = entrada.getBoundingClientRect();
      const espacioAbajo = window.innerHeight - rect.bottom;
      const haciaArriba = espacioAbajo < 240 && rect.top > espacioAbajo;
      lista.style.position = 'fixed';
      lista.style.left = `${rect.left}px`;
      lista.style.width = `${rect.width}px`;
      if (haciaArriba) {
        lista.style.top = 'auto';
        lista.style.bottom = `${window.innerHeight - rect.top + 4}px`;
      } else {
        lista.style.bottom = 'auto';
        lista.style.top = `${rect.bottom + 4}px`;
      }
    }

    function establecerActivo(indice) {
      const items = lista.querySelectorAll('.autocompletado-opcion');
      items.forEach((item) => item.classList.remove('activo'));
      indiceActivo = indice;
      if (indice < 0 || indice >= items.length) {
        entrada.removeAttribute('aria-activedescendant');
        return;
      }
      const item = items[indice];
      item.classList.add('activo');
      entrada.setAttribute('aria-activedescendant', item.id);
      item.scrollIntoView({ block: 'nearest' });
    }

    function abrir() {
      if (estaAbierto()) return;
      pintar(entrada.value);
      lista.hidden = false;
      entrada.setAttribute('aria-expanded', 'true');
      posicionar();
      if (select.value !== '') {
        const indice = visibles.findIndex((o) => o.valor === select.value);
        if (indice >= 0) establecerActivo(indice);
      }
    }

    function cerrar() {
      if (!estaAbierto()) return;
      lista.hidden = true;
      entrada.setAttribute('aria-expanded', 'false');
      entrada.removeAttribute('aria-activedescendant');
      indiceActivo = -1;
    }

    function actualizarValidez() {
      const haySeleccion = select.value !== '';
      if (entrada.required && !haySeleccion && entrada.value.trim() !== '') {
        entrada.setCustomValidity('Selecciona una opción de la lista.');
      } else {
        entrada.setCustomValidity('');
      }
    }

    function elegir(indice) {
      const opcion = visibles[indice];
      if (!opcion) return;
      select.value = opcion.valor;
      textoSeleccionado = opcion.texto;
      entrada.value = opcion.texto;
      actualizarValidez();
      cerrar();
      emitirCambio();
    }

    function limpiarSeleccion() {
      if (select.value === '' && textoSeleccionado === '') return;
      textoSeleccionado = '';
      if (select.value !== '') {
        select.value = '';
        emitirCambio();
      }
    }

    entrada.addEventListener('focus', abrir);
    entrada.addEventListener('click', abrir);

    entrada.addEventListener('input', () => {
      if (entrada.value !== textoSeleccionado) {
        textoSeleccionado = '';
        if (select.value !== '') {
          select.value = '';
          emitirCambio();
        }
      }
      if (entrada.value.trim() === '') limpiarSeleccion();
      actualizarValidez();
      pintar(entrada.value);
      abrir();
    });

    entrada.addEventListener('keydown', (evento) => {
      switch (evento.key) {
        case 'ArrowDown':
          evento.preventDefault();
          if (!estaAbierto()) abrir();
          establecerActivo(Math.min(indiceActivo + 1, visibles.length - 1));
          break;
        case 'ArrowUp':
          evento.preventDefault();
          if (!estaAbierto()) abrir();
          establecerActivo(Math.max(indiceActivo - 1, 0));
          break;
        case 'Enter':
          if (estaAbierto()) {
            evento.preventDefault();
            if (indiceActivo >= 0) {
              elegir(indiceActivo);
            } else if (visibles.length === 1) {
              elegir(0);
            }
          }
          break;
        case 'Escape':
          if (estaAbierto()) {
            evento.preventDefault();
            entrada.value = textoSeleccionado;
            cerrar();
          }
          break;
        case 'Tab':
          cerrar();
          break;
        default:
          break;
      }
    });

    entrada.addEventListener('blur', () => {
      setTimeout(() => {
        if (document.activeElement === entrada) return;
        if (entrada.value !== textoSeleccionado) {
          entrada.value = textoSeleccionado;
          actualizarValidez();
        }
        cerrar();
      }, 120);
    });

    lista.addEventListener('mousedown', (evento) => {
      const item = evento.target.closest('.autocompletado-opcion');
      if (!item) return;
      evento.preventDefault();
      const indice = visibles.findIndex((o) => o.valor === item.dataset.valor);
      if (indice >= 0) elegir(indice);
    });

    lista.addEventListener('mouseover', (evento) => {
      const item = evento.target.closest('.autocompletado-opcion');
      if (!item) return;
      const indice = visibles.findIndex((o) => o.valor === item.dataset.valor);
      if (indice >= 0) establecerActivo(indice);
    });

    // Sincroniza el texto si otro código cambia el select por fuera.
    select.addEventListener('change', () => {
      if (eventoInterno) return;
      const opcion = opciones.find((o) => o.value === select.value && o.value !== '');
      textoSeleccionado = opcion ? opcion.textContent.trim() : '';
      entrada.value = textoSeleccionado;
    });

    select.dataset.autocompletadoActivo = '1';
    instancias.push({
      entrada,
      lista,
      estaAbierto,
      cerrar,
      posicionar,
    });
  }

  document.querySelectorAll('select[data-autocompletar]').forEach(inicializar);

  document.addEventListener('mousedown', (evento) => {
    instancias.forEach((instancia) => {
      if (!instancia.estaAbierto()) return;
      if (instancia.entrada.contains(evento.target)) return;
      if (instancia.lista.contains(evento.target)) return;
      instancia.cerrar();
    });
  });

  window.addEventListener('resize', () => {
    instancias.forEach((instancia) => instancia.posicionar());
  });

  window.addEventListener(
    'scroll',
    () => {
      instancias.forEach((instancia) => instancia.posicionar());
    },
    true
  );
})();
