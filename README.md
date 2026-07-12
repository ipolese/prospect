# Prospector de Sites para Codex

Plugin local para organizar um fluxo semi-automático de prospecção comercial: encontrar negócios com boa reputação e sites fracos, qualificar leads, criar novas versões das páginas, apresentá-las localmente e preparar propostas, follow-ups e contratos.

## Visão geral

O Prospector conduz o seguinte ciclo:

1. Configura preferências, assinatura e ambiente local.
2. Pesquisa negócios por nicho e cidade.
3. Qualifica os estabelecimentos pela reputação e qualidade do site atual.
4. Produz uma página redesenhada com conteúdo e identidade reais.
5. Gera editor visual e comparador antes/depois.
6. Disponibiliza a demonstração em localhost.
7. Prepara a abordagem comercial quando houver uma URL pública.
8. Acompanha respostas, follow-ups, contratos e valores no dashboard.

## Características

- Prospecção assistida pelo navegador integrado do Codex.
- Qualificação por nota, quantidade de avaliações, qualidade do site e disponibilidade de contato.
- Redesign responsivo em HTML autocontido.
- Preservação de conteúdo, fotos, logo, contatos e identidade visual do cliente.
- Editor visual para alteração de textos e imagens no navegador.
- Comparador antes/depois para revisão interna.
- Preview local sem depender de hospedagem.
- Validação estrutural de páginas, SEO básico e placeholders.
- Dashboard com SQLite para leads, contratos e financeiro.
- Preparação de propostas e follow-ups com checklist anti-spam.
- Geração de minuta HTML e contrato DOCX.
- Integração opcional com Gmail, Google Drive/Sheets e HostGator.

## Requisitos

### Obrigatórios

- Codex Desktop ou outro ambiente Codex que suporte plugins e skills.
- Python 3 para o servidor localhost e o dashboard.
- Uma pasta de trabalho com permissão de leitura e escrita.
- Navegador integrado para a prospecção e captura de conteúdo.

## Instalação pelo marketplace do GitHub

O repositório já usa o layout de marketplace do Codex. No terminal, registre o
marketplace uma única vez:

```bash
codex plugin marketplace add ipolese/prospect
```

Depois, abra o gerenciador de plugins do Codex, selecione o marketplace
`igorpolese-plugins` e instale `prospector-de-sites-codex`. O pacote do plugin
fica exclusivamente em `plugins/prospector-de-sites-codex`; não há uma segunda
cópia dos arquivos na raiz do repositório.

### Opcionais

- Conector Gmail para criar rascunhos e consultar respostas.
- Conector Google Drive/Sheets para gerar planilhas online.
- `python-docx` para geração do contrato DOCX.
- Hospedagem pública para compartilhar demonstrações com clientes.
- HostGator/cPanel, somente se esse for o provedor escolhido.

## Estrutura do plugin

```text
prospectar-codex/
├── .codex-plugin/
│   └── plugin.json
├── assets/
│   └── manual.html
├── scripts/
│   ├── servidor-sites.py
│   ├── iniciar-sites.command
│   └── iniciar-sites.bat
├── skills/
│   ├── setup/
│   ├── prospectar/
│   ├── prospeccao-maps/
│   ├── redesenhar/
│   ├── redesign-premium/
│   ├── editor/
│   ├── publicar/
│   ├── deploy-hostgator/
│   ├── proposta/
│   ├── proposta-email/
│   ├── respostas/
│   ├── followup/
│   ├── contrato/
│   ├── contrato-servico/
│   └── dashboard-leads/
└── README.md
```

Cada diretório dentro de `skills/` contém um `SKILL.md`. Algumas skills também possuem templates e scripts em `references/`.

## Instalação no Codex

### Instalação rápida pelo terminal

Clone o repositório e registre o marketplace:

```bash
git clone https://github.com/ipolese/prospect.git
cd prospect
codex plugin marketplace add ipolese/prospect
codex plugin marketplace upgrade igorpolese-plugins
codex
```

No Codex, o plugin aparece como `prospector-de-sites-codex`. A versão atual do
CLI pode não ter um comando `plugin add`; nesse caso, o marketplace é
atualizado pelo terminal e o plugin é habilitado pelo gerenciador de plugins do
Codex Desktop. O aplicativo ChatGPT e sua tela de Plugins não são o instalador
deste plugin de skills.

Para atualizar uma instalação existente:

```bash
cd /caminho/para/prospect
git pull --ff-only
codex plugin marketplace upgrade igorpolese-plugins
```

O diretório precisa ser instalado ou disponibilizado como plugin local do Codex. O manifesto principal está em:

```text
.codex-plugin/plugin.json
```

Depois de instalar ou habilitar o plugin, inicie uma nova tarefa no Codex para garantir que as skills sejam carregadas. Verifique se aparecem sugestões como:

- `$setup`
- `$prospectar`
- `$redesenhar`
- `$publicar`

O nome técnico do plugin é `prospector-de-sites-codex` e a versão atual é `1.0.0`.

### Executar o dashboard local

Depois do `$setup`, abra uma segunda aba do terminal na pasta de trabalho e
inicie o servidor administrativo:

```bash
cd /Users/ipolese/Documents/Projetos/prospector
python3 dashboard-server.py --host 127.0.0.1 --port 8765
```

Abra [http://127.0.0.1:8765](http://127.0.0.1:8765). Para o preview dos sites,
use outro terminal:

```bash
cd /Users/ipolese/Documents/Projetos/prospector
python3 servidor-sites.py --host 127.0.0.1 --port 8766
```

O dashboard roda na porta `8765`; os sites publicados localmente rodam na
porta `8766`. Pare cada servidor com `Ctrl+C`.

## Configuração inicial

Execute:

```text
$setup
```

O setup cria ou organiza os seguintes arquivos na pasta de trabalho:

```text
prospector-config.json
prospector.db
dashboard.html
dashboard-server.py
iniciar-dashboard.command ou iniciar-dashboard.bat
servidor-sites.py
iniciar-sites.command ou iniciar-sites.bat
sites/
```

O arquivo de configuração segue esta estrutura:

```json
{
  "assinatura": {
    "nome": "",
    "apresentacao": "",
    "whatsapp": ""
  },
  "prospeccao": {
    "nichos": [
      "Todos",
      "nutricionistas", "psicologos", "advogados", "psiquiatras",
      "dentistas", "dermatologistas", "fisioterapeutas", "fonoaudiologos",
      "terapeutas ocupacionais", "clinicas de estetica", "studios de pilates", "academias",
      "clinicas veterinarias", "pet shops", "saloes de beleza", "barbearias",
      "arquitetos", "designers de interiores", "contadores", "consultores financeiros",
      "imobiliarias", "escolas de idiomas", "cursos profissionalizantes", "fotografos",
      "cerimonialistas", "restaurantes", "pousadas", "oficinas mecanicas"
    ],
    "cidade": "",
    "leadsPorBusca": 10
  },
  "envio": {
    "modo": "rascunho"
  },
  "publicacao": {
    "provedor": "localhost",
    "porta": 8766,
    "host": "127.0.0.1"
  },
  "hostgator": {
    "habilitado": false,
    "usuario": "",
    "dominio": "",
    "servidor": "",
    "porta": 22,
    "chaveSsh": "",
    "pastaBase": "clientes"
  }
}
```

O bloco `hostgator` pode permanecer desabilitado e vazio durante todo o uso local.

## Fluxo de uso

### 1. Configurar

```text
$setup
```

Define assinatura, nichos, cidade, meta de leads, modo de e-mail e publicação local.

`Todos` é uma opção especial de nicho: ao selecioná-la na prospecção, o plugin percorre todos os demais nichos configurados para a cidade e consolida os leads.

### 2. Prospectar

```text
$prospectar nutricionistas em Campinas
```

O fluxo pesquisa negócios no Google Maps, visita os sites e registra:

- nome;
- nicho e cidade;
- nota e número de avaliações;
- site atual;
- telefone e WhatsApp;
- e-mail público;
- motivo objetivo da qualificação ou descarte;
- status do lead.

Os leads são persistidos em SQLite, refletidos no dashboard e mantidos em uma cópia local. Quando um conector compatível estiver disponível, também pode ser criada uma planilha online.

### 3. Redesenhar

```text
$redesenhar Nome do Cliente
```

Para cada cliente são gerados:

```text
sites/[slug]/[slug].html
sites/[slug]/[slug]-editor.html
```

O processo também cria ou atualiza:

```text
comparar.html
```

O redesign deve utilizar somente informações reais encontradas no site original, Google Maps ou outras fontes verificáveis. Serviços, credenciais, depoimentos e resultados nunca devem ser inventados.

### 4. Editar

```text
$editor Nome do Cliente
```

O editor permite:

- clicar em textos para editá-los;
- clicar em imagens para substituí-las;
- exportar um HTML limpo, sem a interface de edição.

### 5. Abrir em localhost

```text
$publicar Nome do Cliente
```

No modo padrão, a palavra “publicar” significa preparar e servir a demonstração localmente. As URLs seguem este formato:

```text
http://127.0.0.1:8766/sites/[slug]/[slug].html
http://127.0.0.1:8766/sites/[slug]/proposta.html
```

Para iniciar manualmente o servidor:

#### macOS

```bash
./iniciar-sites.command
```

#### Windows

```bat
iniciar-sites.bat
```

#### Python diretamente

```bash
python3 servidor-sites.py --host 127.0.0.1 --port 8766
```

Por padrão, o servidor escuta apenas em `127.0.0.1`, evitando exposição automática para outros dispositivos da rede.

> Uma URL `localhost` ou `127.0.0.1` só funciona no computador que está executando o servidor. Ela não deve ser enviada a um cliente externo.

### 6. Preparar proposta

```text
$proposta Nome do Cliente
```

O fluxo valida se existe uma URL pública acessível. Se a página ainda estiver somente em localhost, o plugin pode preparar uma prévia do texto, mas deve bloquear o envio do link ao cliente.

Quando uma URL pública estiver disponível, a proposta:

- usa uma primeira linha personalizada;
- menciona fatos verificáveis;
- aponta problemas do site sem ofender;
- não informa preço;
- contém somente um link principal;
- passa por uma checklist anti-spam;
- vira rascunho no Gmail quando o conector está disponível.

### 7. Verificar respostas

```text
$respostas
```

Com Gmail conectado, pesquisa respostas reais dos leads e atualiza o pipeline. Sem conector, fornece a lista de buscas necessárias sem alterar status por suposição.

### 8. Criar follow-up

```text
$followup Nome do Cliente
```

Seleciona apenas propostas sem resposta há pelo menos três dias. Cada lead recebe no máximo um follow-up automático, sempre curto e sem pressão.

### 9. Gerar contrato

```text
$contrato Nome do Cliente
```

Gera:

```text
sites/[slug]/contrato-[slug].html
sites/[slug]/contrato-[slug].docx
```

Valores, prazo, forma de pagamento, documentos e manutenção devem vir do banco ou ser confirmados pelo usuário. A minuta não substitui revisão jurídica profissional.

## Skills disponíveis

| Skill | Responsabilidade |
|---|---|
| `$setup` | Configuração inicial e atualização do ambiente |
| `$prospectar` | Orquestração da prospecção |
| `prospeccao-maps` | Critérios e procedimento de qualificação |
| `$redesenhar` | Orquestração do redesign |
| `redesign-premium` | Regras de conteúdo, design e responsividade |
| `$editor` | Geração do editor visual |
| `$publicar` | Preview localhost ou seleção do provedor |
| `deploy-hostgator` | Deploy opcional na HostGator |
| `$proposta` | Preparação e criação de rascunho |
| `proposta-email` | Estrutura e checklist anti-spam |
| `$respostas` | Consulta de respostas e atualização do pipeline |
| `$followup` | Follow-up único para leads elegíveis |
| `$contrato` | Orquestração do contrato |
| `contrato-servico` | Templates e regras contratuais |
| `dashboard-leads` | Persistência SQLite e dashboard |

As skills sem `$` na tabela são geralmente acionadas pelas skills de orquestração, mas também podem ser utilizadas diretamente quando necessário.

## Dashboard e banco de dados

O arquivo `prospector.db` é a fonte principal dos leads. O dashboard apresenta:

- pipeline em kanban;
- lista e busca de clientes;
- sites redesenhados;
- comparador antes/depois;
- propostas aguardando follow-up;
- contratos;
- valores recebidos e a receber;
- manutenção mensal recorrente.

Estados suportados:

```text
novo
redesenhado
publicado-local
publicado
proposta
respondeu
fechado
descartado
```

`publicado-local` significa que o site está pronto para revisão, mas ainda não pode ser acessado pela internet.

## Publicação pública opcional

Para compartilhar uma demonstração com o cliente, é necessário usar uma hospedagem pública com HTTPS válido. A HostGator é apenas uma das opções possíveis e somente deve ser usada quando o plano oferecer SFTP.

Para habilitá-la no config:

```json
{
  "publicacao": {
    "provedor": "hostgator"
  },
  "hostgator": {
    "habilitado": true
  }
}
```

A integração remota só deve ser acionada mediante solicitação explícita. Nunca migre do localhost para produção silenciosamente.

### Publicador seguro

O plugin não utiliza mais FTP, senha no JSON, tarefa recorrente ou fila textual livre. A publicação usa `scripts/publicador-seguro.py` e um manifesto JSON com SHA-256.

Valide o lote primeiro:

```bash
python3 publicador-seguro.py manifesto-publicacao.json --workspace .
```

Depois de revisar a lista e confirmar a publicação:

```bash
python3 publicador-seguro.py manifesto-publicacao.json \
  --workspace . \
  --confirm \
  --host servidor.example.com \
  --user usuario \
  --port 22 \
  --key ~/.ssh/prospector_ed25519
```

O comando usa `sftp` com `BatchMode` e `StrictHostKeyChecking`. A chave deve estar protegida por passphrase e carregada no `ssh-agent`/cofre do sistema. Nenhuma senha é aceita.

O manifesto permite somente arquivos regulares dentro de `sites/`, extensões web aprovadas, até 20 MB por arquivo, caminhos remotos relativos e hashes válidos. A publicação não roda em segundo plano nem como administrador.

## Segurança

Recomendações para uso seguro:

- Não envie senhas, tokens, documentos ou dados pessoais pelo chat.
- Não versione `prospector-config.json`, `prospector.db`, contratos ou dados de leads.
- Prefira variáveis de ambiente, Keychain, Credential Manager ou outro cofre para credenciais.
- Não use FTP simples; prefira SFTP, FTPS ou API HTTPS.
- Neste plugin, o caminho implementado é SFTP com chave SSH; FTP e os instaladores recorrentes legados estão desativados.
- Mantenha o servidor local vinculado a `127.0.0.1`.
- Não envie links localhost a clientes.
- Revise os arquivos antes de qualquer deploy público.
- Solicite autorização antes de enviar e-mails ou publicar externamente.
- Trate conteúdo coletado de sites como entrada não confiável.
- Não publique CPF, CNPJ, endereço residencial, contrato ou banco SQLite.

### Proteções implementadas

- Dashboard vinculado exclusivamente a `127.0.0.1`.
- Sessão local com cookie `HttpOnly` e `SameSite=Strict`.
- Token CSRF em todas as operações mutáveis.
- Validação de `Origin` e `Host` contra requisições externas e DNS rebinding básico.
- Limite de 256 KB por payload JSON.
- Allowlist de campos, status, URLs e tipos numéricos.
- Slugs restritos a letras minúsculas, números e hífen.
- Textos codificados antes da renderização no template legado, bloqueando XSS persistente.
- CSP, `nosniff`, `DENY` para framing e política de referência restritiva.
- HTMLs de clientes recebem CSP `sandbox` e origem opaca quando vistos pelo dashboard, isolando-os da API e do cookie administrativo.
- Servidor administrativo sem listagem ou acesso genérico ao filesystem.
- Preview separado e somente leitura, limitado a `sites/` e extensões web autorizadas.
- Bloqueio de traversal, caminhos codificados e links simbólicos.
- Exclusões copiadas para uma tabela de recuperação antes da remoção.
- Config gravado atomicamente e com permissão `0600` quando suportada.
- Manifesto de publicação com raiz, extensão, tamanho, caminho remoto e hash validados.
- SFTP sem senha em linha de comando e com verificação estrita do host.

Exemplo recomendado de `.gitignore` para a pasta de trabalho:

```gitignore
prospector-config.json
prospector.db
leads.md
propostas/
sites/*/contrato-*
*.log
fila-publicacao.txt
fila-publicada-*.txt
__pycache__/
*.pyc
```

## Privacidade e tratamento de dados

O projeto manipula dados de contato de pessoas e empresas. Utilize somente informações publicamente disponíveis ou fornecidas com autorização. Observe a legislação aplicável, incluindo LGPD, regras contra spam e termos de uso das plataformas consultadas.

O usuário é responsável por:

- definir uma base legal adequada para o tratamento;
- limitar a coleta ao necessário;
- manter os dados protegidos;
- atender solicitações de correção ou exclusão;
- evitar disparos em massa e abordagens enganosas.

## Solução de problemas

### O servidor local não inicia

Verifique se Python 3 está instalado:

```bash
python3 --version
```

Se a porta estiver ocupada, use outra:

```bash
python3 servidor-sites.py --port 8877
```

Atualize também `publicacao.porta` no config.

### O cliente não consegue abrir o link

Confirme se o endereço contém `localhost` ou `127.0.0.1`. Esses endereços não são públicos. Configure uma hospedagem pública antes do envio.

### O Google Maps solicita CAPTCHA ou login

Interrompa a automação e conclua manualmente a verificação no navegador. Não tente contornar CAPTCHA.

### Gmail ou Sheets não aparecem

Confirme se os conectores correspondentes estão instalados e autorizados. O fluxo local continua funcionando sem eles.

### O site antigo não aparece no comparador

Alguns sites bloqueiam iframes por `X-Frame-Options` ou CSP. Abra o site antigo em nova aba ou utilize uma captura de tela autorizada.

### O contrato DOCX não é gerado

Verifique se `python-docx` está disponível. Instale dependências somente após revisar sua procedência e, em ambientes gerenciados, após autorização.

### A página ficou sem imagens

As imagens originais podem bloquear hotlink ou mudar de URL. Baixe e armazene cópias autorizadas localmente ou atualize as referências antes de publicar.

## Desenvolvimento e validação

Ao alterar o plugin:

1. Mantenha o nome da pasta e o campo `name` do manifesto consistentes.
2. Preserve `.codex-plugin/plugin.json`.
3. Mantenha cada skill em uma pasta com `SKILL.md` válido.
4. Valide os scripts Python:

```bash
python3 -m py_compile scripts/servidor-sites.py scripts/publicador-seguro.py \
  skills/dashboard-leads/references/dashboard-server.py
python3 -m unittest discover -s tests -v
```

5. Valide o manifesto do plugin com o validador oficial do ambiente Codex.
6. Teste o fluxo em uma pasta temporária sem dados reais.
7. Verifique localhost, editor, comparador, banco e dashboard.
8. Faça teste de segurança antes de habilitar publicação externa.

Scripts operacionais adicionais:

```bash
python3 scripts/sync-dashboard.py --workspace .
python3 scripts/backup-db.py --workspace .
python3 scripts/dedupe-leads.py --workspace .
python3 scripts/validate-site.py sites/cliente/cliente.html
python3 scripts/validate-plugin-manifest.py .
python3 scripts/migrate-db.py --workspace .
python3 scripts/version-site.py sites/cliente/cliente.html --label antes-da-edicao
```

O `sync-dashboard.py` regenera o snapshot estático; `backup-db.py` verifica a integridade antes de criar backup; `dedupe-leads.py` lista possíveis duplicatas por domínio/telefone; e `validate-site.py` bloqueia placeholders, ausência de title/description/viewport e referências HTTP.
`migrate-db.py` mantém a versão do schema e `version-site.py` cria versões restauráveis antes de alterações.

## Limitações conhecidas

- Prospecção depende da disponibilidade e interface do Google Maps.
- Conectores podem não estar instalados em todos os ambientes Codex.
- Localhost não substitui hospedagem pública.
- Sites antigos podem impedir incorporação em iframe.
- Imagens remotas podem deixar de funcionar.
- A minuta contratual requer revisão jurídica conforme o caso.
- A qualidade do redesign depende da quantidade e confiabilidade das informações encontradas.

## Evoluções implementadas

Esta versão inclui a primeira rodada do roadmap técnico:

- referências de interface ajustadas para Codex;
- status `publicado-local` exibido no dashboard e comparador;
- sessão local, CSRF, validação de origem e limite de payload;
- preview isolado por CSP sandbox;
- publicação SFTP por manifesto com hash e confirmação;
- schema JSON inicial da configuração;
- backup e verificação de integridade do SQLite;
- relatório de possíveis duplicatas;
- trilha de auditoria de alterações no dashboard;
- sincronização oficial do snapshot estático;
- contratos de provedores para leads, e-mail e hospedagem;
- logging local com redaction de nomes de segredos;
- validação de title, description, viewport, canonical, Open Graph, JSON-LD, alt, placeholders e HTTP.
- dashboard JavaScript extraído para `dashboard-app.js`, com sessão/CSRF lidos por meta tag e teste HTTP do preview.
- comparador com fallback para `oldImage` quando o site antigo bloquear iframe.
- validador local do manifesto sem dependência de PyYAML.
- identidade Google Maps por `placeId`, checkpoint persistente de prospecção, estados de negociação/perda/rascunho e tarefas de follow-up.
- conectores Google por token do ambiente, consentimento/exportação/exclusão LGPD e instalador local.
- captura Playwright opcional e validação visual estrutural.

O dashboard usa delegação de eventos em `dashboard-app.js`; templates não contêm handlers inline e a CSP não usa `unsafe-inline` em scripts. Antes de operação em escala, execute os testes HTTP em ambiente que permita abrir sockets locais.

## Uso responsável

O plugin foi projetado para abordagem comercial personalizada e de baixo volume. Ele não deve ser usado para spam, coleta indiscriminada, falsificação de avaliações, invenção de credenciais ou publicação de conteúdo sem autorização.

Antes de enviar qualquer proposta:

- revise o site gerado;
- confirme todos os fatos;
- valide contatos e links;
- teste no celular e desktop;
- confirme que a URL é pública e usa HTTPS;
- revise o destinatário e o texto do e-mail.

## Licença e autoria

Autor informado no manifesto: **Igor Polese**.

O manifesto atual não declara uma licença. Antes de distribuir ou publicar o plugin, defina uma licença compatível com os direitos sobre o projeto original, templates e demais recursos incluídos.
