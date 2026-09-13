# Handoff — Almoxarifado

Atualizado em 12/09/2026. Este documento é a entrada de contexto para agentes futuros.

## 1. Objetivo e contrato com o usuário

Catálogo pessoal de componentes para comparar os itens que o usuário possui e escolher um microcontrolador para cada projeto. A primeira categoria é microcontroladores; outras serão acrescentadas depois. A experiência principal é uma tabela expansível, com ficha técnica, pinagem, datasheet e documentação educativa integrada.

Repositório local: `/home/davi/repos/almoxarifado`. O projeto começou com apenas README e commit inicial `af3e1a1`. Não havia código ou alterações locais a preservar. O usuário autorizou implementar e comitar o projeto e o banco; não pediu publicação web. Não foi feito push nesta entrega.

Requisitos prioritários:

- Clonar e abrir, sem instalação, servidor, conta ou senha.
- SQLite versionado; atualização distribuída por Git pull/push.
- Conteúdo legível em português, termos explicados, poucas etapas para usar.
- Preservar outros repositórios, Obsidian, TCC e montagens físicas.
- README curto; este handoff completo e atualizado junto com cada melhoria.
- Não realizar alterações físicas, programação de placas ou pedir segredos.

## 2. Arquitetura e decisões

**Página estática em HTML (HyperText Markup Language), CSS (Cascading Style Sheets) e JavaScript**, sem framework, dependências de execução ou hospedagem. A folha de estilo usa fontes do sistema. O arquivo `index.html` é a entrada final, não uma etapa de build.

**SQLite é a fonte canônica dos dados**, mas não é consultado em tempo de execução pelo navegador. Navegadores não abrem automaticamente um SQLite vizinho via `file://` como uma aplicação nativa. Para preservar “clonar e abrir”, `scripts/export.py` gera `data/catalog.js`, um snapshot (cópia de leitura) do banco carregado por uma tag script clássica. Não usa fetch, módulos externos, servidor, armazenamento do navegador, WebAssembly ou CDN (Content Delivery Network, rede de distribuição).

O mesmo exportador gera `data/inventory.sql`, uma representação textual revisável do banco. Atualizações devem incluir SQLite, SQL e catálogo JS no mesmo commit. Nunca editar os arquivos gerados para mudar dados: editar SQLite e exportar.

A aplicação é de consulta. Busca, filtros e seleção para comparar não são persistidos. Não há formulário de cadastro: não foi solicitado um fluxo de edição na interface; o usuário quer evolução via agentes e Git. Se isso mudar, discutir uma interface explícita de importação/exportação de arquivo ou um pequeno servidor local. Não introduzir servidor apenas por preferência técnica.

O plugin Sites foi solicitado e suas orientações de interface e SQLite foram consultadas. A solicitação expressa de funcionamento local dispensa registro e publicação. Não há projeto hospedado, `.openai/hosting.json`, conta Cloudflare ou credenciais. O pacote Sites inicialmente legível deixou de aparecer no cache durante o trabalho; não foi possível executar seu configurador (Node inicialmente fora do PATH e, posteriormente, pacote ausente). Isso não afeta os arquivos estáticos entregues.

## 3. Organização

| Caminho | Responsabilidade |
| --- | --- |
| `index.html` | Estrutura, navegação, primeira tela e ícone incorporado |
| `assets/style.css` | Aparência, tabela, painel, modal, responsividade |
| `assets/app.js` | Renderização, filtros, ordenação, comparação, glossário, leitura |
| `data/inventory.sqlite` | Banco canônico, incluído no Git |
| `data/inventory.sql` | Dump textual determinístico; permite reconstrução e revisão |
| `data/catalog.js` | Snapshot determinístico para `file://` |
| `data/sources.json` | URLs, data de obtenção e SHA-256 dos documentos |
| `data/readers/*.js` | Texto de cada PDF separado por página, carregado sob demanda |
| `assets/documents/*.pdf` | 16 documentos originais locais |
| `assets/pinouts/*.png` | 10 prévias recortadas de páginas e renders oficiais |
| `assets/pinouts/sources/*.png` | Desenhos de pinagem sem PDF oficial, como baixados |
| `data/pinout_sources.json` | URL, SHA-256, crédito e licença desses desenhos |
| `docs/evidence/blackpill-variant.png` | Print fornecido pelo usuário da variante adquirida |
| `docs/SOURCES.md` | Proveniência, créditos e versões documentais |
| `docs/H7R3-PINOUT.md` | Pinagens simples/completa da H7R3, esferas UFBGA144 SMPS GP, paridade das fileiras dos headers duplos e tabela de conferência |
| `docs/G474-PINOUT.md` | Pinagens simples/completa da G474, regra UFQFPN48 × LQFP48, histórico da correção e tabela pino a pino |
| `scripts/export.py` | Atualiza e confere catálogo JS e dump SQL |
| `scripts/seed.py` | Restaura banco ausente a partir do dump; recusa sobrescrita |
| `scripts/download_sources.py` | Lista explícita de downloads públicos; uso de manutenção |
| `scripts/prepare_documents.py` | Extração textual dos datasheets usando Poppler |
| `scripts/prepare_pinouts.py` | Recorta todas as pinagens; requer Poppler e Pillow |
| `tests/test_inventory.py` | Integridade, arquivos, variantes, hashes e reconstrução |
| `tests/interface.mjs` | Fluxos da interface em DOM simulado |
| `tests/vendor/` | LinkeDOM 0.18.12 e licença MIT, somente para testes |

Nenhum recurso de execução depende de caminhos absolutos desta máquina. O print foi copiado do anexo, não referenciado em `/tmp`. A página também pode ser servida como arquivos estáticos por qualquer servidor, mas isso não é requisito.

## 4. Modelo de dados

SQLite `PRAGMA user_version=1`.

- `categories(id, name)`: inclui `microcontroladores`.
- `components(id, category_id, name, family, kind, quantity, estimated, specs)`.
  - `kind`: `chip` ou `placa`; quantidade inteira não negativa.
  - `estimated`: 0 ou 1; apenas quantidades PIC são estimadas.
  - `specs`: JSON (JavaScript Object Notation) validado pelo SQLite, com os campos técnicos. A escolha mantém flexibilidade para categorias futuras sem dezenas de colunas nulas.
  - `clock`: número em MHz; `ram`: inteiro em bytes.
  - `flash`, `external`, `adc`, `gpio`, etc.: texto com unidades, qualificações e escopo.
  - `datasheet`, `pinout`, `pinout_source`, `schematic`: nomes de arquivos locais.
  - `pinouts` (opcional): lista ordenada `{file, title, notice}` exibida uma abaixo da outra na aba Pinagem; `pinout` continua sendo o primeiro arquivo. Hoje G474 (`g474-long-pinout-simple.png`, `-full.png`) e H7R3 (`h7-pinout-simple.png`, `-full.png`) usam.
  - `origin`, `notes`, `status`, `evidence`, `variant`: contexto do acervo.
- `glossary(term, meaning, short, detail, example)`: 91 entradas; significado completo, explicação curta, aprofundamento e exemplo no acervo.
- `tools(id, name, quantity, description, compatibility)`: acessórios de programação/conexão.

Não há índices especulativos além de chaves primárias; apenas 10 componentes são exportados integralmente e filtrados na memória do navegador. Uma categoria futura exigirá também adaptar navegação, cabeçalhos e campos da interface; adicionar uma linha em categories sozinho não implementa nova experiência.

## 5. Acervo e identificação

| Item | Quantidade | Identificação / estado |
| --- | ---: | --- |
| PIC16F887-I/P | 2 estimadas | PDIP-40, 8.192 palavras de 14 bits, 368 B SRAM |
| PIC12F675-I/P | 3 estimadas | PDIP-8, sem PWM por hardware |
| PIC12F683-I/P | 2 estimadas | PDIP-8, CCP/PWM |
| PIC12F1501-I/P | 3 estimadas | PDIP-8, PWM/CLC/NCO/CWG, HEF |
| Arduino Uno | 1 | Referência Uno R3/ATmega328P; revisão física não especificada |
| Arduino Nano | 2 | Referência Nano clássico/ATmega328P; um soldado em PCB, um solto |
| BluePill | 3 | STM32F103C8T6 confirmado pelo usuário em 12/09/2026: duas unidades com conector USB-C e uma com micro-USB |
| WeAct BlackPill | 1 | STM32F411CEU6, HSE 25 MHz, Flash externa 8 MB, em uso no TCC |
| WeAct G474 Long | 1 | STM32G474CEU6, UFQFPN48, 512 KiB Flash e 128 KiB SRAM; recém-adquirida |
| WeAct H7R3 | 1 | STM32H7R3Z8J6, UFBGA144, 64 KiB internos e 8 MiB externos; recém-adquirida |

Total: 19 unidades (inclui estimativas e duas recém-adquiridas); não declarar recebimento ou teste das novas placas.

Ferramentas: 1 CH343P, 1 ST-Link V2, 1 PICkit 3. “picokit 3” foi normalizado para PICkit 3. Não são contadas como microcontroladores.

### Fontes pessoais lidas, sem modificação

- `/home/davi/repos/obsidian-vault/Peças disponiveis/Inventario_Componentes_Eletronicos_Obsidian.md` — documento de 07/05/2026. Contém os quatro PICs e quantidades estimadas. BT145 e IRFP4227 não foram importados porque a categoria solicitada é microcontroladores.
- `/home/davi/repos/TCC/DOCUMENTACAO_TECNICA_CRONOLOGICA.md` — identifica a BlackPill STM32F411CEU6, cristal de 25 MHz e uso da CPU a 96 MHz. Seção 7.5 continha incerteza histórica de capacidade da Flash externa.
- `/home/davi/repos/obsidian-vault/TCC - PIPboy/BlackPill - STM32F411 + 25Mhz + 8M flash.md`.
- `/home/davi/repos/obsidian-vault/TCC - PIPboy/Firmware para leitura e Gravação em 8M de Flash.md` — informa Flash montada e ligações propostas.
- Conversa “Comparar placas STM32”, id `6a9714da-dba0-83e9-8e38-df50b08b01bc`, consultada nesta tarefa. A resposta final corrigida identifica CEU6 Long como 512 KB Flash / 128 KB RAM; não reaproveitar a identificação errada de um anúncio anterior.
- Usuário confirmou nesta tarefa: BlackPill com Flash externa **8 MB**, WeAct. Essa confirmação substitui a incerteza histórica. Print `docs/evidence/blackpill-variant.png` mostra a opção **F411 25M HSE 8MFlash**. Não registrar novamente como capacidade desconhecida.

Em 12/09/2026 o usuário confirmou que as três BluePill são STM32F103C8T6, duas com conector USB-C e uma com micro-USB. Isso encerra a incerteza anterior: a ficha deixou de ser marcada como referência. A busca local havia encontrado uma conversa citada como “Branch · Software para programar Bluepill”, mas o texto consolidado correspondente descreve BlackPill F411; não confundir nome de conversa com prova de MCU, nem importar a identificação de um módulo ADS1256 + F103 de outro projeto como se fosse a BluePill. Continua valendo: não assumir 128 KiB de Flash, porque o datasheet C8 declara 64 KiB.

## 6. Notas técnicas a preservar

- Memória PIC deve conservar **palavras × 14 bits**. KiB é uma equivalência de capacidade, não garante que toolchains tratem programa como bytes comuns.
- SRAM em bytes no banco; interface converte para KiB (kibibytes, 1.024 bytes). MiB = 1.048.576 bytes. Anúncios frequentemente usam KB/MB para capacidades binárias.
- BlackPill: 512 KiB internos, 128 KiB SRAM, 8 MiB de Flash SPI externa conforme confirmação do usuário. F411 não tem DAC nem CAN. O clock máximo é 100 MHz; 96 MHz é configuração do TCC, 25 MHz é cristal externo.
- Flash externa montada não prova que o logger esteja implementado no firmware do TCC. Não mudar essa afirmação sem revisar o firmware.
- G474CEU6: 512 KiB Flash; SRAM 96 + 32 KiB CCM. Long é formato físico; não implica mais pinos que a versão compacta CEU6. O diagrama incluído é QFN48 Long, não QFP48 nem compacto. **Número de pino do CI = coluna UFQFPN48 da tabela 12 do DS12288**, nunca LQFP48 (o LQFP48 nem tem PC4/PC6/PC10/PC11 e desloca a numeração a partir de PB0). Versões antigas do desenho simples tinham 13 números errados (PB10, VREF+, PB11–PB15, PC6, PA8–PA12); as duas imagens atuais estão corrigidas e conferidas. Detalhes e tabela em `docs/G474-PINOUT.md`.
- H7R3: 64 KiB de Flash interna podem hospedar boot e/ou código; não tratar como zero Flash nem como 8 MB internos. A placa WeAct adiciona 8 MB externos. H7R3 **não possui DAC**; fonte usada DS14360 Rev 3. Possui Cortex-M7 com FPU de dupla precisão. Não importar recursos gráficos de H7R7 indiscriminadamente para H7R3.
- GPIO, ADC, DAC e interfaces da família não equivalem automaticamente a sinais expostos na placa nem disponíveis simultaneamente. Verificar encapsulamento e funções alternativas.
- PIC12: GP3/RA3 somente entrada. PIC16F887: RE3 somente entrada. PIC12F675 não tem PWM de hardware. PIC12F1501 usa HEF, não EEPROM clássica.
- PIC ICSP e conector ICSP AVR têm protocolos/sinais diferentes. PICkit 3 não é programador AVR genérico.
- CH343P é ponte USB–UART, não depurador SWD. Níveis elétricos do módulo precisam ser conferidos quando for conectar.
- ST-Link V2: não prometer H7RS sem conferir versão do software, firmware e suporte do gravador. Nenhuma gravação física foi feita.

## 7. Interface e documentação interativa

`app.js` renderiza as linhas a partir do catálogo, usando escape de conteúdo. Delegação de eventos mantém as ações disponíveis após rerender. A seleção de comparação está num Set em memória. A tabela oferece 17 colunas configuráveis, que podem ser exibidas, ocultadas, reordenadas e restauradas; preferências ficam no `localStorage` do navegador. Cabeçalhos com seta ordenam as linhas. Filtros por família e tipo e busca percorrem os campos do item.

As métricas de processamento exibidas são a classe editorial e os aceleradores confirmados para cada componente. Benchmarks e medições comparáveis serão incluídos somente quando houver valores reais no inventário.

Cada linha abre uma seção com abas: especificações, pinagem, datasheet comentado e original. Abas respondem às setas, Home e End. Ajuda rápida aparece por hover/foco; clique abre um dialog nativo que oferece fechamento e Escape. Termos também podem ser acessados por toque. Layout possui adaptações até telas estreitas e rolagem horizontal da tabela.

**Largura e tipografia (12/09/2026):** a tabela rola na horizontal dentro de `.table-wrap`, que tem `position:relative`. Sem isso, o `.sr-only` do cabeçalho (`position:absolute`) escapava e alargava a página até ~2.983 px. O detalhamento (`.detail-cell>.detail`) é `position:sticky;left:0` e usa a largura visível da tabela via `--detail-width`, atualizada por `fitDetailWidth()` a cada `drawRows` e `resize`. As imagens de pinagem usam `max-width:100%` e `max-height:min(750px,80vh)`, sem faixas brancas. A interface fora do detalhamento e a tabela visível foram ampliadas (tabela 13,5 px, cabeçalho 12 px, título 40 px); as colunas usam `columnWidth()` = largura base × 1,15. O detalhamento mantém os tamanhos originais: `td.detail-cell` fixa 12 px e os seletores ampliados excluem `.detail-cell`. Conferido no Chrome em 1920, 1440, 1100, 700 e ~480 px: largura da página igual à da janela.

**Datasheet comentado:** arquivo JS por PDF, carregado sob demanda por tag script clássica (compatível com `file://`). Contém páginas de texto extraídas por `pdftotext -layout`, navegação e busca circular por página. Um reconhecedor insensível a maiúsculas transforma os 91 termos cadastrados em botões. Não é um tradutor, modelo de linguagem nem glossário de todas as palavras dos PDFs. Subsímbolos como VDD com formatação especial ou texto dentro de desenhos podem não casar com o reconhecedor.

**Documento original:** objeto PDF local com link alternativo. Diagramação e desenhos do fabricante são preservados. O visualizador nativo de PDF não recebe os tooltips do aplicativo; estes ficam na leitura comentada e nas fichas. Comportamento do visualizador varia conforme navegador. Não prometer anotação visual sobre cada palavra do PDF original.

**Pinagem:** recortes de páginas e imagens oficiais, sem desenho inventado ou arte gerada por IA. `scripts/prepare_pinouts.py` descarta cabeçalho, rodapé, espaço vazio e encapsulamentos que não estão no acervo, e empilha diagrama e tabela de funções quando o fabricante as publica em páginas separadas. Cada ficha mostra o crédito da imagem, gravado em `pinout_credit`.

Os quatro PICs trazem o diagrama PDIP mais a tabela de alocação de funções. Uno e Nano usam a folha oficial Arduino, inclusive a legenda de cores e o aviso de licença. BluePill passou a usar *The Generic STM32F103 Pinout Diagram* de Rasmus Friis Kjeldsen, CC BY-SA 4.0 — desenho da placa, com funções alternativas e limites elétricos; a imagem mostra a variante micro-USB, e duas das três unidades são USB-C. Obra derivada desse desenho precisa manter a mesma licença. **Exceção à regra de não redesenhar:** a pedido do usuário, a H7R3 mostra `h7-pinout-simple.png` e, abaixo, `h7-pinout-full.png`, desenhos do almoxarifado no mesmo estilo dos da G474. Pino do CI = esfera da coluna UFBGA144 SMPS GP (não a GFx); headers duplos com paridade invertida: externa = par em P1/P3, ímpar em P2/P4; LTDC, ETH MII e Hexa-SPI omitidos por não existirem no Z8J6. Leia `docs/H7R3-PINOUT.md`. O recorte `h7-pinout.png` continua gerado por `prepare_pinouts.py`, mas não é exibido. A G474 Long mostra dois desenhos feitos para o almoxarifado, empilhados pelo campo `pinouts`: `g474-long-pinout-simple.png` (colunas sobre o render WeAct; funções principais) e, abaixo, `g474-long-pinout-full.png` (vetorial; todas as AF0–AF15 com número, funções adicionais, tolerância FT/TT e pinos fora dos headers). Ambas usam a numeração UFQFPN48 conferida na tabela 12 e no esquema. São os únicos arquivos de pinagem da G474; o antigo recorte `g474-long-pinout.png` e a receita dele em `prepare_pinouts.py` foram removidos. Leia `docs/G474-PINOUT.md` antes de alterar essas imagens. A pinagem da BlackPill não foi alterada a pedido do usuário: continua sendo o desenho WeAct v2.0+ de Richard Balint, byte a byte igual, com anotações de família — o datasheet F411 prevalece para recursos do chip.

## 8. Manutenção

Executar na raiz do clone. Uso normal só precisa do navegador. Manutenção do banco requer Python 3 com sqlite3 (biblioteca padrão). Extração textual requer Poppler; recortar pinagens requer Poppler e Pillow (`python3-pil`); testes DOM requerem Node.js moderno, que nesta máquina não está no PATH (há um binário em `~/.lmstudio/.internal/utils/node`). Nenhuma dependência é instalada ao abrir o site.

Depois de editar o SQLite:

```bash
# Gera a página de dados e a representação SQL revisável a partir do banco.
python3 scripts/export.py

# Confere se os dois arquivos gerados correspondem exatamente ao banco.
python3 scripts/export.py --check

# Valida banco, fontes, arquivos e reconstrução.
python3 -m unittest discover -s tests -v

# Testa as interações em uma árvore de documento simulada, sem navegador.
node tests/interface.mjs
```

A opção `--check` não grava; falha se qualquer snapshot estiver desatualizado. `-m` executa módulo Python; `discover -s tests` procura testes na pasta tests; `-v` detalha os resultados. `node` executa JavaScript fora do navegador.

Para adicionar componente, usar uma migração explícita no SQLite com parâmetros e transação; preencher proveniência e pendências. Para permitir revisão, exportar e revisar `git diff -- data/inventory.sql`. Nunca excluir o banco para rodar seed: o seed é apenas restauração quando o banco não existe, a partir do SQL versionado.

Atualização voluntária dos documentos:

```bash
# Obtém apenas documentos listados que ainda não estão presentes; requer internet.
python3 scripts/download_sources.py

# Extrai o texto dos datasheets; requer Poppler instalado.
python3 scripts/prepare_documents.py

# Recorta todas as pinagens; requer Poppler e Pillow.
python3 scripts/prepare_pinouts.py

# Inclui a proveniência atualizada no snapshot do catálogo.
python3 scripts/export.py
```

O script de download não atualiza silenciosamente um PDF existente. Para mudar revisão, preservar o anterior até validar o substituto, alterar a lista explicitamente, conferir contagem/pinagens e atualizar docs/SOURCES.md. Hashes são SHA-256 (resumo criptográfico do conteúdo), úteis para detectar alteração dos arquivos.

### Git e conflitos de banco

Banco binário não deve ser mesclado automaticamente. Rever as alterações SQL dos dois lados, resolver a intenção das mudanças, aplicar numa cópia validada e gerar os snapshots novamente. Não executar o dump de uma versão por cima de um banco existente. O teste de roundtrip já verifica que a versão SQL atual reconstrói os mesmos registros.

Comitar somente arquivos desta tarefa. `git pull` recebe atualizações, `git push` envia commits; o usuário executa normalmente. Não há sincronização automática nem escrita em serviço externo.

## 9. Validação desta entrega

- 9 testes de dados passaram: integridade SQLite, chaves estrangeiras, quantidades, variantes confirmadas, todos os caminhos locais, hashes de todos os PDFs, hashes/crédito/licença das imagens de pinagem, existência dos textos, reconstrução por SQL, exportação determinística e ausência de dependências de rede de execução.
- Testes de interação passaram com LinkeDOM: busca com/sem resultado, filtro de família, expansão, caminhos de pinagem e PDF, comparação/diferenças/remoção, busca no glossário, modal, ferramentas, leitor e busca/paginação/limites.
- Sintaxe JavaScript verificada pelo Node.
- Pinagem G474 (12/09/2026): 10 testes de dados e o teste de interface passaram. `test_g474_pinout_versions` confere a ordem simples → completa, os PNGs e que não existam outros arquivos de pinagem da G474; o teste de interface confere as duas imagens empilhadas na aba. Números UFQFPN48 conferidos contra a tabela 12 do DS12288 e o U1 do esquema WeAct.
- Todas as prévias de pinagem foram inspecionadas como imagens locais depois do recorte: os quatro PICs com diagrama e tabela, BluePill, Uno, Nano, G474 Long, H7R3 e a BlackPill inalterada. O arquivo da BlackPill foi conferido por hash antes e depois de rodar o gerador.
- Os PDFs são snapshots técnicos, não todos as revisões mais recentes. Seu hash, data de obtenção e número de páginas estão registrados; não afirmar revisão de todas as páginas ou todas as especificações elétricas.
- Validação visual em navegador real concluída em 12/09/2026 por servidor HTTP local temporário, restrito a `127.0.0.1:8765`: tabela larga, menu aberto, ocultar coluna, restaurar e persistência após recarregar foram conferidos. O servidor foi encerrado; nenhuma porta é necessária para o uso normal por `file://`.

## 10. Próximos passos e limites concretos

1. Usuário abrir index.html, conferir tabela, expandir BlackPill/G474, visualizar pinagem e datasheet, comparar dois componentes. Registrar o resultado da revisão visual e corrigir qualquer problema encontrado.
2. BluePill: marcação C8T6 confirmada pelo usuário e qualificação de referência retirada. Falta, se o usuário quiser, um desenho específico da variante USB-C — o diagrama atual é da variante micro-USB e serve para as três porque o chip é o mesmo.
3. Confirmar as revisões Uno/Nano e quantidades PIC somente quando houver nova informação, sem impedir a consulta atual.
4. Expandir glossário conforme termos que o usuário encontrar. Para cobertura visual sobre todas as palavras do PDF original, uma etapa futura poderia usar um renderizador local com camada de texto; avaliar tamanho e compatibilidade `file://` antes de mudar a arquitetura.
5. Adicionar novas categorias apenas quando solicitado; não incluir automaticamente os semicondutores de potência do Obsidian.

Para qualquer etapa manual, seguir instruções do usuário: concluir trabalho independente primeiro, fornecer seção “Ação manual necessária”, comandos mínimos explicados e diretório, nunca pedir senha, aguardar “feito” ou saída e continuar.
