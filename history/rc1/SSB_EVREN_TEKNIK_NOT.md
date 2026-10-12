# TÜRKİYE ARAZİ ÖRTÜSÜ V2 — TEKNİK BİLGİ NOTU (SSB & EVREN)
## Coğrafi Olarak Bağımsız Değerlendirme ve Yayın Adayı Raporu

**Tarih:** 2026-10-12  
**Sürüm:** V2.0-RC1 (Yayın Adayı)  
**Model Tanımı:** Turkey-scale Sentinel-2 RGB land-cover classification model with geographically disjoint evaluation and prior-shift calibration  
**Altyapı:** EVREN Kamu 1-GPU Sandkutusu (0 Retraining, 0 Ücretli Servis)  

---

### 1. Yönetici Özeti
Türkiye Arazi Örtüsü V2 araştırma çalışmasında, EVREN platformunun kısıtları (tek GPU, stok Ultralytics, ek harici kütüphane olmaması) dahilinde veri seviyesinde sınıf dengelemesi ve sonradan uygulanan olasılık öncülü kalibrasyonu ($\\tau = 0.50$) geliştirilmiştir.

Eğitim ve doğrulama süreçlerinde hiç görülmemiş 7 bağımsız ilde (Artvin, Edirne, Mersin, Kars, Mardin, Muğla, Nevşehir) toplam **68.558** çözümlenmiş Sentinel-2 RGB yaması üzerinde yapılan tek seferlik nihai test tamamlanmıştır.

### 2. Bağımsız Olarak Doğrulanan Sonuçlar
- **Top-1 Doğruluğu:** **%86,17** (68.558 yamada **59.076** doğru tahmin)
  - 95% yama düzeyi bootstrap güven aralığı: [%85,91, %86,44]
- **Makro-F1:** **0,6721**
  - 95% yama düzeyi bootstrap güven aralığı: [0,6557, 0,6876]
  - Geliştirme seti kıyaslaması (Val 50K): 0,6706 (Gözlemlenen fark: +0,0015)
- **Dengeli Doğruluk (Balanced Accuracy):** **%73,98**
- **En Zayıf Sınıf F1:** **0,4138** (Sulak alan: 0,4138; Çalı: 0,4238; Çıplak alan: 0,4140)

### 3. Bilimsel ve Operasyonel Sınırlar
1. **Model Statüsü:** Model, 10m Sentinel-2 RGB verisi üzerinde eğitilmiş deneysel bir araştırma prototipidir. Askeri operasyonel haritalama veya kadastro amaçlı sertifikalı bir ürün değildir.
2. **Coğrafi Değişkenlik:** Başarım Türkiye genelinde homojen değildir. İl bazlı Makro-F1 (mevcut sınıflar) Mersin'de 0,6467, Muğla'da 0,6190, Edirne'de 0,6119, Nevşehir'de 0,7692 olarak ölçülmüştür. Nadir sınıfların yerel örtüsü azaldığında tespit hassasiyeti düşmektedir.
3. **Önceden Eğitilmiş Başlangıç:** Model sıfırdan değil, ImageNet ağırlıkları ile ilklendirilmiş YOLO11n-cls omurgası üzerinden ince ayar (fine-tuning) ile eğitilmiştir.
4. **Dağıtım Yapılandırması:** Sistem yalnızca model ağırlıklarından (`best.pt`) ibaret değildir; dondurulmuş $\\tau = 0.50$ öncül kalibrasyon vektörü ve 128x128 ön işleme kuralları ile birlikte çalıştırılmalıdır.
