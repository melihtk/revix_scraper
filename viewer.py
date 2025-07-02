from __future__ import annotations

from tkinter import Tk, Label, Button, Text, Entry, LEFT, RIGHT, END
from tkinter import messagebox
from PIL import Image, ImageTk

from utils import load_ads


class AdViewer:
    def __init__(self, ads):
        self.ads = ads
        self.filtered = ads
        self.index = 0

        self.root = Tk()
        self.root.title("Inserate Viewer")

        self.title_label = Label(self.root, text="", font=("Arial", 14, "bold"))
        self.title_label.pack()

        self.price_label = Label(self.root, text="", fg="green")
        self.price_label.pack()

        self.text_box = Text(self.root, height=10, width=60)
        self.text_box.pack()

        nav_frame = Label(self.root)
        nav_frame.pack()

        self.prev_btn = Button(nav_frame, text="Zurück", command=self.prev_ad)
        self.prev_btn.pack(side=LEFT)

        self.next_btn = Button(nav_frame, text="Weiter", command=self.next_ad)
        self.next_btn.pack(side=LEFT)

        self.copy_btn = Button(nav_frame, text="In Zwischenablage", command=self.copy_clipboard)
        self.copy_btn.pack(side=LEFT)

        search_frame = Label(self.root)
        search_frame.pack()
        self.search_entry = Entry(search_frame)
        self.search_entry.pack(side=LEFT)
        Button(search_frame, text="Suchen", command=self.search).pack(side=LEFT)

        self.image_label = Label(self.root)
        self.image_label.pack()

        self.show_ad()
        self.root.mainloop()

    def show_ad(self):
        if not self.filtered:
            messagebox.showinfo("Info", "Keine Inserate gefunden")
            return
        ad = self.filtered[self.index]
        self.title_label.config(text=ad["title"])
        self.price_label.config(text=ad["price"])
        self.text_box.delete("1.0", END)
        self.text_box.insert("1.0", ad["description"])
        img_path = ad["images"][0] if ad["images"] else None
        if img_path:
            img = Image.open(img_path)
            img.thumbnail((300, 300))
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo)
        else:
            self.image_label.config(image="")

    def next_ad(self):
        self.index = (self.index + 1) % len(self.filtered)
        self.show_ad()

    def prev_ad(self):
        self.index = (self.index - 1) % len(self.filtered)
        self.show_ad()

    def copy_clipboard(self):
        ad = self.filtered[self.index]
        text = f"{ad['title']}\n{ad['price']}\n{ad['description']}"
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Kopiert", "Text in Zwischenablage")

    def search(self):
        term = self.search_entry.get().lower()
        self.filtered = [ad for ad in self.ads if term in ad["title"].lower() or term in ad["description"].lower()]
        if not self.filtered:
            messagebox.showinfo("Info", "Keine Treffer")
            self.filtered = self.ads
        self.index = 0
        self.show_ad()


if __name__ == "__main__":
    ads = load_ads()
    if not ads:
        print("Keine Inserate gefunden. Bitte zuerst scraper ausführen.")
    else:
        AdViewer(ads)
