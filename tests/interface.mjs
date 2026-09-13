// DOM simulation only. No browser launch, networking, layout or rendering.
import {parseHTML} from './vendor/linkedom.mjs';
import {readFileSync,existsSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const {window}=parseHTML(readFileSync(path.join(root,'index.html'),'utf8'));
const {document}=window;
window.scrollTo=()=>{};
for(const node of document.querySelectorAll('select')) Object.defineProperty(node,'value',{value:'',writable:true});
const dialog=document.querySelector('dialog');dialog.showModal=()=>{dialog.open=true};dialog.close=()=>{dialog.open=false};
const ctx=vm.createContext({window,document,console,innerWidth:1400,innerHeight:1000});
vm.runInContext(readFileSync(path.join(root,'data/catalog.js'),'utf8'),ctx);
vm.runInContext(readFileSync(path.join(root,'assets/app.js'),'utf8'),ctx);
const $=s=>document.querySelector(s),count=()=>document.querySelectorAll('[data-select]').length;
const click=s=>{assert.ok($(s),'Missing '+s);$(s).dispatchEvent(new window.Event('click',{bubbles:true}))};
const input=(s,v)=>{$(s).value=v;$(s).dispatchEvent(new window.Event('input',{bubbles:true}))};
assert.equal(count(),10);
assert.equal(document.querySelectorAll('#inventory thead tr:last-child th').length,19);
assert.equal(document.querySelectorAll('[data-column-toggle]').length,17);
assert.deepEqual([...document.querySelectorAll('.column-groups th')].map(th=>th.textContent),['Acervo','Desempenho e memória','Periféricos','Elétrica','Detalhes']);
assert.match($('#rows').textContent,/Alto desempenho/);assert.doesNotMatch($('#rows').textContent,/A medir/);assert.match($('#rows').textContent,/CORDIC/);assert.match($('#rows').textContent,/USART\/UART/);
{const toggle=$('[data-column-toggle="accelerators"]');toggle.checked=false;toggle.dispatchEvent(new window.Event('change',{bubbles:true}));assert.equal($('#visible-column-count').textContent,'16/17');assert.equal(document.querySelectorAll('#inventory thead tr:last-child th').length,18)}
click('[data-column-move="family"][data-direction="-1"]');assert.equal(document.querySelector('#inventory thead tr:last-child th:nth-child(2)').textContent,'Família ↕');
click('[data-reset-columns]');assert.equal($('#visible-column-count').textContent,'17/17');assert.equal(document.querySelector('#inventory thead tr:last-child th:nth-child(2)').textContent,'Componente ↕');
click('[data-sort="processingClass"]');click('[data-sort="processingClass"]');assert.equal(document.querySelector('[data-select]').dataset.select,'h7r3');
input('#search','PIC12F675');assert.equal(count(),1);assert.match($('#rows').textContent,/PIC12F675/);
input('#search','nada-corresponde');assert.equal(count(),0);assert.match($('#rows').textContent,/Nenhum/);
input('#search','');assert.equal(count(),10);
$('#family').value='STM32';$('#family').dispatchEvent(new window.Event('change',{bubbles:true}));assert.equal(count(),4);
$('#family').value='';$('#family').dispatchEvent(new window.Event('change',{bubbles:true}));
click('[data-expand="blackpill"]');assert.equal($('.detail-cell').getAttribute('colspan'),'19');assert.match($('.tab-content').textContent,/STM32F411CEU6/);assert.match($('.tab-content').textContent,/25 MHz/);
click('[data-tab="pins"]');assert.ok(existsSync(path.join(root,$('.pinout-image').getAttribute('src'))));
click('[data-expand="g474"]');click('[data-tab="pins"]');{const imgs=[...document.querySelectorAll('.pinout-image')];assert.deepEqual(imgs.map(i=>i.getAttribute('src')),['assets/pinouts/g474-long-pinout-simple.png','assets/pinouts/g474-long-pinout-full.png']);imgs.forEach(i=>assert.ok(existsSync(path.join(root,i.getAttribute('src')))))}
click('[data-expand="h7r3"]');click('[data-tab="pins"]');assert.deepEqual([...document.querySelectorAll('.pinout-image')].map(i=>i.getAttribute('src')),['assets/pinouts/h7-pinout-simple.png','assets/pinouts/h7-pinout-full.png']);
click('[data-expand="blackpill"]');click('[data-tab="pins"]');click('[data-tab="pdf"]');assert.ok(existsSync(path.join(root,$('object').getAttribute('data'))));
for(const id of ['pic12f675','g474']){const c=$(`[data-select="${id}"]`);c.checked=true;c.dispatchEvent(new window.Event('change',{bubbles:true}))}
assert.equal($('#compare-count').textContent,'2');click('nav [data-view="comparar"]');assert.match($('#main').textContent,/PIC12F675/);assert.match($('#main').textContent,/WeAct G474 Long/);assert.ok(document.querySelectorAll('.different').length>5);
click('[data-remove="g474"]');assert.match($('#main').textContent,/pelo menos dois/);
click('nav [data-view="glossario"]');input('#glossary-search','analog-to-digital');assert.equal(document.querySelectorAll('.glossary-card').length,1);click('.glossary-card');assert.equal(dialog.open,true);assert.match($('#term-content').textContent,/4096/);click('.close');assert.equal(dialog.open,false);
click('nav [data-view="ferramentas"]');assert.equal(document.querySelectorAll('.tools-grid article').length,3);
click('nav [data-view="catalogo"]');for(const node of document.querySelectorAll('select'))Object.defineProperty(node,'value',{value:'',writable:true});
click('[data-expand="pic12f683"]');vm.runInContext(readFileSync(path.join(root,'data/readers/pic12f683.js'),'utf8'),ctx);click('[data-tab="reader"]');assert.match($('.reader-text').textContent,/PIC12F683/);assert.ok($('.reader-text [data-term]'));click('[data-page-step="1"]');assert.equal(+ $('[data-page]').value,2);input('[data-find-text]','oscillator');click('[data-find-next]');assert.match($('.reader-status').textContent,/Encontrado/);
$('[data-page]').value=99999;$('[data-page]').dispatchEvent(new window.Event('change',{bubbles:true}));assert.equal(+ $('[data-page]').value,176);assert.equal($('[data-page-step="1"]').disabled,true);
click('[data-tab="specs"]');click('.tab-content [data-term="CPU"]');assert.equal(dialog.open,true);
console.log('Interface: busca, filtros, expansão, pinagem, PDF, comparação, glossário, ferramentas e leitor passaram (DOM simulado).');
