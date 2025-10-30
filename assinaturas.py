import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import unicodedata
import re
import os

class GeradorAssinaturaApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerador de Assinatura")

        self.caminho_assinatura = None

        self.nome_var = tk.StringVar()
        self.conselho_var = tk.StringVar()
        self.profissao_var = tk.StringVar()

        tk.Label(master, text="Nome Completo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(master, textvariable=self.nome_var, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(master, text="Conselho/Número:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(master, textvariable=self.conselho_var, width=50).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(master, text="Profissão:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(master, textvariable=self.profissao_var, width=50).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Button(master, text="Selecionar Assinatura", command=self.selecionar_assinatura).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(master, text="Gerar Imagem de Evolução", command=self.gerar_evolucao).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(master, text="Gerar Imagem de Prescrição", command=self.gerar_prescricao).grid(row=4, column=1, padx=5, pady=5)

    def selecionar_assinatura(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.caminho_assinatura = file_path
            messagebox.showinfo("Assinatura Selecionada", f"Assinatura selecionada:\n{self.caminho_assinatura}")

    def _sanitizar_nome_arquivo(self, nome):
        nome_sanitizado = unicodedata.normalize('NFD', nome).encode('ascii', 'ignore').decode('utf-8')
        nome_sanitizado = re.sub(r'[^\w-]', '_', nome_sanitizado)
        nome_sanitizado = re.sub(r'__+', '_', nome_sanitizado)
        nome_sanitizado = nome_sanitizado.strip('_')
        return nome_sanitizado.lower()

    def redimensionar_assinatura(self, imagem_original, largura_max, altura_max):
        largura_original, altura_original = imagem_original.size
        proporcao = min(largura_max / largura_original, altura_max / altura_original)
        nova_largura = int(largura_original * proporcao)
        nova_altura = int(altura_original * proporcao)
        return imagem_original.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)

    def criar_imagem(self, largura, altura, tipo_imagem):
        if not self.caminho_assinatura:
            messagebox.showerror("Erro", "Selecione a assinatura primeiro!")
            return
        
        nome = self.nome_var.get().strip()
        conselho = self.conselho_var.get().strip()
        profissao = self.profissao_var.get().strip()

        if not nome or not conselho:
            messagebox.showerror("Erro", "Preencha nome e número do conselho!")
            return

        img = Image.new('RGBA', (largura, altura), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        try:
            fonte_evolucao = ImageFont.truetype("arial.ttf", 8)
            fonte_prescricao = ImageFont.truetype("arial.ttf", 11)
        except IOError:
            fonte_evolucao = ImageFont.load_default()
            fonte_prescricao = ImageFont.load_default()

        try:
            assinatura_img_original = Image.open(self.caminho_assinatura).convert("RGBA")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar a imagem da assinatura:\n{e}")
            return

        if tipo_imagem == "evolucao":
            # Área para assinatura (100x35)
            assinatura_img = self.redimensionar_assinatura(assinatura_img_original, 100, 35)
            pos_assinatura_x = (largura - assinatura_img.width) // 2
            pos_assinatura_y = 5
            img.paste(assinatura_img, (pos_assinatura_x, pos_assinatura_y), assinatura_img)

            # Texto centralizado
            espacamento_linha = 10
            pos_y_base = 48
            for i, texto in enumerate([nome, conselho, profissao]):
                largura_texto = draw.textbbox((0, 0), texto, font=fonte_evolucao)[2]
                pos_x = (largura - largura_texto) // 2
                draw.text((pos_x, pos_y_base + i * espacamento_linha), texto, fill='black', font=fonte_evolucao)

        else:  # prescricao
            # NOVA ÁREA DA ASSINATURA: 130x50 em x=195, y=21
            ASS_LARG = 130
            ASS_ALT = 50
            ASS_X = 190
            ASS_Y = 25

            assinatura_img = self.redimensionar_assinatura(assinatura_img_original, ASS_LARG, ASS_ALT)
            pos_assinatura_x = ASS_X + (ASS_LARG - assinatura_img.width) // 2
            pos_assinatura_y = ASS_Y + (ASS_ALT - assinatura_img.height) // 2
            img.paste(assinatura_img, (pos_assinatura_x, pos_assinatura_y), assinatura_img)

            # Texto com fonte maior (tamanho 10)
            espacamento_linha = 10
            pos_y_base = 94
            for i, texto in enumerate([nome, conselho, profissao]):
                largura_texto = draw.textbbox((0, 0), texto, font=fonte_prescricao)[2]
                pos_x = 171 + (138 - largura_texto) // 2
                draw.text((pos_x, pos_y_base + i * espacamento_linha), texto, fill='black', font=fonte_prescricao)

        # Criação da pasta output
        os.makedirs("output", exist_ok=True)
        nome_sanitizado = self._sanitizar_nome_arquivo(nome)
        if tipo_imagem == "evolucao":
            nome_arquivo = os.path.join("output", f"assina_{nome_sanitizado}_evolucao.bmp")
        else:
            nome_arquivo = os.path.join("output", f"assina_{nome_sanitizado}_prescricao.bmp")

        try:
            img.save(nome_arquivo)
            messagebox.showinfo("Sucesso", f"Imagem salva em:\n{nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar a imagem:\n{e}")

    def gerar_evolucao(self):
        self.criar_imagem(268, 85, "evolucao")

    def gerar_prescricao(self):
        self.criar_imagem(344, 143, "prescricao")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeradorAssinaturaApp(root)
    root.mainloop()
