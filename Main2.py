import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os

def is_ngrs_file(filepath):
    """Dosyanın .ngrs ile bitip bitmediğini kontrol eder."""
    return filepath.lower().endswith('.ngrs')

def read_file_in_hex(filepath):
    """Dosyayı açar ve içeriğini hex formatında döner."""
    with open(filepath, 'r') as file:
        content = file.read()
    return content

def hex_to_image(hex_content, width=125, height=125):
    """Hex kodunu bir görüntüye dönüştürür."""
    # Hex string'ini byte'lara dönüştür
    img_data = bytes.fromhex(hex_content)
    
    # Görüntü oluşturma
    image = Image.frombytes('RGB', (width, height), img_data)
    
    return image

def display_image(image):
    """Hex kodunu dönüştürdüğümüz görüntüyü yeni bir pencerede gösterir."""
    new_window = tk.Toplevel(root)
    new_window.title("Görüntü")

    img = ImageTk.PhotoImage(image)
    panel = tk.Label(new_window, image=img)
    panel.image = img  # Image'nin garbage collector tarafından silinmesini önlemek için referans tutuyoruz
    panel.pack()

def open_ngrs_file():
    """NGRS dosyası seçilir ve hex kodu resme dönüştürülerek gösterilir."""
    filepath = filedialog.askopenfilename(
        title="Bir .ngrs dosyası seçin",
        filetypes=[("NGRS Dosyaları", "*.ngrs"), ("Tüm Dosyalar", "*.*")]
    )
    
    if filepath:
        if is_ngrs_file(filepath):
            hex_content = read_file_in_hex(filepath)
            try:
                image = hex_to_image(hex_content)
                display_image(image)
            except Exception as e:
                messagebox.showerror("Hata", f"Görüntü oluşturulamadı: {e}")
        else:
            messagebox.showerror("Hata", "Lütfen .ngrs uzantılı bir dosya seçin.")

def save_png_as_ngrs():
    """PNG dosyasını seçip onu 125x125 boyutunda .ngrs dosyasına çevirir."""
    filepath = filedialog.askopenfilename(
        title="Bir PNG dosyası seçin",
        filetypes=[("PNG Dosyaları", "*.png"), ("Tüm Dosyalar", "*.*")]
    )
    
    if filepath:
        # PNG dosyasını açma ve yeniden boyutlandırma
        image = Image.open(filepath).convert('RGB')
        resized_image = image.resize((125, 125))
        
        # Görüntüyü byte'lara dönüştürme
        img_data = resized_image.tobytes()
        hex_content = img_data.hex()
        
        # Hex içeriğini .ngrs dosyasına kaydetme
        ngrs_filepath = filedialog.asksaveasfilename(
            title="NGRS dosyası olarak kaydet",
            defaultextension=".ngrs",
            filetypes=[("NGRS Dosyaları", "*.ngrs")]
        )
        
        if ngrs_filepath:
            with open(ngrs_filepath, 'w') as ngrs_file:
                ngrs_file.write(hex_content)
            messagebox.showinfo("Başarılı", "PNG dosyası başarıyla 125x125 boyutunda .ngrs dosyasına çevrildi!")

# Ana uygulama penceresi
root = tk.Tk()
root.title("NGRS Dosya İşleme")
root.geometry("300x200")

# NGRS dosyası seçme düğmesi
select_button = tk.Button(root, text="NGRS Dosyası Seç", command=open_ngrs_file)
select_button.pack(pady=10)

# PNG dosyasını NGRS formatına çevirme düğmesi
convert_button = tk.Button(root, text="PNG'yi NGRS'ye Çevir", command=save_png_as_ngrs)
convert_button.pack(pady=10)

# Uygulamayı başlat
root.mainloop()


