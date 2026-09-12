# ▦ Almoxarifado

**Conheça o que você tem. Escolha o que seu projeto precisa.**

Seu acervo de microcontroladores, com comparação lado a lado, mapas de pinagem e documentação de bancada. Local, sem conta e sem instalação.

## Abrir

Clone este repositório e abra **[index.html](index.html)** no navegador. É só isso — não precisa iniciar servidor, instalar pacotes ou criar banco.

Para receber melhorias, execute `git pull` na pasta do projeto e recarregue a página.

## Na bancada

- **10 modelos e 19 unidades:** quatro PICs, Uno, Nano, BluePill, BlackPill e as novas WeAct G474 Long e H7R3. As 10 unidades PIC são estimativas do Obsidian.
- **Compare:** marque os componentes na tabela; as diferenças aparecem destacadas.
- **Explore:** expanda uma linha para ver especificações, aplicação, pinagem e datasheet.
- **Entenda:** 91 termos com explicação rápida ao passar o cursor e documentação completa ao clicar. Funciona também por teclado e toque.
- **Consulte offline:** documentos originais e leitura comentada incluídos no repositório. Links para as fontes são opcionais e precisam de internet.
- **Conecte:** fichas do CH343P, ST-Link V2 e PICkit 3.

A BlackPill cadastrada é a **WeAct STM32F411CEU6, cristal de 25 MHz e Flash externa de 8 MB**, usada no TCC (Trabalho de Conclusão de Curso). A BluePill usa a ficha de referência STM32F103C8T6; a marcação exata das três unidades ainda não foi recuperada nos registros. Uno e Nano usam as referências clássicas ATmega328P.

## Como os dados ficam guardados

O **SQLite** é um banco de dados em um único arquivo: [data/inventory.sqlite](data/inventory.sqlite). A página lê uma cópia gerada desse banco, permitindo abrir diretamente pelo arquivo, sem servidor. Banco, cópia de leitura e documentos são versionados juntos.

As alterações permanentes são feitas no projeto e compartilhadas por `commit`, `push` e `pull` — registrar, enviar e receber versões no Git. A seleção para comparar é temporária; a página não grava no banco.

A leitura comentada destaca os **termos cadastrados**; ela não traduz automaticamente todo o documento. Para desenhos, tabelas complexas e limites elétricos completos, use a aba do documento original.

## Continuar o desenvolvimento

Peça ao próximo agente: **“Leia o handoff.md antes de alterar o projeto.”**

O [handoff.md](handoff.md) registra arquitetura, fontes, decisões, testes, manutenção e pendências. Créditos dos documentos: [docs/SOURCES.md](docs/SOURCES.md).
