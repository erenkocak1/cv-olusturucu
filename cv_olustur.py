import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, Toplevel
import json
from fpdf import FPDF
import os
import sys

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

DATA_FILE = "cv_data.json"
ICON_NAME = "cv.ico" 

def resource_path(relative_path):
    """ EXE olunca dosyaları bulmak için gerekli yol fonksiyonu """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CV Oluşturucu - Profesyonel Editör")
        self.root.geometry("1150x850")
        
        try:
            self.root.iconbitmap(resource_path(ICON_NAME))
        except:
            pass

        self.data = {
            "name": "", "title": "", "phone": "", "email": "", 
            "linkedin": {"title": "", "url": ""}, 
            "blog": {"title": "", "url": ""}, 
            "about": "", "photo_path": "",
            "education": [], "skills": [], "certificates": [], "projects": []
        }

        self.load_data()
        self.create_widgets()
        self.setup_context_menu()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        right_panel = ttk.Frame(main_frame, padding=30, bootstyle="secondary")
        right_panel.pack(side="right", fill="y")

        ttk.Label(right_panel, text="PROGRAM HAKKINDA", font=("Arial", 16, "bold"), bootstyle="inverse-secondary").pack(pady=(0, 20), anchor="w")
        
        info_text = """
🎯 PROGRAMIN AMACI:
CV'nizi her güncellemede sıfırdan yazma
derdini ortadan kaldırın! 

Bu program verilerinizi hafızada tutar.
Böylece sadece yeni eklenen eğitimi
veya tecrübeyi güncelleyerek,
önceki verilerin üzerine işlem yapıp
saniyeler içinde yeni PDF alabilirsiniz.

✨ ÖNE ÇIKAN ÖZELLİKLER:
• Fotoğraf Ekleme Desteği
• Tıklanabilir Linkler (LinkedIn / Web)
• Türkçe Karakter Uyumlu PDF
• Sade ve Profesyonel Tasarım

📝 METİN BİÇİMLENDİRME:
"Hakkımda" kutusunda yazılarınızı
özelleştirebilirsiniz:

1. Yazıyı fare ile seçin.
2. Üstteki butonları kullanın:
   [ B ] -> Kalın (Bold)
   [ I ] -> İtalik (Italic)
   [ ⬅ ↔ ➡ ] -> Metin Hizalama

⚠️ DİKKAT:
Yazı içinde oluşan <b>, <i> gibi
etiketleri silmeyin. Onlar PDF
çıktısında stili sağlar.
        """
        ttk.Label(right_panel, text=info_text, font=("Arial", 12), justify="left", bootstyle="inverse-secondary").pack(anchor="w")
        
        ttk.Label(right_panel, text="Geliştiriciler:\nYusuf Eren KOÇAK", font=("Arial", 9, "italic"), bootstyle="inverse-secondary").pack(side="bottom", anchor="w", pady=10)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, padding=20)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        style = ttk.Style()
        bg = style.lookup('TFrame', 'background')
        canvas.configure(yscrollcommand=scrollbar.set, bg=bg, highlightthickness=0)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)


        img_frame = ttk.Labelframe(self.scrollable_frame, text="Profil Fotoğrafı", bootstyle="info", padding=10)
        img_frame.pack(fill="x", pady=10)
        ttk.Button(img_frame, text="Fotoğraf Seç", command=self.select_photo, bootstyle="outline-info").pack(side="left", padx=5)
        current_photo = self.data.get("photo_path", "")
        self.lbl_photo = ttk.Label(img_frame, text=os.path.basename(current_photo) if current_photo else "Fotoğraf Yok")
        self.lbl_photo.pack(side="left", padx=5)

        info_frame = ttk.Labelframe(self.scrollable_frame, text="Kişisel Bilgiler", bootstyle="primary", padding=10)
        info_frame.pack(fill="x", pady=10)
        self.entry_name = self.create_input(info_frame, "Ad Soyad:", self.data.get("name", ""))
        self.entry_title = self.create_input(info_frame, "Ünvan:", self.data.get("title", ""))
        self.entry_phone = self.create_input(info_frame, "Telefon:", self.data.get("phone", ""))
        self.entry_email = self.create_input(info_frame, "Email:", self.data.get("email", ""))

        link_frame = ttk.Labelframe(self.scrollable_frame, text="Bağlantılar", bootstyle="info", padding=10)
        link_frame.pack(fill="x", pady=10)
        
        lk_sub = ttk.Frame(link_frame)
        lk_sub.pack(fill="x", pady=5)
        ttk.Label(lk_sub, text="LinkedIn Başlık:", width=15).pack(side="left")
        self.entry_lk_title = ttk.Entry(lk_sub)
        self.entry_lk_title.pack(side="left", expand=True, fill="x", padx=(0,5))
        self.entry_lk_title.insert(0, self.data["linkedin"].get("title", ""))
        ttk.Label(lk_sub, text="URL:", width=5).pack(side="left")
        self.entry_lk_url = ttk.Entry(lk_sub)
        self.entry_lk_url.pack(side="left", expand=True, fill="x")
        self.entry_lk_url.insert(0, self.data["linkedin"].get("url", ""))

        bg_sub = ttk.Frame(link_frame)
        bg_sub.pack(fill="x", pady=5)
        ttk.Label(bg_sub, text="Web/Blog Başlık:", width=15).pack(side="left")
        self.entry_bg_title = ttk.Entry(bg_sub)
        self.entry_bg_title.pack(side="left", expand=True, fill="x", padx=(0,5))
        self.entry_bg_title.insert(0, self.data["blog"].get("title", ""))
        ttk.Label(bg_sub, text="URL:", width=5).pack(side="left")
        self.entry_bg_url = ttk.Entry(bg_sub)
        self.entry_bg_url.pack(side="left", expand=True, fill="x")
        self.entry_bg_url.insert(0, self.data["blog"].get("url", ""))

        about_frame = ttk.Labelframe(self.scrollable_frame, text="Hakkımda", bootstyle="success", padding=10)
        about_frame.pack(fill="x", pady=10)

        toolbar = ttk.Frame(about_frame)
        toolbar.pack(fill="x", pady=(0, 5))
        ttk.Button(toolbar, text="B", width=3, bootstyle="secondary-outline", command=lambda: self.insert_tag("<b>", "</b>")).pack(side="left", padx=2)
        ttk.Button(toolbar, text="I", width=3, bootstyle="secondary-outline", command=lambda: self.insert_tag("<i>", "</i>")).pack(side="left", padx=2)
        ttk.Separator(toolbar, orient="vertical").pack(side="left", padx=5, fill="y")
        ttk.Button(toolbar, text="⬅", width=3, bootstyle="secondary-outline", command=lambda: self.insert_align("left")).pack(side="left", padx=2)
        ttk.Button(toolbar, text="↔", width=3, bootstyle="secondary-outline", command=lambda: self.insert_align("center")).pack(side="left", padx=2)
        ttk.Button(toolbar, text="➡", width=3, bootstyle="secondary-outline", command=lambda: self.insert_align("right")).pack(side="left", padx=2)
        ttk.Separator(toolbar, orient="vertical").pack(side="left", padx=5, fill="y")
        ttk.Button(toolbar, text="Temizle", width=8, bootstyle="danger-outline", command=lambda: self.text_about.delete("1.0", tk.END)).pack(side="right", padx=2)

        self.text_about = tk.Text(about_frame, height=12, width=60, font=("Arial", 10))
        self.text_about.pack(fill="x")
        self.text_about.insert("1.0", self.data.get("about", ""))

        self.create_simple_list("Eğitimler", "education", "warning")
        self.create_certificate_section()
        self.create_simple_list("Yetenekler", "skills", "danger")
        self.create_simple_list("Kazanımlar / Projeler", "projects", "primary")

        btn_frame = ttk.Frame(self.scrollable_frame, padding=(0, 20, 0, 50))
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="💾 KAYDET", bootstyle="success-outline", width=20, command=self.save_data).pack(side="left", padx=(0, 15))
        ttk.Button(btn_frame, text="📄 PDF İNDİR", bootstyle="primary", width=20, command=self.generate_pdf).pack(side="left")

    def insert_tag(self, start_tag, end_tag):
        try:
            sel_start = self.text_about.index("sel.first")
            sel_end = self.text_about.index("sel.last")
            selected_text = self.text_about.get(sel_start, sel_end)
            new_text = f"{start_tag}{selected_text}{end_tag}"
            self.text_about.delete(sel_start, sel_end)
            self.text_about.insert(sel_start, new_text)
        except tk.TclError:
            messagebox.showinfo("Bilgi", "Lütfen biçimlendirmek istediğiniz metni seçin.")

    def insert_align(self, align):
        try:
            sel_start = self.text_about.index("sel.first")
            sel_end = self.text_about.index("sel.last")
            selected_text = self.text_about.get(sel_start, sel_end)
            new_text = f'<p align="{align}">{selected_text}</p>'
            self.text_about.delete(sel_start, sel_end)
            self.text_about.insert(sel_start, new_text)
        except tk.TclError:
            full_text = self.text_about.get("1.0", "end-1c")
            new_text = f'<p align="{align}">{full_text}</p>'
            self.text_about.delete("1.0", tk.END)
            self.text_about.insert("1.0", new_text)

    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Kes ✂️", command=lambda: self.root.focus_get().event_generate('<<Cut>>'))
        self.context_menu.add_command(label="Kopyala 📄", command=lambda: self.root.focus_get().event_generate('<<Copy>>'))
        self.context_menu.add_command(label="Yapıştır 📋", command=lambda: self.root.focus_get().event_generate('<<Paste>>'))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Tümünü Seç", command=lambda: self.root.focus_get().event_generate('<<SelectAll>>'))
        def do_popup(event):
            try:
                if event.widget.winfo_class() in ['Text', 'Entry', 'TEntry']:
                    self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
        self.root.bind_all("<Button-3>", do_popup)

    def create_input(self, parent, label, val):
        f = ttk.Frame(parent)
        f.pack(fill="x", pady=2)
        ttk.Label(f, text=label, width=10).pack(side="left")
        e = ttk.Entry(f)
        e.pack(side="right", expand=True, fill="x")
        if val: e.insert(0, val)
        return e

    def create_simple_list(self, title, key, color_style="secondary"):
        f = ttk.Labelframe(self.scrollable_frame, text=title, bootstyle=color_style, padding=10)
        f.pack(fill="x", pady=10)
        lb = tk.Listbox(f, height=3, borderwidth=0, highlightthickness=1)
        lb.pack(fill="x", pady=5)
        items = self.data.get(key, [])
        for item in items: lb.insert(tk.END, item)
        btn_f = ttk.Frame(f)
        btn_f.pack(fill="x")
        def add():
            val = simpledialog.askstring("Ekle", f"Yeni {title}:")
            if val: 
                lb.insert(tk.END, val)
                self.data[key].append(val)
        def delete():
            sel = lb.curselection()
            if sel:
                lb.delete(sel[0])
                del self.data[key][sel[0]]
        ttk.Button(btn_f, text="+ Ekle", bootstyle="secondary-outline", command=add).pack(side="left", padx=5)
        ttk.Button(btn_f, text="- Çıkar", bootstyle="danger-outline", command=delete).pack(side="right", padx=5)

    def create_certificate_section(self):
        title = "Sertifikalar"
        key = "certificates"
        f = ttk.Labelframe(self.scrollable_frame, text=title, bootstyle="warning", padding=10)
        f.pack(fill="x", pady=10)
        lb = tk.Listbox(f, height=3, borderwidth=0, highlightthickness=1)
        lb.pack(fill="x", pady=5)
        items = self.data.get(key, [])
        for item in items:
            if isinstance(item, str): lb.insert(tk.END, item)
            else:
                display = f"{item['name']} " if item['url'] else item['name']
                lb.insert(tk.END, display)
        btn_f = ttk.Frame(f)
        btn_f.pack(fill="x")
        def add_cert():
            popup = Toplevel(self.root)
            popup.title("Ekle")
            popup.geometry("350x150")
            tk.Label(popup, text="Sertifika Adı:").pack(pady=2)
            e_name = tk.Entry(popup, width=40)
            e_name.pack()
            tk.Label(popup, text="URL:").pack(pady=2)
            e_url = tk.Entry(popup, width=40)
            e_url.pack()
            def confirm():
                name = e_name.get()
                url = e_url.get()
                if name:
                    self.data[key].append({"name": name, "url": url})
                    lb.insert(tk.END, f"{name}")
                    popup.destroy()
            tk.Button(popup, text="Kaydet", command=confirm).pack(pady=10)
        def delete_cert():
            sel = lb.curselection()
            if sel:
                lb.delete(sel[0])
                del self.data[key][sel[0]]
        ttk.Button(btn_f, text="+ Ekle", bootstyle="secondary-outline", command=add_cert).pack(side="left", padx=5)
        ttk.Button(btn_f, text="- Çıkar", bootstyle="danger-outline", command=delete_cert).pack(side="right", padx=5)

    def select_photo(self):
        f = filedialog.askopenfilename(filetypes=[("Resimler", "*.jpg;*.png;*.jpeg")])
        if f:
            self.data["photo_path"] = f
            self.lbl_photo.config(text=os.path.basename(f))

    def save_data(self):
        self.data["name"] = self.entry_name.get()
        self.data["title"] = self.entry_title.get()
        self.data["phone"] = self.entry_phone.get()
        self.data["email"] = self.entry_email.get()
        self.data["linkedin"] = {"title": self.entry_lk_title.get(), "url": self.entry_lk_url.get()}
        self.data["blog"] = {"title": self.entry_bg_title.get(), "url": self.entry_bg_url.get()}
        self.data["about"] = self.text_about.get("1.0", tk.END).strip()
        with open(DATA_FILE, "w", encoding="utf-8") as f: 
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Başarılı", "Veriler Kaydedildi.")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f: 
                    loaded = json.load(f)
                if "linkedin" in loaded and isinstance(loaded["linkedin"], str):
                    loaded["linkedin"] = {"title": "LinkedIn", "url": loaded["linkedin"]}
                if "blog" in loaded and isinstance(loaded["blog"], str):
                    loaded["blog"] = {"title": "Web Sitesi", "url": loaded["blog"]}
                for k, v in self.data.items():
                    if k not in loaded: loaded[k] = v
                self.data = loaded
                new_certs = []
                for c in self.data.get("certificates", []):
                    if isinstance(c, str): new_certs.append({"name": c, "url": ""})
                    else: new_certs.append(c)
                self.data["certificates"] = new_certs
            except: pass

    def generate_pdf(self):
        self.save_data()
        pdf = FPDF()
        pdf.add_page()
        
        path_regular = r'C:\Windows\Fonts\arial.ttf'
        path_bold    = r'C:\Windows\Fonts\arialbd.ttf' 
        path_italic  = r'C:\Windows\Fonts\ariali.ttf' 
        path_bi      = r'C:\Windows\Fonts\arialbi.ttf'
        
        try:
            pdf.add_font('ArialTR', '', path_regular)
            pdf.add_font('ArialTR', 'B', path_bold)
            pdf.add_font('ArialTR', 'I', path_italic)
            pdf.add_font('ArialTR', 'BI', path_bi)
            
            FONT_FAMILY = "ArialTR"
        except:
            messagebox.showwarning("Font Hatası", "Arial Bold/Italic dosyaları bulunamadı. Standart font kullanılacak.")
            pdf.set_font("Arial", size=11)
            FONT_FAMILY = "Arial"

        pdf.set_font(FONT_FAMILY, '', 11)
        RENK_BASLIK = (46, 139, 87)
        RENK_METIN = (0, 0, 0)
        RENK_GRI = (80, 80, 80)

        resim_genislik = 30
        sol_bosluk = 10
        foto_yolu = self.data.get("photo_path", "")
        
        if foto_yolu and os.path.exists(foto_yolu):
            try:
                pdf.image(foto_yolu, x=sol_bosluk, y=10, w=resim_genislik)
                yazi_baslangic_x = sol_bosluk + resim_genislik + 5
                hizalama = 'L'
            except:
                yazi_baslangic_x = sol_bosluk
                hizalama = 'C'
        else:
            yazi_baslangic_x = sol_bosluk
            hizalama = 'C'

        pdf.set_xy(yazi_baslangic_x, 15)
        pdf.set_text_color(*RENK_METIN)
        pdf.set_font(FONT_FAMILY, 'B', 24)
        pdf.cell(0, 10, self.data.get("name", ""), align=hizalama, new_x="LMARGIN", new_y="NEXT")

        pdf.set_x(yazi_baslangic_x)
        pdf.set_text_color(*RENK_GRI)
        pdf.set_font(FONT_FAMILY, '', 14)
        pdf.cell(0, 8, self.data.get("title", ""), align=hizalama, new_x="LMARGIN", new_y="NEXT")

        pdf.set_xy(yazi_baslangic_x, pdf.get_y() + 2)
        pdf.set_font(FONT_FAMILY, '', 9)
        pdf.set_text_color(*RENK_BASLIK)
        
        parts = []
        if self.data.get("phone"): parts.append({"text": self.data["phone"], "url": None})
        if self.data.get("email"): parts.append({"text": self.data["email"], "url": None})
        lk = self.data.get("linkedin", {})
        if lk.get("title"): parts.append({"text": lk["title"], "url": lk.get("url")})
        bg = self.data.get("blog", {})
        if bg.get("title"): parts.append({"text": bg["title"], "url": bg.get("url")})

        separator = "  |  "
        if hizalama == 'C': start_x = 10 
        else: start_x = yazi_baslangic_x

        pdf.set_x(start_x)
        for i, p in enumerate(parts):
            text = p["text"]
            if p["url"]:
                pdf.set_text_color(*RENK_METIN)
                pdf.cell(pdf.get_string_width(text), 6, text, link=p["url"])
            else:
                pdf.set_text_color(*RENK_BASLIK)
                pdf.cell(pdf.get_string_width(text), 6, text)
            
            if i < len(parts) - 1:
                pdf.set_text_color(*RENK_BASLIK)
                pdf.cell(pdf.get_string_width(separator), 6, separator)

        pdf.ln(8)
        cizgi_y = max(pdf.get_y(), 50) 
        pdf.set_draw_color(*RENK_BASLIK)
        pdf.line(10, cizgi_y, 200, cizgi_y)
        pdf.set_xy(10, cizgi_y + 5)

        about_text = self.data.get("about", "")
        if about_text:
            if "<" not in about_text: 
                about_text = about_text.replace("\n", "<br>")
            
            pdf.set_text_color(*RENK_METIN)
            pdf.set_font(FONT_FAMILY, '', 11)
            
            try:
                pdf.write_html(about_text)
            except Exception as e:
                print(f"HTML Hatası: {e}")
                pdf.multi_cell(0, 5, self.data.get("about", ""))
            
            pdf.ln(5)

        

        y_start = pdf.get_y()
        
        pdf.set_xy(10, y_start)
        pdf.set_text_color(*RENK_BASLIK)
        pdf.set_font(FONT_FAMILY, '', 12)
        pdf.cell(90, 8, "Eğitim", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_text_color(*RENK_METIN)
        pdf.set_font(FONT_FAMILY, 'B', 10) 
        
        for item in self.data.get("education", []):
            pdf.set_x(10) 
            pdf.multi_cell(85, 5, f"{item}")
            pdf.ln(1) 
        
        pdf.ln(3) 

        
        pdf.set_x(10)
        pdf.set_text_color(*RENK_BASLIK)
        pdf.set_font(FONT_FAMILY, '', 12)
        pdf.cell(90, 8, "Sertifikalar", new_x="LMARGIN", new_y="NEXT")
        
        
        pdf.set_font(FONT_FAMILY, 'B', 10) 
        
        for cert in self.data.get("certificates", []):
            pdf.set_x(10)
            if cert["url"]:
                pdf.set_text_color(*RENK_METIN) 
                pdf.cell(90, 6, f"{cert['name']}", new_x="LMARGIN", new_y="NEXT", link=cert["url"])
            else:
                pdf.set_text_color(*RENK_METIN)
                pdf.cell(90, 6, f"{cert['name']}", new_x="LMARGIN", new_y="NEXT")

        y_left_end = pdf.get_y()

        pdf.set_xy(110, y_start)
        pdf.set_text_color(*RENK_BASLIK)
        pdf.set_font(FONT_FAMILY, '', 12)
        pdf.cell(80, 8, "Yetenekler", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_text_color(*RENK_METIN)
        pdf.set_font(FONT_FAMILY, 'B', 10)
        
        for item in self.data.get("skills", []):
            pdf.set_x(110) 
            pdf.cell(80, 5, f"{item}", new_x="LMARGIN", new_y="NEXT")

        pdf.set_xy(10, max(y_left_end, pdf.get_y()) + 10)
        
        pdf.set_text_color(*RENK_BASLIK)
        pdf.set_font(FONT_FAMILY, '', 12)
        pdf.cell(0, 8, "Kazanımlar / Projeler", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_draw_color(*RENK_BASLIK)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        
        pdf.set_text_color(*RENK_METIN)
        pdf.set_font(FONT_FAMILY, '', 10) 
        
        for item in self.data.get("projects", []):
            pdf.multi_cell(0, 6, f"> {item}")

        try:
            pdf.output("CV.pdf")
            os.startfile("CV.pdf")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = CVApp(root)
    root.mainloop()