# b2bflow — Desafio em Python

Lê contatos do **Supabase** e envia mensagem personalizada via **Z-API** (WhatsApp).

## 1. Setup da tabela no Supabase

No **SQL Editor** do projeto:

```sql
CREATE TABLE contacts (
    id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name  TEXT NOT NULL,
    phone TEXT NOT NULL
);

INSERT INTO contacts (name, phone) VALUES ('Seu Nome', '5511999990001');

ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow anon select" ON contacts FOR SELECT TO anon USING (true);
```

> Formato do telefone: DDI + DDD + número, sem `+`. Ex: `5511999990001`

## 2. Variáveis de ambiente

```bash
cp .env.example .env
```

| Variável            | Onde encontrar                                               |
|---------------------|---------------------------------------------------------     |
| `SUPABASE_URL`      | Settings → General → Project ID → `https://<id>.supabase.co` |
| `SUPABASE_KEY`      | Settings → API Keys → Publishable key                        |
| `ZAPI_INSTANCE_ID`  | Z-API → instância → ID da instância                          |
| `ZAPI_TOKEN`        | Z-API → instância → Token da instância                       |
| `ZAPI_CLIENT_TOKEN` | Z-API → Security → Token de segurança da conta               |

- Obs: Apontar a câmera do celular no QRCode do Z-API para conectar a instância e enviar mensagens via API.

## 3. Como rodar

```bash
python main.py
```

## Demo
Um vídeo rodando o código e funcionando: 
- https://youtu.be/qjhsQrxn2bU
