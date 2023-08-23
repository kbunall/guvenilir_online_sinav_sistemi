#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# os ve sys modüllerini içe aktarır
import os
import sys

# main() adında bir fonksiyon tanımlar
def main():
    # DJANGO_SETTINGS_MODULE çevresel değişkenini 'onlinexam.settings' olarak ayarlar
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinexam.settings')
    
    try:
        # Django'nun execute_from_command_line fonksiyonunu içe aktarır
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Django'yı içe aktarırken hata alınırsa, uygun hata mesajını oluşturur ve yükseltir
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # sys.argv üzerinden komut satırı argümanlarını alarak Django'nun yönetim komutlarını yürütür
    execute_from_command_line(sys.argv)

# Eğer bu betik dosyası doğrudan çalıştırılıyorsa (diğer bir dosyadan içe aktarılmadıysa), main() fonksiyonunu çağırır
if __name__ == '__main__':
    main()
