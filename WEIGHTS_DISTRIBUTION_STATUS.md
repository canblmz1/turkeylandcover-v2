# Model Weights Distribution Status & Licensing Evidence

**Status:** PUBLISHED — proje ağırlıklar/birleşik dağıtım için GNU AGPL-3.0 beyan ediyor; tüm haklar ve tam uyumluluk bağımsız doğrulanmış değildir.  
**Revision:** `v2.0` · 12 October 2026  
**Checkpoint SHA-256:** `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a` (`model/best.pt`)

---

## 1. Doğrulanan yayın ve lisans beyanları

- [v2.0](https://github.com/canblmz1/turkeylandcover-v2/releases/tag/v2.0), 12 Ekim 2026 tarihinde yayımlanmıştır. `best.pt` eki 3.201.787 bayttır; GitHub'ın bildirdiği SHA-256 yukarıdaki değerle eşleşir. Bu incelemede ikili dosya indirilip yeniden hash'lenmedi veya çalıştırılmadı.
- Etiket `7579554596ded1448d6643d6ea1d2f1e11aaa4fe` commit'ine işaret eder. Bu commit `model/best.pt`, `LICENSE_AGPL.txt`, kökte `ATTRIBUTION.md` ve eğitim kaynaklarını ekleyerek önceki ihtiyati alıkoyma durumunu değiştirmiştir.
- İncelenen main: `bc99e650668e68d01712f45d7833c1d654f06dff`. Sonraki bu commit eğitim yöntemi açıklamasını düzeltmiştir; v2.0 etiketi bu sonraki düzeltmeyi içermez.

| Bileşen | Depodaki beyan | Doğrulama sınırı |
| :--- | :--- | :--- |
| Veri materyali | `LICENSE`: CC BY 4.0 | Kaynak beyanıdır; tüm verilerin hak zinciri bu incelemede doğrulanmadı. |
| Kod | `LICENSE`: Apache-2.0 (`src/`, `scripts/`, `tests/`) | Yayın açıklaması özgün kod için Apache-2.0 der; `training/README.md` ise AGPL-3.0 beyan eder. `inference/`, `tools/`, `training/` ve belgelerin kesin kapsamı hak sahibi tarafından netleştirilmelidir. |
| Ağırlıklar ve birleşik dağıtım | v2.0 / yayın commit'i: GNU AGPL-3.0 | Mevcut proje beyanıdır; bağımsız hak veya tam uyumluluk onayı değildir. `LICENSE_AGPL.txt` mevcuttur. |

## 2. Açık kalan kanıtlar

- Checkpoint üstverisi `pretrained=true`, `ultralytics==8.3.0` ve önbellekteki `yolo11n-cls.pt` yolunu kaydeder. Tarihsel başlangıç dosyasının kimliği/hash'i ve ona uygulanan hakların eksiksiz kaydı doğrulanmış değildir. [Upstream v8.3.0 lisans metni](https://github.com/ultralytics/ultralytics/blob/v8.3.0/LICENSE) AGPL-3.0'dır; bu tek başına kullanılan tarihsel ağırlığın kimliğini kanıtlamaz.
- 40.253 öğelik iç eğitim manifestosu bilinmiyor. Bu bilimsel soykütük sınırlılığıdır; burada tek başına hukuki ihlal veya hukuki muafiyet sonucu çıkarılmaz.
- İlgili Kaynak Kodun (Corresponding Source) yeterliliği ve tüm bileşenlerin lisans kapsamı bu belge incelemesiyle kesinleştirilmemiştir. Önceki kesin uyumluluk, özel eğitim verisi muafiyeti ve zorunluluk yorumları doğrulanmış proje sonuçları olarak kullanılmamalıdır.
- `LICENSE` içindeki iki `legal/` yolu mevcut değildir; kökteki `ATTRIBUTION.md` bunlardan farklı bir dosyadır.

---

## 3. Kaynak ve yöntem kayıtları

Aşağıdaki kaynaklar depoda bulunur; varlıkları tam hukuki uyumluluk veya eksiksiz tarihsel eğitim kanıtı olarak yorumlanmamalıdır:
1. **Gerçek V2 Eğitim Yöntemi ve İlgili Kaynak Kod (Corresponding Source):** 
   - **Main'deki yöntem kaydı:** Proje kayıtlarına göre model, veri düzeyinde dengeleme (`v2-balanced-train-50k`, 50.000 havuz) + EVREN kümesinde çalışan standart (stock) Ultralytics `ClassificationTrainer` (Cross-Entropy kaybı) ile eğitilmiş; çıkarımda ise donmuş $\tau=0,50$ Bayesian prior-shift düzeltmesi uygulanmıştır.
   - **Eğitim Başlatıcısı (Client Launcher):** `training/run_exp_v2_balanced_50k.py` EVREN eğitim API'sine iş yükünü ileten ve parametreleri denetleyen istemci betiğidir.
   - **Sunucuda Çalışan Trainer:** Upstream stock Ultralytics `ClassificationTrainer` sınıfıdır.
   - **Tarihsel Deney Kodu:** `training/v2_training_pipeline.py` dosyasındaki Focal Loss ve WeightedRandomSampler tasarımı V2 modelinde uygulanmamış, terk edilmiş hipotez kodudur; arşivsel şeffaflık için saklanmaktadır.
   - **Çıkarım ve Ön İşleme:** `inference/predict.py` ve hiperparametre dökümü (`evidence/independent_audit/checkpoint_embedded_metadata.json`) depoda yer almaktadır.
2. **Framework Sürüm Sabitlemesi:** Checkpoint üstverisi Ultralytics `8.3.0` sürümünü kaydeder. Upstream kaynak bağlantısı: [`https://github.com/ultralytics/ultralytics/tree/v8.3.0`](https://github.com/ultralytics/ultralytics/tree/v8.3.0).
3. **Donmuş Kalibrasyon:** Model tek başına çıplak ağırlık değil; sabit $\tau=0,50$ prior-shift düzeltmesi ve öncül vektörleri (`config/calibration_config.json`) ile birlikte çalışan bir sistemdir.
4. **Apache-2.0 Bildirimleri:** Kök `LICENSE` korunmuştur; diğer dizinler için kesin kapsam ve çelişen kod beyanları henüz netleşmemiştir.
5. **Atıflar ve Bildirimler:** ESA WorldCover (CC BY 4.0), Copernicus Sentinel (AB Hukuki Bildirimi), Natural Earth (Public Domain) ve Ultralytics atıfları `ATTRIBUTION.md` dosyasında belgelenmiştir.

---

## 4. EVREN Platform Dağıtım Koşulları

EVREN sözleşmesinin uygulanabilir sürümü ve dış dağıtım iznini gösteren doğrulanmış kayıt bu incelemede elde edilmedi. Önceki 4.7–4.10 madde yorumları ve verilerin açık lisanslı olmasından tüm platform koşullarının sağlandığı sonucu doğrulanmış kabul edilmemelidir. Depoda katalog kimliği `01a13136-5474-7d32-9161-8af7e6ba9a06` bildirilir; güncel platform durumu veya kurumsal onay bu incelemede doğrulanmadı.

---

## 5. Doğrulama ve Çalıştırma

Model ağırlığı `model/best.pt` konumunda sağlanmaktadır:
- **Dosya Boyutu:** 3.201.787 bayt
- **SHA-256:** `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`

Doğrulama komutu:
```powershell
python tools/verify_release.py
```
Bu komut 68.558 mühürlü test örneğinin sayısal tahmin dizisini (`predictions/test_predictions.npz`) ve donmuş kalibrasyon metriklerini bağımsız olarak teyit eder.

## 6. Bu belge düzeltmesinin sürüme etkisi

Bu düzeltme yalnızca main için önerilen üç belgeyi günceller. v2.0 etiketi, yayın açıklaması, ek belgeler ve ZIP değiştirilmez; eski kopyalardaki çelişkiler sürer. Güncel değerlendirmede bu belge ve `LICENSE_NOTES.md` birlikte okunmalıdır. Bilimsel sonuçlar, model ve deney kayıtları değişmez. Mevcut hash manifestoları eski yayın anlık görüntülerine aittir; bu belge değişiklikleri için yeniden üretilmez.
