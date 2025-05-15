import subprocess
import time
import os
import logging

# 🔧 Ρύθμιση logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

SETUP_EXE = "setup.exe"
FIREWALL_RULE_NAME = "BlockSetupExe"

# 🔐 Προσθήκη κανόνα στο firewall
def block_setup_exe():
    exe_path = os.path.abspath(SETUP_EXE)
    cmd = [
        "netsh", "advfirewall", "firewall", "add", "rule",
        f"name={FIREWALL_RULE_NAME}",
        "dir=out", "action=block", f"program={exe_path}",
        "enable=yes"
    ]
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        logging.info("🔒 Προστέθηκε κανόνας firewall για μπλοκάρισμα του setup.exe.")
        return True
    else:
        if "An object with the same key already exists" in result.stderr:
            logging.info("ℹ Ο κανόνας firewall υπάρχει ήδη.")
            return True
        logging.error("❌ Αποτυχία δημιουργίας κανόνα firewall.")
        logging.error(result.stderr.strip())
        return False

# 🔓 Αφαίρεση κανόνα firewall
def unblock_setup_exe():
    cmd = [
        "netsh", "advfirewall", "firewall", "delete", "rule",
        f"name={FIREWALL_RULE_NAME}"
    ]
    subprocess.run(cmd, shell=True)
    logging.info("✅ Ο κανόνας firewall αφαιρέθηκε.")

# ▶ Εκκίνηση setup.exe
def run_setup_and_wait():
    exe_path = os.path.abspath(SETUP_EXE)
    try:
        process = subprocess.Popen([exe_path])
        logging.info("🚀 Ξεκίνησε το setup.exe...")
        while process.poll() is None:
            time.sleep(1)
        logging.info("📦 Το setup.exe έκλεισε.")
    except Exception as e:
        logging.error(f"⚠ Σφάλμα κατά την εκκίνηση του setup.exe: {e}")

# 🔁 Κύρια ροή
if __name__ == "__main__":
    print("\n==========================================")
    print("🔧 Script: Internet Blocker for AutoCAD.exe")
    print("👨‍💻 Developer: G.T. (Giannis Tsimpouris)")
    print("🗓 Version: 1.1 - 2025")
    print("==========================================\n")

    exe_path = os.path.abspath(SETUP_EXE)

    if block_setup_exe():
        if os.path.exists(exe_path):
            run_setup_and_wait()
        else:
            logging.error(f"❌ Το αρχείο δεν βρέθηκε: {exe_path}")
        unblock_setup_exe()
    else:
        logging.error("⛔ Δεν μπόρεσε να δημιουργηθεί ο κανόνας firewall. Τίποτα δεν θα εκτελεστεί.")
