---
name: deploy-hostgator
description: Publicar páginas opcionalmente em hospedagem compatível com SFTP, com manifesto validado, chave SSH e confirmação explícita. Usar somente quando o usuário pedir publicação pública ou HostGator e o provedor oferecer SFTP.
---

# Deploy remoto seguro

O fluxo padrão permanece localhost. Publicação remota é opcional, executada sob demanda e exige autorização explícita.

## Requisitos

- SFTP/SSH com verificação estrita da chave do servidor.
- Chave do usuário protegida pelo Keychain, Credential Manager, ssh-agent ou passphrase.
- Nenhuma senha em `prospector-config.json`, argumentos, logs ou chat.
- HTTPS válido no domínio final.

FTP simples e FTPS sem validação de certificado são proibidos.

## Manifesto

Criar `manifesto-publicacao.json` com versão 1, `jobId` aleatório e até 200 arquivos. Cada item contém `origem`, `destino` e SHA-256. Origens devem ser arquivos regulares dentro de `sites/`; destinos não podem ser absolutos nem conter `..`.

```json
{
  "version": 1,
  "jobId": "job-12345678",
  "arquivos": [
    {
      "origem": "sites/cliente/cliente.html",
      "destino": "public_html/clientes/cliente/index.html",
      "sha256": "HASH_DE_64_CARACTERES"
    }
  ]
}
```

## Procedimento

1. Copiar `scripts/publicador-seguro.py` para a pasta de trabalho.
2. Validar sem publicar: `python3 publicador-seguro.py manifesto-publicacao.json --workspace .`.
3. Mostrar a lista validada ao usuário e obter confirmação.
4. Publicar com `--confirm --host HOST --user USUARIO --port 22 --key CAMINHO_DA_CHAVE`.
5. O script usa `sftp -oBatchMode=yes -oStrictHostKeyChecking=yes`; não aceita senha.
6. Verificar página e capa por HTTPS antes de marcar o lead como `publicado`.

Os instaladores recorrentes e publicadores FTP presentes em versões antigas estão desativados e não devem ser reativados.
