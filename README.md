# 🛡️ Interactive Honeypot with Discord Alerts

An advanced Python-based honeypot that logs suspicious activity and sends real-time alerts to a Discord webhook with a visually appealing embed.

---

## 🚀 Features
- **Detects unauthorized access attempts**
- **Logs attacker activity and commands**
- **Sends real-time alerts to a Discord webhook**
- **Customizable listening ports & interface**

---

## 📜 Requirements
Ensure you have Python installed, then install dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies
The required dependencies are listed in `requirements.txt`:

```
requests
colorama

```

---

## ⚙️ Setup & Usage

1️⃣ **Clone the repository:**
```bash
git clone https://github.com/Goofisded/SentinelPot.git
cd SentinelPot
```

2️⃣ **Install dependencies:**
```bash
pip install -r requirements.txt
```

3️⃣ **Configure Discord Webhook:**
- Open `SentinelPot.py` and replace `WEBHOOK_URL` with your own webhook.

4️⃣ **Run the honeypot:**
```bash
python SentinelPot.py
```

5️⃣ **Simulate an attack:** (Run this from another machine)
```bash
nc -v <ip> 2222
```

---

## 🛠️ Contributing

Want to improve the project? Follow these steps:

1. **Fork the repository**
2. **Create a new branch:** `git checkout -b feature-name`
3. **Commit changes:** `git commit -m "Added a new feature"`
4. **Push to your branch:** `git push origin feature-name`
5. **Submit a Pull Request**

---

## 📝 License

This project is licensed under the MIT License.

---

## 📧 Contact

For issues or suggestions, open an issue on GitHub or contact me via Discord: `goofisdead`.

Happy hunting! 🕵️‍♂️
