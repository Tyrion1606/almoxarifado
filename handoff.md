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
| `assets/pinouts/*.png` | 10 prévias renderizadas de páginas oficiais |
| `docs/evidence/blackpill-variant.png` | Print fornecido pelo usuário da variante adquirida |
| `docs/SOURCES.md` | Proveniência, créditos e versões documentais |
| `scripts/export.py` | Atualiza e confere catálogo JS e dump SQL |
| `scripts/seed.py` | Restaura banco ausente a partir do dump; recusa sobrescrita |
| `scripts/download_sources.py` | Lista explícita de downloads públicos; uso de manutenção |
| `scripts/prepare_documents.py` | Extração textual e prévias das placas usando Poppler |
| `scripts/prepare_pinouts.py` | Prévias das páginas de pinagem dos chips |
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
| BluePill | 3 | Família STM32 informada; ficha de referência F103C8T6, ainda sem confirmação documental da marcação exata das três unidades |
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

A busca local pela BluePill encontrou uma conversa citada como “Branch · Software para programar Bluepill”, mas o texto consolidado correspondente descreve BlackPill F411. O link compartilhado não retornou o conteúdo pelo leitor web. Não confundir nome da conversa com prova de MCU, nem importar a identificação de um módulo ADS1256 + F103 de outro projeto como se fosse a BluePill. A ficha C8 é explícita como referência; manter essa distinção até evidência melhor.

## 6. Notas técnicas a preservar

- Memória PIC deve conservar **palavras × 14 bits**. KiB é uma equivalência de capacidade, não garante que toolchains tratem programa como bytes comuns.
- SRAM em bytes no banco; interface converte para KiB (kibibytes, 1.024 bytes). MiB = 1.048.576 bytes. Anúncios frequentemente usam KB/MB para capacidades binárias.
- BlackPill: 512 KiB internos, 128 KiB SRAM, 8 MiB de Flash SPI externa conforme confirmação do usuário. F411 não tem DAC nem CAN. O clock máximo é 100 MHz; 96 MHz é configuração do TCC, 25 MHz é cristal externo.
- Flash externa montada não prova que o logger esteja implementado no firmware do TCC. Não mudar essa afirmação sem revisar o firmware.
- G474CEU6: 512 KiB Flash; SRAM 96 + 32 KiB CCM. Long é formato físico; não implica mais pinos que a versão compacta CEU6. O diagrama incluído é QFN48 Long, não QFP48 nem compacto.
- H7R3: 64 KiB de Flash interna podem hospedar boot e/ou código; não tratar como zero Flash nem como 8 MB internos. A placa WeAct adiciona 8 MB externos. H7R3 **não possui DAC**; fonte usada DS14360 Rev 3. Possui Cortex-M7 com FPU de dupla precisão. Não importar recursos gráficos de H7R7 indiscriminadamente para H7R3.
- GPIO, ADC, DAC e interfaces da família não equivalem automaticamente a sinais expostos na placa nem disponíveis simultaneamente. Verificar encapsulamento e funções alternativas.
- PIC12: GP3/RA3 somente entrada. PIC16F887: RE3 somente entrada. PIC12F675 não tem PWM de hardware. PIC12F1501 usa HEF, não EEPROM clássica.
- PIC ICSP e conector ICSP AVR têm protocolos/sinais diferentes. PICkit 3 não é programador AVR genérico.
- CH343P é ponte USB–UART, não depurador SWD. Níveis elétricos do módulo precisam ser conferidos quando for conectar.
- ST-Link V2: não prometer H7RS sem conferir versão do software, firmware e suporte do gravador. Nenhuma gravação física foi feita.

## 7. Interface e documentação interativa

`app.js` renderiza as linhas a partir do catálogo, usando escape de conteúdo. Delegação de eventos mantém as ações disponíveis após rerender. A seleção de comparação está num Set em memória. Tabela ordena por nome ou clock; filtros por família e tipo; busca percorre os campos do item.

Cada linha abre uma seção com abas: especificações, pinagem, datasheet comentado e original. Abas respondem às setas, Home e End. Ajuda rápida aparece por hover/foco; clique abre um dialog nativo que oferece fechamento e Escape. Termos também podem ser acessados por toque. Layout possui adaptações até telas estreitas e rolagem horizontal da tabela.

**Datasheet comentado:** arquivo JS por PDF, carregado sob demanda por tag script clássica (compatível com `file://`). Contém páginas de texto extraídas por `pdftotext -layout`, navegação e busca circular por página. Um reconhecedor insensível a maiúsculas transforma os 91 termos cadastrados em botões. Não é um tradutor, modelo de linguagem nem glossário de todas as palavras dos PDFs. Subsímbolos como VDD com formatação especial ou texto dentro de desenhos podem não casar com o reconhecedor.

**Documento original:** objeto PDF local com link alternativo. Diagramação e desenhos do fabricante são preservados. O visualizador nativo de PDF não recebe os tooltips do aplicativo; estes ficam na leitura comentada e nas fichas. Comportamento do visualizador varia conforme navegador. Não prometer anotação visual sobre cada palavra do PDF original.

**Pinagem:** imagens renderizadas de páginas oficiais, sem desenho inventado ou arte gerada por IA. As páginas dos chips contêm encapsulamentos alternativos; observar o rótulo da ficha. BluePill exibe pinagem do chip LQFP48 (figura superior), não dos conectores de uma placa verificada. Documentos completos de pinagem ficam acessíveis para consultar outras vistas/páginas. O diagrama da BlackPill é o WeAct v2.0+, contém anotações de família: o datasheet F411 prevalece para recursos do chip.

## 8. Manutenção

Executar na raiz do clone. Uso normal só precisa do navegador. Manutenção do banco requer Python 3 com sqlite3 (biblioteca padrão). Extração/renderização adicional requer Poppler; testes DOM requerem Node.js moderno. Nenhuma dependência é instalada ao abrir o site.

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

# Extrai as páginas e renderiza as prévias das placas; requer Poppler instalado.
python3 scripts/prepare_documents.py

# Renderiza as páginas de pinagem dos chips; requer Poppler.
python3 scripts/prepare_pinouts.py

# Inclui a proveniência atualizada no snapshot do catálogo.
python3 scripts/export.py
```

O script de download não atualiza silenciosamente um PDF existente. Para mudar revisão, preservar o anterior até validar o substituto, alterar a lista explicitamente, conferir contagem/pinagens e atualizar docs/SOURCES.md. Hashes são SHA-256 (resumo criptográfico do conteúdo), úteis para detectar alteração dos arquivos.

### Git e conflitos de banco

Banco binário não deve ser mesclado automaticamente. Rever as alterações SQL dos dois lados, resolver a intenção das mudanças, aplicar numa cópia validada e gerar os snapshots novamente. Não executar o dump de uma versão por cima de um banco existente. O teste de roundtrip já verifica que a versão SQL atual reconstrói os mesmos registros.

Comitar somente arquivos desta tarefa. `git pull` recebe atualizações, `git push` envia commits; o usuário executa normalmente. Não há sincronização automática nem escrita em serviço externo.

## 9. Validação desta entrega

- 8 testes de dados passaram: integridade SQLite, chaves estrangeiras, quantidades, variantes confirmadas, todos os caminhos locais, hashes de todos os PDFs, existência dos textos, reconstrução por SQL, exportação determinística e ausência de dependências de rede de execução.
- Testes de interação passaram com LinkeDOM: busca com/sem resultado, filtro de família, expansão, caminhos de pinagem e PDF, comparação/diferenças/remoção, busca no glossário, modal, ferramentas, leitor e busca/paginação/limites.
- Sintaxe JavaScript verificada pelo Node.
- Prévias de pinagem foram inspecionadas como imagens locais, incluindo PICs, F103, Uno, Nano, BlackPill, G474 Long e H7R3.
- Os PDFs são snapshots técnicos, não todos as revisões mais recentes. Seu hash, data de obtenção e número de páginas estão registrados; não afirmar revisão de todas as páginas ou todas as especificações elétricas.
- **Validação visual de navegador pendente:** Chrome recusou `file:///home/davi/repos/almoxarifado/index.html` pela política da ferramenta de navegação. Nenhuma tentativa de contorno foi feita. Não houve teste visual em navegador real, responsividade renderizada nem interação real com o visualizador PDF. LinkeDOM testa estrutura e lógica, não layout nem comportamento nativo do navegador.
- Um teste inicial de servidor local foi impedido pela restrição de sockets da sandbox. Nenhum servidor ficou rodando; nenhuma porta é necessária para o uso final.

## 10. Próximos passos e limites concretos

1. Usuário abrir index.html, conferir tabela, expandir BlackPill/G474, visualizar pinagem e datasheet, comparar dois componentes. Registrar o resultado da revisão visual e corrigir qualquer problema encontrado.
2. Recuperar/confirmar o código físico das BluePill sem confundir o histórico da BlackPill; se for C8 confirmado, retirar a qualificação de referência e adicionar mapa de conectores da revisão correta.
3. Confirmar as revisões Uno/Nano e quantidades PIC somente quando houver nova informação, sem impedir a consulta atual.
4. Expandir glossário conforme termos que o usuário encontrar. Para cobertura visual sobre todas as palavras do PDF original, uma etapa futura poderia usar um renderizador local com camada de texto; avaliar tamanho e compatibilidade `file://` antes de mudar a arquitetura.
5. Adicionar novas categorias apenas quando solicitado; não incluir automaticamente os semicondutores de potência do Obsidian.

Para qualquer etapa manual, seguir instruções do usuário: concluir trabalho independente primeiro, fornecer seção “Ação manual necessária”, comandos mínimos explicados e diretório, nunca pedir senha, aguardar “feito” ou saída e continuar.
