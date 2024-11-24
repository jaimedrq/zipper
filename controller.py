import os
from flask import Flask, request, jsonify, send_file
from helper_methods import download_file, zipfile

if __name__ == '__main__':
  app = Flask(__name__)

  @app.route('/downloadzipper', methods=['GET'])
  def zipper():
    """Servicio para descargar y comprimir archivos."""
    try:
      url = request.args.get('url', None)
      if not url: return jsonify({'error': 'URL no proporcionada'}), 400

      downloaded_file, filename = download_file(url)  # Descargar el archivo
      
      # Enviar el archivo y luego eliminarlo
      response = send_file(
        downloaded_file,
        as_attachment=True,
        download_name=filename,
        mimetype='application/x-7z-compressed'
      )
      
      # Configurar una función de callback para eliminar el archivo después de enviarlo
      @response.call_on_close
      def cleanup():
        """"""
        print("wasabi!")
        print(f"Intentando eliminar el archivo: {downloaded_file}")
        if os.path.exists(downloaded_file):
          os.remove(downloaded_file)
          print(f"Archivo eliminado: {downloaded_file}")
        else:
          print(f"El archivo no existe: {downloaded_file}")
      
      return response

    except Exception as e:
      return jsonify({'error': f'Error en el procesamiento: {str(e)}'}), 500

  
  # ----------------
  # RUN
  # ----------------
  app.run(debug=True, host='0.0.0.0', port=80)

  # ----------------
  # CALL FUNCTION
  # ----------------
  # curl -O -J "http://localhost/downloadzipper?url=https://image.freepik.com/vector-gratis/ilustracion-vector-prueba-trabajo-examen_138676-243.jpg"