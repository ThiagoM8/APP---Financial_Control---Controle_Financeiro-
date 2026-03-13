# ⚡ PixControl

> **Domine seus gastos, um Pix de cada vez.**

O **PixControl** é um assistente financeiro inteligente integrado ao **WhatsApp**. Ele foi criado para resolver o "caos silencioso" das dezenas de transações via Pix que fazemos diariamente e que, sem o devido registro, acabam com o orçamento no fim do mês.

---

## 🎯 O Diferencial
Diferente de apps bancários complexos, o **PixControl** foca na **velocidade**. Você não abre um app; você envia uma mensagem natural como se estivesse conversando com um amigo.

> 💬 *"16 reais em doces"* — A IA cuida de todo o resto.

---

## 🛠️ Stack Tecnológica

* **🧠 Cérebro (IA):** [Google Gemini 2.0 Flash](https://aistudio.google.com/) (NLP & Inteligência de Calendário).
* **📱 Interface:** WhatsApp (via [Twilio API](https://www.twilio.com/)).
* **⚙️ Coração (Backend):** Python + Flask (Hospedado no [Render](https://render.com/)).
* **💾 Memória (DB):** [Neon PostgreSQL](https://neon.tech/) (Persistência em nuvem).
* **🕒 Relógio:** `pytz` & `datetime` para relatórios precisos no fuso horário de Brasília.

---

## ✨ Funcionalidades Principais

* ✅ **Registro Inteligente:** Extrai valor, descrição e categoria de frases naturais.
* 📅 **Consciência Temporal:** Filtra resumos por períodos (ex: *"Quanto gastei em fevereiro?"*).
* 📊 **Relatórios por Categoria:** Agrupa gastos para você saber exatamente para onde o dinheiro está indo.
* 🔄 **Menu Interativo:** Suporte a comandos rápidos para facilitar a navegação.

---

## 🚀 Como funciona o Fluxo?



1.  **Input:** O usuário envia uma mensagem no WhatsApp.
2.  **Inteligência:** O Gemini identifica se é um **gasto** ou um **pedido de resumo**.
3.  **Processamento:** O sistema aplica a lógica de datas e salva (ou busca) no **PostgreSQL (Neon)**.
4.  **Output:** O usuário recebe uma confirmação imediata ou o relatório formatado.

---

### 📝 Licença
Este projeto foi desenvolvido para fins de estudo em **Análise e Desenvolvimento de Sistemas (ADS)**.


## 📺 Demonstração em Vídeo

Aqui você pode ver o **PixControl** em ação: registrando gastos, gerando resumos e gerenciando o banco de dados em tempo real.

![Assista à demonstração](assets/PixControl.mp4)