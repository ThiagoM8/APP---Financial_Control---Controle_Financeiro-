# ⚡ PixControl

> **Master your expenses, one Pix at a time.**

**PixControl** is an intelligent financial assistant integrated with **WhatsApp**. It was created to solve the "silent chaos" of dozens of daily Pix transactions that, without proper tracking, end up ruining the monthly budget.

---

## 🎯 The Difference
Unlike complex banking apps, **PixControl** focuses on **speed**. You don't open an app; you send a natural message as if you were talking to a friend.

> 💬 *"Spent 16 on sweets"* — The AI handles everything else.

---

## 🛠️ Tech Stack

* **🧠 Brain (AI):** [Google Gemini 2.0 Flash](https://aistudio.google.com/) (NLP & Calendar Intelligence).
* **📱 Interface:** WhatsApp (via [Twilio API](https://www.twilio.com/)).
* **⚙️ Core (Backend):** Python + Flask (Hosted on [Render](https://render.com/)).
* **💾 Memory (DB):** [Neon PostgreSQL](https://neon.tech/) (Cloud persistence).
* **🕒 Clock:** `pytz` & `datetime` for accurate reports in Brasília Timezone (UTC-3).

---

## ✨ Key Features

* ✅ **Smart Logging:** Extracts value, description, and category from natural language.
* 📅 **Time Awareness:** Filters summaries by period (e.g., *"How much did I spend in February?"*).
* 📊 **Category Reports:** Groups expenses so you know exactly where your money is going.
* 🔄 **Interactive Menu:** Support for quick commands to make navigation easier.

---

## 🚀 How it Works



1.  **Input:** User sends a message on WhatsApp.
2.  **Intelligence:** Gemini identifies if it's an **expense** or a **summary request**.
3.  **Processing:** The system applies date logic and saves (or fetches) data from **PostgreSQL (Neon)**.
4.  **Output:** The user receives an immediate confirmation or the formatted report.

---

### 📝 License
This project was developed for study purposes in **Analysis and Systems Development (ADS)**.


## 📺 Video Demo

Here you can see **PixControl** in action: logging expenses, generating summaries, and managing the database in real-time.

![Assista à demonstração](assets/PixControl.mp4)