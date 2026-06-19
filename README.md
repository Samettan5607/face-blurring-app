# Gerçek Zamanlı Yüz Bulanıklaştırma Uygulaması

Bu proje, bilgisayarınızın kamerasından (webcam) alınan canlı video akışında insan yüzlerini gerçek zamanlı olarak tespit eder ve bu bölgeleri Gaussian Blur (Gauss Bulanıklığı) kullanarak otomatik olarak sansürler. Özellikle gizlilik sağlama ve görüntü işleme temellerini öğrenme amacıyla geliştirilmiş bir Python uygulamasıdır.

---

## Özellikler

*   **Gerçek Zamanlı Tespit:** Kameradan saniyede onlarca kare (FPS) işleyerek yüzleri anlık olarak algılar.
*   **Dinamik Bulanıklaştırma:** Yüzün kameraya olan mesafesine (ekrandaki boyutuna) göre bulanıklaştırma derecesini (kernel size) otomatik ayarlar.
*   **Hata Toleransı ve Güvenlik:** Kamera koordinatlarının ekran dışına taşmasını engellemek için sınır kontrolleri içerir.
*   **Kolay Kapatma:** Aktif pencere üzerindeyken klavyeden `q` tuşuna basarak uygulamayı güvenli bir şekilde kapatabilirsiniz.

---

## Kullanılan Teknolojiler

*   **Python 3.x:** Ana programlama dili.
*   **OpenCV (opencv-python):** Görüntü işleme, kamera kontrolü ve yüz tespiti için kullanılan kütüphane.
*   **Haar Cascade:** Yüz tespiti için OpenCV ile hazır gelen hafif ve hızlı makine öğrenimi tabanlı sınıflandırıcı model (`haarcascade_frontalface_default.xml`).

---

## Kurulum ve Çalıştırma

### 1. Gereksinimlerin Yüklenmesi

Projeyi çalıştırmadan önce Python yüklü olmalıdır. Ardından gerekli OpenCV kütüphanesini yüklemek için proje dizininde şu komutu çalıştırabilirsiniz:

```bash
pip install -r requirements.txt
```

### 2. Uygulamanın Başlatılması

Uygulamayı başlatmak için terminalden veya komut satırından aşağıdaki komutu çalıştırın:

```bash
python face_blur.py
```

### 3. Uygulamayı Kapatma

Kamera penceresi açık ve seçili durumdayken klavyenizden **`q`** tuşuna basarak uygulamayı sonlandırabilir ve kamerayı serbest bırakabilirsiniz.

---

## .exe Dosyası Oluşturma (Bağımsız Çalıştırılabilir Dosya)

Uygulamayı herhangi bir Python kurulumuna ihtiyaç duymadan çalışabilecek tek bir `.exe` dosyası haline getirmek için **PyInstaller** kullanabilirsiniz.

### 1. PyInstaller Kurulumu
```bash
pip install pyinstaller
```

### 2. Derleme Komutu
Pencere modunda (arka planda konsol ekranı açılmadan) çalıştırmak ve tüm bağımlılıkları tek bir dosyada toplamak için şu komutu çalıştırın:

```bash
pyinstaller --onefile --noconsole face_blur.py
```

> **Not:** Haar Cascade XML dosyası OpenCV kütüphanesinin içine gömülü olarak sistemde yer aldığından, derleme sonrasında da doğru şekilde bulunabilmesi için `cv2.data.haarcascades` yolunu dinamik olarak çözümleyen kod yapısı eklenmiştir.

Oluşan `.exe` dosyası projenin ana dizininde oluşacak olan `dist` klasörü altında yer alacaktır.

---

## Kodun Çalışma Mantığı (Walkthrough)

1.  **Haar Cascade Yükleme:** `cv2.CascadeClassifier` aracılığıyla OpenCV'nin dahili dizinindeki önceden eğitilmiş yüz algılama modeli yüklenir.
2.  **Kamera Erişimi:** `cv2.VideoCapture(0)` ile sistemdeki birincil kamera açılır.
3.  **Kare Okuma & Dönüştürme:** Kameradan gelen her kare, yüz tespitinin daha kararlı çalışması için gri tonlamaya (`cv2.cvtColor`) dönüştürülür.
4.  **Tespit (`detectMultiScale`):** Gri resim üzerinde yüzler taranır ve koordinatları `(x, y, genişlik, yükseklik)` olarak alınır.
5.  **Bulanıklaştırma (`GaussianBlur`):** Tespit edilen her yüz bölgesi (Region of Interest - ROI) kesilerek dinamik boyutlandırılmış bir filtre ile bulanıklaştırılır ve orijinal kareye geri yazılır.
6.  **Gösterim:** Kareler `cv2.imshow` ile ekrana yansıtılır.
