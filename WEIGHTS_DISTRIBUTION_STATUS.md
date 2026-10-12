# Model Weights Distribution Status & Open-Source Compliance Analysis

**Status:** PUBLISHED (*GNU AGPL-3.0 ve Apache-2.0 Birleşik Dağıtım Lisansı Kapsamında Yayımlandı*)  
**Revision:** `v2.0` · 12 October 2026  
**Checkpoint SHA-256:** `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a` (`model/best.pt`)

---

## 1. Bileşen Bazlı Lisans Taksonomisi

TurkeyLandCover V2 projesinde yer alan bileşenler farklı açık kaynak lisanslarına tabidir:

| Bileşen | Uygulanan Lisans | Hukuki Kapsam ve Uyumluluk |
| :--- | :--- | :--- |
| **Özgün Proje Kodu** (`inference/`, `tools/`, `training/`) | **Apache License 2.0** | Özgün geliştirilen kaynak kodun telif bildirimleri korunmuştur. Apache 2.0 lisansı, GNU AGPL-3.0 ile tek yönlü uyumludur (one-way compatible); özgün dosyaların lisans başlıkları değiştirilmeden AGPL-3.0 birleşik çalışması altında sunulabilir. |
| **Veri Manifestoları ve İstatistikler** (`metadata_and_splits/`) | **CC BY 4.0** | ESA WorldCover 2021 ve Copernicus Sentinel uydu verisi türevidir. Zorunlu atıf bildirimleri (`ATTRIBUTION.md`) korunmuştur. |
| **Model Ağırlıkları** (`model/best.pt`) | **GNU AGPL-3.0** | Ultralytics YOLO11n-cls mimarisi ve ön-eğitimli ağırlıklarının ince ayar (fine-tuning) çıktısıdır. Ultralytics'in copyleft şartları gereğince GNU AGPL-3.0 kapsamında dağıtılır. |
| **Birleşik Dağıtım Paketi (Combined Work)** | **GNU AGPL-3.0** | Ağırlıklar, kalibrasyon katmanı ve çalıştırma betiklerinin oluşturduğu birleşik eser bütünü GNU AGPL-3.0 altında conveyed edilmektedir. |

---

## 2. Hukuki ve Mühendislik Taleplerinin Üçlü Ayrımı

Hukuki zorunluluklar ile projenin kendi bilimsel tekrarlanabilirlik hedefleri birbirinden kesin olarak ayrılmıştır:

### A. GNU AGPL-3.0 Metnindeki Açık Yükümlülükler
1. **Madde 1 ("Corresponding Source"):** Nesne kodu biçimindeki bir eserin "İlgili Kaynak Kodu"; eseri oluşturmak, kurmak, çalıştırmak ve değiştirmek için gereken tüm kaynak kodları ve denetim betiklerini ifade eder. Kaynak kod insan tarafından okunabilir yazılım kodudur. **Özel eğitim veri setleri veya veri satır manifestoları AGPL-3.0 Madde 1 kapsamında "kaynak kod" olarak tanımlanmamıştır.**
2. **Madde 4 ve 5 ("Conveying Verbatim Copies & Modified Source Versions"):** Değiştirilen kaynak sürümlerinde belirgin telif ve değişiklik bildirimlerinin yer alması ve eserin bir bütün olarak lisanslanması zorunludur.
3. **Madde 6 ("Conveying Non-Source Forms"):** Model ağırlıkları gibi kaynak dışı nesne formlarının (object code/non-source forms) dağıtılması durumunda, alıcıya makine tarafından okunabilir "İlgili Kaynak Kod"un (Corresponding Source) AGPL-3.0 şartlarıyla ücretsiz sunulması zorunludur.
4. **Madde 13 ("Remote Network Interaction"):** Ağ üzerinden uzaktan etkileşime giren kullanıcılara da kaynak kodun sunulması imkânını düzenler.

### B. Ultralytics'in Resmî Uyumluluk Açıklamaları
- **Model Türevleri (Derivatives):** Ultralytics, kendi ön-eğitimli ağırlıklarından ince ayarlanan (fine-tuned) modelleri AGPL-3.0 copyleft kapsamında türev çalışma olarak değerlendirir.
- **Kaynak Kodun Açılması Zorunluluğu:** Modeli kullanan veya dağıtan tarafların eğitim betiklerini, model yapılandırmalarını ve uygulama kodlarını AGPL-3.0 altında açması VEYA ticari Enterprise lisansı satın alması gerekir.
- **Eğitim Verisi İstisnası (Data Exemption):** Ultralytics'in resmî dokümantasyon ve SSS bildirimlerine göre, **kullanıcıların kendi özel eğitim veri setlerini AGPL-3.0 kapsamında kamuya açma zorunluluğu YOKTUR.** Copyleft yükümlülüğü yazılım koduna ve model ağırlığına bağlanmıştır; görüntü verilerine bağlanmamıştır.

### C. Projenin Kendi Bilimsel Tekrarlanabilirlik Tercihleri (Engineering Provenance)
- **40.253 Satırlık İç Eğitim Manifestosu:** EVREN sunucusunda 50.000 yama havuzundan iç eğitime giren 40.253 satırlık yama listesi, projenin bilimsel şeffaflık ve adli veri soykütüğü (provenance) tercihidir. Bu liste yerel depoda bulunmadığından durumu **`UNKNOWN`** olarak belgelenmiştir. **Bu eksiklik AGPL-3.0 Madde 6'nın veya Ultralytics lisansının açık bir engeli DEĞİLDİR.**
- **Başlangıç Ağırlığı SHA-256 Hash'i:** Checkpoint üstverisinde yer alan `/mnt/evren_data/cache/ultralytics/yolo11n-cls.pt` başlangıç dosyasının geçmişteki kesin hash'i yerel depoda kayıtlı değildir (**`UNKNOWN`**). Bugün indirilen güncel dosyanın hash'i geçmişteki dosyanın hash'i yerine konamaz. Bu durum bilimsel soykütük sınırlılığıdır; AGPL-3.0 Madde 6 şartı değildir.

---

## 3. Lisans Kapsamı ve Birleşik Dağıtım Şartları

Sadece ağırlık dosyasının yanına AGPL metni koymak tam uyum sağlamaz. Tam uyum için:
1. **Gerçek V2 Eğitim Yöntemi ve İlgili Kaynak Kod (Corresponding Source):** 
   - **Gerçek Yöntem:** Model, veri düzeyinde dengeleme (`v2-balanced-train-50k`, 50.000 havuz) + EVREN kümesinde çalışan standart (stock) Ultralytics `ClassificationTrainer` (Cross-Entropy kaybı) ile eğitilmiş; çıkarımda ise donmuş $\tau=0,50$ Bayesian prior-shift düzeltmesi uygulanmıştır.
   - **Eğitim Başlatıcısı (Client Launcher):** `training/run_exp_v2_balanced_50k.py` EVREN eğitim API'sine iş yükünü ileten ve parametreleri denetleyen istemci betiğidir.
   - **Sunucuda Çalışan Trainer:** Upstream stock Ultralytics `ClassificationTrainer` sınıfıdır.
   - **Tarihsel Deney Kodu:** `training/v2_training_pipeline.py` dosyasındaki Focal Loss ve WeightedRandomSampler tasarımı V2 modelinde uygulanmamış, terk edilmiş hipotez kodudur; arşivsel şeffaflık için saklanmaktadır.
   - **Çıkarım ve Ön İşleme:** `inference/predict.py` ve hiperparametre dökümü (`checkpoint_embedded_metadata.json`) eksiksiz olarak depoda yer almaktadır.
2. **Framework Sürüm Sabitlemesi:** Model Ultralytics `8.3.0` sürümü ile eğitilmiştir. Upstream kaynak bağlantısı: [`https://github.com/ultralytics/ultralytics/tree/v8.3.0`](https://github.com/ultralytics/ultralytics/tree/v8.3.0).
3. **Donmuş Kalibrasyon:** Model tek başına çıplak ağırlık değil; sabit $\tau=0,50$ prior-shift düzeltmesi ve öncül vektörleri (`config/calibration_config.json`) ile birlikte çalışan bir sistemdir.
4. **Apache-2.0 Bildirimleri:** Özgün depodaki Apache-2.0 lisans bildirimleri korunmuştur. Birleşik çalışma AGPL-3.0 altında dağıtılırken özgün dosyalar Apache-2.0 niteliğini korur.
5. **Atıflar ve Bildirimler:** ESA WorldCover (CC BY 4.0), Copernicus Sentinel (AB Hukuki Bildirimi), Natural Earth (Public Domain) ve Ultralytics atıfları `ATTRIBUTION.md` dosyasında belgelenmiştir.

---

## 4. EVREN Platform Dağıtım Koşulları

- **Kullanıcı Sözleşmesi Madde 4.7 & 4.8:** Kullanıcı, platforma yüklediği içerikler üzerinde gerekli kullanım haklarına sahip olduğunu ve üçüncü taraf haklarını ihlal etmediğini beyan eder. Sentinel-2 ve ESA WorldCover verileri CC BY 4.0 kapsamında olduğundan bu şart sağlanmıştır.
- **Kullanıcı Sözleşmesi Madde 4.9 & 4.10:** Platform üzerinde oluşturulan model ve çıktıların EVREN tarafından dahili araştırma ve hizmet geliştirme amacıyla işlenebileceğini belirtir. Kullanıcının açık kaynaklı verilerle eğittiği modeli açık lisansla dışarıda paylaşmasını engelleyen bir madde bulunmamaktadır.
- **Katalog Kaydı Statüsü:** EVREN üzerindeki model katalog kaydı (`01a13136-5474-7d32-9161-8af7e6ba9a06`), araştırma prototipi (Research Release Candidate) olarak korunmaktadır. Canlı/çalışan bir model servisi veya API gibi tanıtılmamaktadır.

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
