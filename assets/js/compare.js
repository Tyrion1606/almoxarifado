'use strict';
/* Comparação lado a lado dos componentes marcados na tabela. */

function renderCompare() {
  const items = C.components.filter(c => state.selected.has(c.id));
  const rows = [
    {label: 'Disponível / total', value: stockRatio},
    ...C.spec_fields.filter(field => field.in_compare).map(field => ({label: field.label, value: c => fieldValue(c, field)})),
  ];
  const table = `<div class="table-wrap"><table class="compare-table">
      <thead><tr><th>Especificação</th>${items.map(c => `<th class="${tone(familyTone(c))}">${esc(c.name)} <button data-remove="${esc(c.id)}" aria-label="Remover ${esc(c.name)}">×</button></th>`).join('')}</tr></thead>
      <tbody>${rows.map(row => {
        const values = items.map(row.value);
        return `<tr class="${new Set(values).size > 1 ? 'different' : ''}"><th>${annotate(row.label)}</th>${values.map(v => `<td>${annotate(v)}</td>`).join('')}</tr>`;
      }).join('')}</tbody>
    </table></div>`;
  $('#main').innerHTML = `
    <div class="eyebrow">ESCOLHA PARA O SEU PROJETO</div>
    <h1>Comparar componentes</h1>
    <p>Diferenças destacadas em verde. Clock isolado não mede desempenho entre arquiteturas.</p>
    <p class="compare-actions"><button class="pill-button" data-view="catalogo">← Escolher componentes</button> <button class="pill-button" data-clear>Limpar seleção</button></p>
    ${items.length < 2 ? '<div class="info-card empty">Selecione pelo menos dois componentes na tabela para comparar.</div>' : table}`;
}

function syncSelection() {
  const n = state.selected.size, bar = $('#selection-bar');
  $('#compare-count').textContent = n;
  bar.hidden = n === 0 || state.view !== 'catalogo';
  bar.innerHTML = `${plural(n, 'componente selecionado', 'componentes selecionados')} <button data-view="comparar">Comparar →</button><button data-clear>Limpar</button>`;
}
