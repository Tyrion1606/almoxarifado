'use strict';
/* Aba Histórico: saldo de unidades, formulário de movimentação (só com scripts/server.py) e linha do tempo. */

function historyPanel(c) {
  const flash = state.flash?.component === c.id ? state.flash : null;
  state.flash = null;
  return `<div class="history">
      <div class="history-side">
        ${flash ? `<p class="form-flash ${flash.error ? 'is-error' : ''}" role="status">${esc(flash.text)}</p>` : ''}
        ${state.writable ? movementForm(c) : readOnlyHint()}
        ${c.estimated ? '<p class="source">* Quantidade estimada: o total veio de um inventário antigo, sem contagem física recente.</p>' : ''}
      </div>
      <div class="history-list">
        <h3>Registro de movimentações</h3>
        ${timeline(c)}
      </div>
    </div>`;
}

function movementForm(c) {
  const types = C.movement_types.map(type => ({type, allowed: movementAllowed(c, type)}));
  const firstAllowed = types.find(t => t.allowed)?.type.id;
  return `<form class="movement-form" data-movement-form="${esc(c.id)}">
      <h3>Registrar movimentação</h3>
      <fieldset class="movement-types">
        <legend class="sr-only">O que aconteceu?</legend>
        ${types.map(({type, allowed}) => `
          <label class="movement-type ${tone(type.tone)}" title="${esc(allowed ? type.description : 'Sem unidades suficientes para este registro')}">
            <input type="radio" name="type_id" value="${esc(type.id)}" ${type.id === firstAllowed ? 'checked' : ''} ${allowed ? '' : 'disabled'}>
            <span>${esc(type.action)}</span>
          </label>`).join('')}
      </fieldset>
      <div class="form-row">
        <label>Quantidade <input name="quantity" type="number" min="1" max="1000" value="1" required></label>
        <label>Data <input name="date" type="date" value="${today()}" max="${today()}" required></label>
      </div>
      <label>Observação <input name="note" maxlength="500" placeholder="Ex.: quebrou o regulador · projeto do robô"></label>
      <div class="form-actions"><button class="primary-button" type="submit">Registrar</button><span class="form-status" aria-live="polite"></span></div>
    </form>`;
}

function readOnlyHint() {
  return `<div class="notice read-only">
      <b>Modo consulta.</b> Para registrar compras, uso e descartes, abra o almoxarifado pelo servidor local.
      No terminal, dentro da pasta do projeto, execute <code>python3 scripts/server.py</code> — ele abre esta página
      com o formulário e grava direto no banco.
    </div>`;
}

/* Mais recente primeiro; cada linha mostra o saldo disponível/total logo depois do registro. */
function timeline(c) {
  if (!c.history.length) return '<p class="empty">Nenhuma movimentação registrada.</p>';
  let total = 0, inUse = 0;
  const entries = c.history.map(movement => {
    const type = movementTypeById.get(movement.type_id);
    total += movement.quantity * type.delta_total;
    inUse += movement.quantity * type.delta_in_use;
    return {movement, type, total, available: total - inUse};
  });
  return `<ol class="timeline">${entries.reverse().map(({movement, type, total, available}) => {
    const sign = type.delta_total > 0 ? '+' : type.delta_total < 0 ? '−' : '';
    return `<li class="${tone(type.tone)}">
        <time datetime="${esc(movement.date)}">${esc(formatDate(movement.date))}</time>
        <div class="timeline-main">
          <span class="badge ${tone(type.tone)}">${esc(type.label)}</span>
          <b>${sign}${plural(movement.quantity, 'unidade', 'unidades')}</b>
          ${movement.note ? `<p>${esc(movement.note)}</p>` : ''}
        </div>
        <span class="timeline-balance" title="Disponível / total depois deste registro">${available}/${total}</span>
        ${state.writable ? `<button class="timeline-delete" data-delete-movement="${movement.id}" aria-label="Apagar registro de ${esc(formatDate(movement.date))}" title="Apagar registro">×</button>` : ''}
      </li>`;
  }).join('')}</ol>`;
}

/* ---------- gravação ---------- */

async function saveMovement(form) {
  const componentId = form.dataset.movementForm;
  const field = name => form.querySelector(`[name="${name}"]`);
  const button = form.querySelector('[type=submit]');
  button.disabled = true;
  form.querySelector('.form-status').textContent = 'Gravando…';
  try {
    const response = await api('api/movements', {
      component_id: componentId,
      type_id: [...form.querySelectorAll('[name="type_id"]')].find(input => input.checked)?.value,
      quantity: Number(field('quantity').value),
      date: field('date').value,
      note: field('note').value,
    });
    applyServerCatalog(response.catalog, componentId, 'Registrado e gravado no banco.');
  } catch (error) {
    button.disabled = false;
    form.querySelector('.form-status').textContent = error.message;
    form.querySelector('.form-status').classList.add('is-error');
  }
}

async function deleteMovement(button) {
  const componentId = button.closest('.detail').dataset.component;
  if (!window.confirm('Apagar este registro do histórico?')) return;
  try {
    const response = await api(`api/movements/${Number(button.dataset.deleteMovement)}/delete`, {});
    applyServerCatalog(response.catalog, componentId, 'Registro apagado.');
  } catch (error) {
    state.flash = {component: componentId, text: error.message, error: true};
    drawRows();
  }
}

function applyServerCatalog(catalog, componentId, message) {
  loadCatalog(catalog);
  state.flash = {component: componentId, text: message};
  drawRows();
}
