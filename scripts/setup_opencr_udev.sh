#!/bin/bash
# ==============================================================================
# BRONE OS SETUP: OPENCR UDEV PERMISSIONS AUTOMATION (REVERSIBLE)
# ==============================================================================
# Fungsi:
# Memberikan izin akses non-root ke perangkat OpenCR 1.0 (STMicroelectronics)
# sehingga Terminal 1 (op3_manager) TIDAK PERLU 'sudo bash' lagi.
#
# Penggunaan:
#   bash setup_opencr_udev.sh --install     # Pasang aturan udev (Aman)
#   bash setup_opencr_udev.sh --uninstall   # Hapus aturan & kembalikan ke awal
#   bash setup_opencr_udev.sh --status      # Cek status izin saat ini
# ==============================================================================

RULE_FILE="/etc/udev/rules.d/99-opencr.rules"

function show_help() {
    echo "Penggunaan: bash setup_opencr_udev.sh [OPSI]"
    echo "  --install     Pasang udev rule agar op3_manager bisa jalan tanpa sudo"
    echo "  --uninstall   Hapus udev rule dan kembalikan sistem seperti semula"
    echo "  --status      Periksa apakah aturan udev aktif"
}

function check_status() {
    echo "[INFO] Memeriksa status izin OpenCR..."
    if [ -f "$RULE_FILE" ]; then
        echo "✅ Rule udev TERPASANG di $RULE_FILE"
        cat "$RULE_FILE"
    else
        echo "⚠️ Rule udev BELUM terpasang (Terminal 1 masih butuh sudo bash)."
    fi
    echo ""
    echo "[INFO] Status port serial /dev/ttyUSB* saat ini:"
    ls -l /dev/ttyUSB* 2>/dev/null || echo "Tidak ada perangkat /dev/ttyUSB* yang tertancap saat ini."
}

function install_rule() {
    echo "[INFO] Memasang udev rule untuk OpenCR 1.0 (Vendor: 0483)..."
    
    # Menulis konfigurasi udev: izinkan mode 0666 untuk vendor STMicroelectronics (OpenCR)
    echo '# OpenCR 1.0 USB Serial Rule (BRONE System OS Architecture)' | sudo tee "$RULE_FILE" > /dev/null
    echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", MODE="0666", GROUP="dialout"' | sudo tee -a "$RULE_FILE" > /dev/null
    
    # Reload udev daemon
    echo "[INFO] Me-reload daemon udev..."
    sudo udevadm control --reload-rules
    sudo udevadm trigger
    
    # Menambahkan user saat ini ke group dialout
    sudo usermod -a -G dialout "$USER"
    
    echo "✅ SUKSES: Udev rule berhasil dipasang!"
    echo "👉 Sekarang Terminal 1 (op3_manager) bisa dijalankan langsung TANPA 'sudo bash'!"
}

function uninstall_rule() {
    echo "[INFO] Menghapus udev rule OpenCR..."
    if [ -f "$RULE_FILE" ]; then
        sudo rm "$RULE_FILE"
        sudo udevadm control --reload-rules
        sudo udevadm trigger
        echo "✅ SUKSES: Konfigurasi dikembalikan 100% ke kondisi awal (default OS)."
    else
        echo "[INFO] File $RULE_FILE memang tidak ada. Sistem sudah bersih."
    fi
}

case "$1" in
    --install)
        install_rule
        ;;
    --uninstall)
        uninstall_rule
        ;;
    --status)
        check_status
        ;;
    *)
        show_help
        ;;
esac
