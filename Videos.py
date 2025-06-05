import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp as youtube_dl
import ffmpeg
import os
import threading

def escolher_diretorio():
    caminho = filedialog.askdirectory()
    if caminho:
        pasta_saida.set(caminho)

def baixar():
    url = entrada_url.get()
    formato = formato_var.get()
    caminho = pasta_saida.get()

    if not url or not caminho:
        messagebox.showwarning("Aviso", "Informe a URL e o caminho de saída.")
        return
    if not os.path.isdir(caminho):
        messagebox.showwarning("Aviso", "Caminho de saída inválido.")
        return

    def download_task():
        try:
            ydl_opts = {
                'outtmpl': os.path.join(caminho, '%(title)s.%(ext)s'),
                'format': 'best' if formato == "MP4" else 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }] if formato == "MP3" else [],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get('title', 'Desconhecido')
                janela.after(0, lambda: status_var.set(f"Baixando: {titulo}"))

                if formato == "MP4":
                    arquivo = ydl.prepare_filename(info)
                    janela.after(0, lambda: status_var.set("Download de vídeo (MP4) concluído!"))
                else:
                    arquivo = ydl.prepare_filename(info).replace('.webm', '.mp3')  # Ajuste para MP3
                    janela.after(0, lambda: status_var.set("Download de áudio (MP3) concluído!"))

        except Exception as e:
            janela.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}"))
            janela.after(0, lambda: status_var.set("Erro no download."))

    threading.Thread(target=download_task, daemon=True).start()

# ----- Interface Gráfica -----
janela = tk.Tk()
janela.title("YouTube Downloader")

# Campos de entrada
tk.Label(janela, text="URL do YouTube:").pack(pady=5)
entrada_url = tk.Entry(janela, width=50)
entrada_url.pack()

tk.Label(janela, text="Salvar em:").pack(pady=5)
pasta_saida = tk.StringVar(value="")
tk.Entry(janela, textvariable=pasta_saida, width=40).pack(side=tk.LEFT, padx=(10, 0))
tk.Button(janela, text="Procurar", command=escolher_diretorio).pack(side=tk.LEFT, padx=10)

# Seleção de formato
formato_var = tk.StringVar(value="MP4")
tk.Label(janela, text="Formato:").pack(pady=5)
tk.Radiobutton(janela, text="MP4 (Vídeo)", variable=formato_var, value="MP4").pack()
tk.Radiobutton(janela, text="MP3 (Áudio)", variable=formato_var, value="MP3").pack()

# Botão de download
tk.Button(janela, text="Baixar", command=baixar, bg="green", fg="white").pack(pady=10)

# Status
status_var = tk.StringVar(value="")
tk.Label(janela, textvariable=status_var, fg="blue").pack()

janela.mainloop()


# sudo apt install python3-venv - INSTALA O VENV PARA AMBIENTES VIRTUAIS
# python3 -m venv meu_ambiente - CRIA UM AMBIENTE VIRTUAL
# source Teste-Video/bin/activate - ATIVAR O AMBIENTE VIRTUAL
# deactivate - DESATIVAR O AMBIENTE VIRTUAL
