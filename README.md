# Traffic_sign_detection
## Projenin kodlarına [buraya tıklayarak]( https://colab.research.google.com/drive/1QZzqFVI5vcUxTPOAw6E1fz2CtvsPgRNI) ulaşabilirsiniz.
### 1.ADIM = DARKNET KLONLAMA VE KURULUMU
!git clone https://github.com/AlexeyAB/darknet <br/>
%cd darknet<br/>
!sed -i 's/OPENCV=0/OPENCV=1/' Makefile<br/>
!sed -i 's/GPU=0/GPU=1/' Makefile<br/>
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile<br/>
!sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile<br/>
#verify CUDA<br/>
!/usr/local/cuda/bin/nvcc --version <br/>
!make<br/>
### ADIM 2: YARDIMCI FONKSİYONLARIN TANIMLANMASI
# define helper functions(Bu fonksiyon, belirtilen dosya yolundaki görüntüyü okuyup ekranda gösterir.)<br/>
def imShow(path): <br/>
  import cv2 <br/>
  import matplotlib.pyplot as plt <br/>
  %matplotlib inline <br/>

  image = cv2.imread(path) <br/>
  height, width = image.shape[:2] <br/>
  resized_image = cv2.resize(image,(3*width, 3*height), interpolation = cv2.INTER_CUBIC) <br/>

  fig = plt.gcf() <br/>
  fig.set_size_inches(18, 10) <br/>
  plt.axis("off") <br/>
  plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)) <br/>
  plt.show() <br/>

# use this to upload files <br/>
def upload(): <br/>
  from google.colab import files <br/>
  uploaded = files.upload() <br/> 
  for name, data in uploaded.items(): <br/>
    with open(name, 'wb') as f: <br/>
      f.write(data)<br/>
      print ('saved file', name)<br/>

`# use this to download a file ` <br/>
def download(path):<br/>
  from google.colab import files<br/>
  files.download(path)<br/>
  ### ADIM 3: FOTOĞRAF TOPLAMA VE ETİKETLEME
  Üzerinde tanıma yapacağımız nesne için bir çok fotoğrafa ihtiyacımız olacak. Ne kadar fazla ve ne kadar farklı tip fotoğrafımız olursa o kadar doğru bir modelimiz olur.

Fotoğraflarımızı 2 şekilde hazırlayabiliriz: <br/>
1)Google'ın sunmuş olduğu [Open Images](https://storage.googleapis.com/openimages/web/index.html) sitesinde 600'ün üzerinde nesnenin etiketlenmiş halde binlerce fotoğrafı yer alıyor. Bu siteden istediğimiz kadar fotoğrafı indirip kullanabiliriz.<br/>
2)Tanıma yapacağımız nesneleri kendimiz fotoğraflayabilir veya google'dan bulduğumuz fotoğrafları etiketleyerek kullanabiliriz.

%cd ..<br/>
from google.colab import drive<br/>
drive.mount('/content/gdrive')<br/>
# this creates a symbolic link so that now the path /content/gdrive/My\ Drive/ is equal to /mydrive<br/>
#(/content/gdrive/My\ Drive/ yolunu kullanımı kolay olması sebebi ile /mydrive yoluna eşitleriz.)<br/>
!ln -s /content/gdrive/My\ Drive/ /mydrive<br/>
!ls /mydrive<br/>
### ADIM 4: HAZIRLAMIŞ OLDUĞUMUZ VERİ SETİNİ YÜKLEME
 Hazırlamış olduğumuz veri setini google collab'e yüklemeliyiz. <br/>

Bunun için drive'ımızda bir yolov4 diye klasör oluşturalım.(bu klasörü daha sonra gerekli dosyaları bir arada toplamak için kullanacağız) <br/>

Veri setiniz bir klasör içine alıp zip haline getirerek drive'ımıza yükleyip oradan google colab içine aktarmak bize zaman kazandıracaktır. <br/>

`# this is where my datasets are stored within my Google Drive (I created a yolov4 folder to store all important files for custom training) `<br/>
%cd darknet/<br/>
!ls /mydrive/yolov4<br/>
# Copies the training and test datasets and extracts them to the specified directory.(eğitim ve test dizinlerini kopyalar ve belirtilen dizine çıkarır.)<br/>
!cp /mydrive/yolov4/obj.zip ../<br/>
!cp /mydrive/yolov4/test.zip ../<br/>
# unzip the datasets and their contents so that they are now in /darknet/data/ folder<br/>
!unzip ../obj.zip -d data/<br/>
!unzip ../test.zip -d data/<br/>
### ADIM 5: EĞİTİM İÇİN GEREKLİ DOSYALARI HAZIRLAYALIM
 Bu adımda eğitim için gerekli olan .cfg file, obj.data, obj.names ve train.txt dosyalarını oluşturacağız. <br/>
 *-Config Dosyası* <br/>
` # download cfg to google drive and change its name`<br/>
`%cd darknet/ `<br/>
!cp cfg/yolov4-custom.cfg /mydrive/yolov4/yolov4-obj.cfg<br/>
Config dosyamızda yapmamız gereken değişiklikler:<br/>

(Burada verilen değerler bu değişkenlerin önerilen değerleridir.) <br/>

1.   batch = 64 ve subdivision 16.<br/>

3.   max_batches değerini (2000 * eğitilen sınıf sayısı) değerine eşitliyoruz.<br/>

4.   steps değerlerini (%80 of max_batches) , (%90 of max_batches) yapıyoruz.<br/>

5.   [yolo] başlığı altındaki classes değerlerini eğitim yaptığımız sınıf sayısı ile değiştiriyoruz. <br/>

6.   filters değişkenlerini de (eğitim yapacağımız sınıf sayısı + 5 )*3 değerine eşitliyoruz <br/>


# #Copies the configuration files and tag name files to the relevant directories.
#(Yapılandırma dosyalarını ve etiket isim dosyalarını ilgili dizinlere kopyalar.)

!cp /mydrive/yolov4/yolov4-obj.cfg ./cfg <br/>
*-obj.names ve obj.data*<br/>

yolov3 isimli klasörümüz içine obj.names isimli bir dosya oluşturalım ve dosyayı eğitim yapacağımız nesleriniz isimlerini yazıyoruz.<br/>

ÖRNEĞİN:

Guitar
Mobile Phone


Aynı klasör içinde obj.data isimle bir dosya oluşturarak içine eğitim yapacağımız nesne sayısını, eğitim yaparken kullanacağımız train.txt, text.txt ve obj.names isimli dosyaların adreslerini ve eğitim sonucu bulduğumuz ağırlıkları kaydedeceğimiz dizini yazıyoruz.<br/>

ÖRNEĞİN:

classes = 2
train = data/train.txt
valid = data/test.txt
names = data/obj.names
backup = /mydrive

#Training and testing rules are created. (Eğitim ve test dosyalarını oluşturur.)<br/>
!cp /mydrive/yolov4/obj.names ./data<br/>
!cp /mydrive/yolov4/obj.data  ./data<br/>
*-Train ve Test Dosyaları*<br/>


generate_train.py




import os
image_files = []
os.chdir(os.path.join("data", "obj"))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append("data/obj/" + filename)
os.chdir("..")
with open("train.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()
os.chdir("..")


generate_test.py




import os

image_files = []
os.chdir(os.path.join("data", "test"))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        image_files.append("data/test/" + filename)
os.chdir("..")
with open("test.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()
os.chdir("..")


# upload the generate_train.py and generate_test.py script to cloud VM from Google Drive
!cp /mydrive/yolov4/generate_train.py ./
!cp /mydrive/yolov4/generate_test.py ./


!python generate_train.py
!python generate_test.py
# verify that the newly generated train.txt and test.txt can be seen in our darknet/data folder
!ls data/

### ADIM 6: ÖNCEDEN EĞİTİLMİŞ CONVOLUTİONAL KATMANLARIN AĞIRLIKLARINI İNDİRME
Bu adımda önceden eğitilmiş yolov3 için kullanılmış deeplearning katmanları ağırlıklarını indiriyoruz. Bu adımı uygulamak zorunda değiliz ama eğitime bu ağırlıklarla başlamak eğittiğimiz modelin daha doğru çalışmasına ve eğitim süresini kısaltmaya yardımcı olacaktır. <br/>
!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137
### ADIM 7: KENDİ NESNE TANIYICIMIZI EĞİTELİM
Gerekli tüm dosyalar hazır, eğitime başlayabiliriz.<br/>
Eğitimimiz uzun süreceği için google collab bizi serverdan atabilir. Bunun önüne geçmek için aktif olduğumuzu bir şekile bildirmeliyiz.<br/>

Bunun için de sayfanın üst tarafına sağ tıklayıp "ögeyi denetle" veya "incele" seçeneğiniz seçip, çıkan pencereden "console"'a tıklayıp açılan komut satırına aşağıdaki kodu ekleyip enter tuşuna basarsak bu kod bizim 10 dakikada bir connect butonuna basarak bizim aktif kalmamızı sağlayacaktır.


function ClickConnect(){
console.log("Working"); 
document.querySelector("colab-toolbar-button#connect").click() 
}
setInterval(ClickConnect,60000)

### EĞİTİM

Sıradaki komut ile eğitim başlayacaktır.<br/>

Eğitimimizin süresi veri setinizdeki fotoğraf sayısı, fotoğrafların kalitesi, eğitim yaptığınız nesne sayısı gibi faktörlere göre değişebilir. Modelimizin doğruluğu için loss değerimiz önemlidir. Loss değerimiz ne kadar düşük olursa modelimiz o kadar doğru çalışır. Modelimizi loss değeri azalmayı durdurana kadar çalıştırıp veri setimize göre mümkün olan en doğru modeli eğitebiliriz. 

```#Trains the model with the specified data and configuration files. The -dont_show parameter is used to not show graphics during training, while -map provides performance measurements during the training process.
#(Modeli belirtilen veri ve yapılandırma dosyalarıyla eğitir. -dont_show parametresi, eğitim sırasında grafikleri göstermemek için kullanılır, -map ise eğitim sürecindeki performans ölçümlerini sağlar.)
!./darknet detector train data/obj.data cfg/yolov4-obj.cfg yolov4.conv.137 -dont_show -map


Modelimizi eğittikten sonra eğitim sırasında loss değerimizin nasıl değiştiğine dair bir grafik görebiliriz.


# eğitimimize ait grafiğimiz.
imShow('chart.png')
#We can continue education from where we left off.(# eğitime kaldığımız yerden devam edebiliriz.)

!./darknet detector train data/obj.data cfg/yolov4-obj.cfg /mydrive/yolov4/backup/yolov4-obj_last.weights -dont_show

### ADIM 7: EĞİTTİĞİMİZ MODELİMİZİ KULLANALIM
Eğitimimiz tamamlandı, şimdi istediğimiz fotoğraflar üzerinde tanıma yapabiliriz.
`#Runs the command that evaluates the performance of the model.(#Modelin performansını değerlendiren komutu çalıştırır.)`

`!./darknet detector map data/obj.data cfg/yolov4-obj.cfg /mydrive/yolov4/backup/yolov4-obj_best.weights `<br/>
### ADIM 8: Modelimizi Çalıştıralım!!!

# need to set our custom cfg to test mode.(#cfy'yi test moduna ayarlarız.)
%cd cfg
!sed -i 's/batch=64/batch=1/' yolov4-obj.cfg
!sed -i 's/subdivisions=16/subdivisions=1/' yolov4-obj.cfg
%cd ..

```
#It performs object detection on the test image and displays the results.#(Test görüntüsü üzerinde nesne algılama işlemi yapar ve sonuçları gösterir.)
!./darknet detector test data/obj.data cfg/yolov4-obj.cfg /mydrive/yolov4/backup/yolov4-obj_last.weights /mydrive/images/car4.jpg -thresh 0.3
imShow('predictions.jpg')

Bu projede "generate_train.py" test verilerimizi listeye atan, genellikle eğitim veri setinin yol bilgilerini içeren bir metin dosyası örneğin; train.txt oluşturmak için kullanılır.

"generate_test.py" train verilerimizi listeyen atan ve YOLO modeli için test dosyalarının otomatik olarak oluşturulmasına yardımcı olur. Bu dosya, genellikle test veri setinin yol bilgilerini içeren bir metin dosyası örneğin;test.txt oluşturmak için kullanılır.

obj.data dosyası,YOLO nesne algılama modeli eğitimi ve testi için gerekli olan bilgileri içeren bir yapılandırma dosyasıdır. Bu dosya, eğitim ve test sürecinde kullanılan veri yollarını ve diğer önemli parametreleri tanımlar.

obj.names dosyası, YOLO modelinin eğitim ve test sürecinde kullandığı sınıf (etiket) isimlerini içeren bir dosyadır. Bu dosya, modelin tanıyacağı nesne sınıflarının isimlerini belirtir.
