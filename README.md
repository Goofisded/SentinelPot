# 🛡️ Interactive Honeypot with Discord Alerts

An advanced Python-based honeypot that logs suspicious activity and sends real-time alerts to a Discord webhook with a visually appealing embed.

---

## 🚀 Features
- **Detects unauthorized access attempts**
- **Logs attacker activity and commands**
- **Sends real-time alerts to a Discord webhook**
- **User-friendly CLI output with color formatting**
- **Prevents Discord API rate limit issues**
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
socketserver
logging
requests
datetime
json
colorama
```

---

## ⚙️ Setup & Usage

1️⃣ **Clone the repository:**
```bash
git clone https://github.com/yourusername/honeypot.git
cd honeypot
```

2️⃣ **Install dependencies:**
```bash
pip install -r requirements.txt
```

3️⃣ **Configure Discord Webhook:**
- Open `config.py` (or inside `honeypot.py`) and replace `DISCORD_WEBHOOK_URL` with your own webhook.

4️⃣ **Run the honeypot:**
```bash
python honeypot.py
```

5️⃣ **Simulate an attack:** (Run this from another machine)
```bash
nc -v <your-public-ip> 2222
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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

For issues or suggestions, open an issue on GitHub or contact me via Discord.

Happy hunting! 🕵️‍♂️
