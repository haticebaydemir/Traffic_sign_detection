import os

image_files = []

# "data/test" dizinine geçiş yapın
try:
    os.chdir(os.path.join("data", "test"))
except FileNotFoundError as e:
    print(f"Hata: {e}")
    # Gerekli dizinlerin var olup olmadığını kontrol edin
    os.makedirs(os.path.join("data", "test"), exist_ok=True)
    os.chdir(os.path.join("data", "test"))

# Mevcut dizindeki ".jpg" uzantılı dosyaları listeye ekleyin
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append("data/test/" + filename)

# Üst dizine geri dönün
os.chdir("..")

# "test.txt" dosyasını yazın
with open("test.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image + "\n")  # Tek satırda yazma işlemi

# Tekrar üst dizine geri dönün (gerekiyorsa)
os.chdir("..")
