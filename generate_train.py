import os

image_files = []

# "data/obj" dizinine geçiş yapın
try:
    os.chdir(os.path.join("data", "obj"))
except FileNotFoundError as e:
    print(f"Hata: {e}")
    # Gerekli dizinlerin var olup olmadığını kontrol edin
    os.makedirs(os.path.join("data", "obj"), exist_ok=True)

# Mevcut dizindeki ".jpg" uzantılı dosyaları listeye ekleyin
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append("data/obj/" + filename)

# Üst dizine geri dönün
os.chdir("..")

# "train.txt" dosyasını yazın
with open("train.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image + "\n")

# Tekrar üst dizine geri dönün (gerekiyorsa)
os.chdir("..")
