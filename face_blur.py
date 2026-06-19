import cv2
import sys

def main():
    print("Gerçek Zamanlı Yüz Bulanıklaştırma Uygulaması Başlatılıyor...")
    
    # Haar Cascade yüz tespit modelini OpenCV'nin varsayılan dizininden yüklüyoruz.
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    if face_cascade.empty():
        print("Hata: Haar Cascade model dosyası yüklenemedi!")
        sys.exit(1)
        
    print("Haar Cascade modeli başarıyla yüklendi.")
    
    # Kamerayı başlatıyoruz. Varsayılan kamera indeksi 0'dır.
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Hata: Bilgisayar kamerası (webcam) açılamadı!")
        print("Lütfen kameranızın bağlı olduğundan ve başka bir uygulama tarafından kullanılmadığından emin olun.")
        sys.exit(1)
        
    print("Kamera başarıyla açıldı. Pencereyi kapatmak veya çıkış yapmak için 'q' tuşuna basın.")
    
    # Pencere adını tanımlıyoruz
    window_name = "Gercek Zamanli Yuz Bulaniklastirma"
    
    # Pencerenin boyutunun kullanıcı tarafından değiştirilebilmesi için ayar
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    try:
        while True:
            # Kameradan bir kare (frame) okuyoruz
            ret, frame = cap.read()
            if not ret:
                print("Hata: Kameradan canlı görüntü akışı alınamıyor.")
                break
                
            # Görüntü boyutlarını alıyoruz (sınır taşmalarını önlemek için)
            img_h, img_w, _ = frame.shape
            
            # Yüz tespiti gri tonlamalı görüntülerde daha hızlı ve kararlı çalışır
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Yüzleri tespit ediyoruz
            # scaleFactor: Görüntü boyutunun her ölçekte ne kadar azaltılacağını belirtir (1.1 = %10 azaltma)
            # minNeighbors: Her aday dikdörtgenin kaç komşusu olması gerektiğini belirtir (daha yüksek değer daha az yanlış tespit)
            # minSize: Tespit edilecek minimum yüz boyutu
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # Tespit edilen her bir yüzü bulanıklaştırıyoruz
            for (x, y, w, h) in faces:
                # Sınır dışı koordinatları kırpıyoruz (kamera görüntüsü dışına çıkmayı önler)
                x_start = max(0, x)
                y_start = max(0, y)
                x_end = min(img_w, x + w)
                y_end = min(img_h, y + h)
                
                # Geçerli bir bölge olup olmadığını kontrol ediyoruz
                if x_end > x_start and y_end > y_start:
                    # Yüz bölgesini (ROI) kesiyoruz
                    face_roi = frame[y_start:y_end, x_start:x_end]
                    
                    # Yüzün boyutuna göre dinamik bir bulanıklık çekirdeği (kernel size) hesaplıyoruz
                    # Çekirdek boyutu tek sayı (odd) olmalıdır.
                    ksize_w = int(w * 0.4) | 1
                    ksize_h = int(h * 0.4) | 1
                    
                    # Aşırı küçük değerleri önlemek için alt sınır belirliyoruz (en az 15x15)
                    ksize_w = max(15, ksize_w)
                    ksize_h = max(15, ksize_h)
                    
                    # Gaussian Blur uyguluyoruz
                    blurred_face = cv2.GaussianBlur(face_roi, (ksize_w, ksize_h), 0)
                    
                    # Bulanıklaştırılmış yüzü orijinal kareye geri yerleştiriyoruz
                    frame[y_start:y_end, x_start:x_end] = blurred_face
                    
            # İşlenmiş görüntüyü ekranda gösteriyoruz
            cv2.imshow(window_name, frame)
            
            # 'q' tuşuna basılıp basılmadığını kontrol ediyoruz
            # waitKey(1) 1 milisaniye bekler, klavye girdisini kontrol eder
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Çıkış tuşuna ('q') basıldı. Uygulama kapatılıyor...")
                break
                
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        
    finally:
        # Kaynakları serbest bırakıyoruz
        cap.release()
        cv2.destroyAllWindows()
        print("Kamera bağlantısı kapatıldı ve pencereler yok edildi. Hoşça kalın!")

if __name__ == "__main__":
    main()
