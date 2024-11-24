import os
import py7zr
import requests
from pathlib import Path

def download_file(url):
  """Descarga un archivo desde una URL."""
  download_dir = str(Path.home() / "Downloads")
  file_name = Path(os.path.basename(url)).stem  # Obtener el nombre del archivo
  ext_file = Path(os.path.basename(url)).suffix  # Obtener la extensión del archivo
  
  # Ruta completa del archivo original
  original_file = os.path.join(download_dir, f"{file_name}{ext_file}")
  
  # Descargar el archivo
  downfile = requests.get(url, stream=True, allow_redirects=True)
  with open(original_file, 'wb') as f:
    for chunk in downfile.iter_content(chunk_size=8192):
      if chunk:
        f.write(chunk)
    
  # Comprimir y cifrar
  compressed_file = zipfile(download_dir, file_name, ext_file, password="1234")
    
  # Eliminar el archivo original después de comprimirlo
  os.remove(original_file)
    
  return compressed_file, f"{file_name}.7z"

def zipfile(download_dir, file_name, ext_name, password="12345678"):
  """Comprime y cifra un archivo usando 7z"""
  # Ruta completa del archivo original
  original_file = os.path.join(download_dir, f"{file_name}{ext_name}")
  
  # Ruta completa del archivo comprimido
  compressed_file = os.path.join(download_dir, f"{file_name}.7z")
  
  # Comprimir y cifrar con 7z
  with py7zr.SevenZipFile(compressed_file, 'w', password=password) as zip_file:
    zip_file.write(original_file, arcname=f"{file_name}{ext_name}")
  
  return compressed_file
