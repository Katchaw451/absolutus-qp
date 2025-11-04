import qrcode
from PIL import Image

url = "https://github.com/Katchaw451/absolutus-qp/raw/main/pitch_ip.pdf"
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_download_pdf.png")
print("QR code salvo como qr_download_pdf.png")
