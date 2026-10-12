# TurkeyLandCover V2 — Teknik bilgi notu

**Tarih:** 12 Ekim 2026 · **Yayın adayı:** v2.0-rc2-docfix  
**Durum:** Araştırma prototipi; kayıtlı tahminlerin sayısal tutarlılığı doğrulanmış, eğitim kökeni kısmen doğrulanabilir.

## Çalışmanın amacı

Türkiye için Sentinel-2 RGB görüntü yamalarını sekiz arazi örtüsü sınıfına ayıran YOLO11n-cls tabanlı bir prototip geliştirilmiştir. Proje kayıtları, EVREN altyapısında veri düzeyinde sınıf dengelemesi ve sonrasında sabit bir öncül-dağılım düzeltmesi (τ=0,50) kullanıldığını bildirir. Bu bilgi notu kurum onayı, tedarik uygunluğu veya operasyonel hazırlık iddiası değildir.

## Doğrulanan sonuç

Artvin, Edirne, Mersin, Kars, Mardin, Muğla ve Nevşehir olarak işaretlenmiş **68.558** benzersiz kayıtlı test örneğinde:

| Ölçüt | Sonuç |
|---|---:|
| Doğru tahmin | 59.076 / 68.558 |
| Top-1 doğruluk | %86,1694 |
| Sekiz sınıflı Macro-F1 | 0,672094 |
| Dengeli doğruluk | %73,9826 |
| En düşük sınıf F1 | 0,413793 |

Bağımsız kontrol **kayıtlı logit → donmuş düzeltme → tahmin → metrik** zincirini yeniden hesaplamıştır. Ham görüntülerden model çıktısı yeniden üretilmemiş; kaynak etiketlerin doğruluğu bu denetimde doğrulanmamıştır.

Geliştirme/final toplu Macro-F1 değerleri 0,670588 / 0,672094'tür. İlde mevcut sınıfları esas alan ortalama il Macro-F1 değerleri 0,681884 / 0,671503'tür. Yama düzeyindeki %95 Macro-F1 güven aralığı [0,655683; 0,687631], B=1.000 ve seed=20261012 ile hesaplanmıştır; mekânsal kümelenme için düzeltilmiş değildir.

## Eğitim ve dağıtım bilgisi

Checkpoint kaydı `pretrained=true` göstermektedir; rastgele başlangıçtan eğitim iddiası kullanılmamaktadır. İlk kaynak ağırlığın tam kimliği doğrulanmamıştır. Proje kayıtlarına göre 50.000 öğelik seçilmiş havuzun **40.253** öğesi gerçek iç eğitim bölmesindedir; sunucu kayıtları ve eğitim örnek listeleri bağımsız denetim için eksiktir.

Final sistem `best.pt`, τ=0,50, kesin prior vektörleri, sınıf sırası ve 128×128 ön işleme birlikte korunarak tanımlanır. Bu yayın düzeltmesinde yeni eğitim, yeni görüntü çıkarımı veya ücretli hizmet kullanılmamıştır.

## Sınırlılıklar ve değerlendirme kapsamı

Model yama sınıflandırması yapar; piksel bazlı haritalama, zaman içinde değişim tespiti veya askeri/kadastral karar sistemi değildir. Test manifestindeki 954 satırın görüntüsü çözümlenememiştir; tek tek eksiklik nedenleri kanıtlanmamıştır. İller ve sınıflar arasında başarım farklıdır. Örneğin çıplak/seyrek arazi precision değeri yaklaşık %30,96, yapılaşmış alan precision değeri %49,70'tir.

Eğitim kökeni, asıl kaynak etiketler, canlı EVREN kayıtları, çıkarım paketinin uçtan uca çalışması ve ağırlıkların paylaşım hakları bu paket üzerinden tamamen doğrulanmış değildir. Teknik görüşme için uygun konu, prototipin sonuç ve sınırlarının incelenmesi; doğrulanmamış operasyonel kabiliyetler değildir.

**Ekler:** MODEL_CARD.md, REPRODUCIBILITY.md, doğrulanmış sonuç tabloları, kayıtlı tahminler ve bağımsız denetim çıktıları. Bu bilgi notu herhangi bir kuruma gönderilmemiştir.
