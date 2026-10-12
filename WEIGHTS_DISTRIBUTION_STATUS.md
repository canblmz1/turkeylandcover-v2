# Model Weights Distribution Status & Open-Source Compliance Analysis

**Status:** WITHHELD OUT OF CAUTION (*İhtiyaten Dağıtımdan Alıkonuldu — Dağıtımı Hukuken Yasak Değildir*)  
**Revision:** `v2.0-rc2-docfix` · 12 October 2026

---

## 1. Bileşen Bazlı Lisans Taksonomisi

TurkeyLandCover V2 projesinde yer alan farklı bileşenler farklı açık kaynak lisanslarına tabidir:

| Bileşen | Uygulanan Lisans | Açıklama ve Uyumluluk |
| :--- | :--- | :--- |
| **Proje Kodu** (`inference/`, `tools/`, `scripts/`) | **Apache License 2.0** | Mevcut kod lisansı korunmuştur. Apache 2.0 lisansı, AGPL-3.0 ile tek yönlü uyumludur (one-way compatible); kodun kendi telif bildirimleri değiştirilmeden AGPL-3.0 birleşik çalışmalarda dağıtılabilir. |
| **Veri Manifestoları ve İstatistikler** (`metadata_and_splits/`) | **CC BY 4.0** | ESA WorldCover 2021 ve Copernicus Sentinel uydu verisi türevidir. Zorunlu atıf bildirimleri korunmuştur. |
| **Model Ağırlıkları** (`model/best.pt`) | **GNU AGPL-3.0** | Checkpoint, Ultralytics YOLO11n-cls mimarisi ve ön-eğitimli ağırlıklarının ince ayar (fine-tuning) çıktısıdır. Ultralytics'in açık kaynak lisansı AGPL-3.0 copyleft hükümlerine tabidir. |

---

## 2. "Dağıtımı Yasak" ile "İhtiyaten Alıkonuluyor" Ayrımı

Bu ayrım hukuki ve teknik açıdan kritiktir:

- **Dağıtımı Hukuken Yasak DEĞİLDİR:**  
  Ultralytics'in ticari kurumsal lisansı zorunlu bir engel teşkil etmez; Ultralytics modelleri ve türev ağırlıkları **GNU AGPL-3.0 kapsamında ücretsiz ve açık kaynak olarak yasal biçimde dağıtılabilir**.
- **İHTİYATEN Alıkonulmaktadır (Precautionary Withholding):**  
  Ağırlık dosyasının (`best.pt`) AGPL-3.0 şartlarına tam uyumlu biçimde dağıtılabilmesi için gereken teknik ve yasal koşullar yerel kanıt paketinde henüz eksiksiz karşılanmamıştır. Telif ihlali veya eksik kaynak bildirimine mahal vermemek adına ağırlıklar **ihtiyaten** kamuya açık depodan alıkonulmuştur.

---

## 3. Ücretsiz AGPL-3.0 Kapsamında Dağıtım İçin Karşılanması Gereken Somut Koşullar

AGPL-3.0 Madde 6 ("Corresponding Source") uyarınca, ağırlıkların ücretsiz olarak dağıtılabilmesi için alıcıya aşağıdaki unsurların eksiksiz sunulması zorunludur:

1. **Eksiksiz İlgili Kaynak Kod (Corresponding Source):**
   Modeli bu ağırlıklara getiren tam eğitim kodu, veri ön işleme adımları ve çalıştırma betikleri eksiksiz olarak sunulmalıdır.
2. **Eğitim Verisi Manifestosu:**
   EVREN üzerinde eğitilen 50.000 yama havuzundan iç eğitime giren **40.253 yamanın tam kimlik/dosya listesi** bağımsız olarak doğrulanabilir olmalıdır.
3. **Başlangıç Ağırlığı Provenansı (Upstream Provenance):**
   Checkpoint üstverisinde `/mnt/evren_data/cache/ultralytics/yolo11n-cls.pt` yolu kayıtlıdır. Ancak bu başlangıç dosyasının kesin SHA-256 hash'i ve ImageNet sürüm kimliği yerel kanıtlarda bulunmamaktadır. Kaynak ağırlığın kesin kimliği kanıtlanmadan "ImageNet kökeni bağımsız doğrulandı" denilemez.
4. **Çift Lisans ve Bildirim Açıklığı:**
   Deponun kök Apache-2.0 lisansı sessizce değiştirilmemeli; ancak ağırlık dosyasının AGPL-3.0 altında paylaşıldığı, Ultralytics telif bildirimleri ve AGPL-3.0 lisans metni açıkça eklenmelidir.

---

## 4. Ağırlık Paylaşımı İçin Kalan SOMUT Eksikler

Ağırlıkların AGPL-3.0 kapsamında kamuya açılabilmesi için tamamlanması gereken somut adımlar:

1. [ ] **Eğitim Havuzu Manifestosu:** İç eğitime dahil olan 40.253 yamanın kesin satır listesinin yerel depoya eklenmesi (şu anda yalnızca test ve doğrulama manifestoları tamdır).
2. [ ] **Başlangıç Ağırlığı Doğrulaması:** Ultralytics `yolo11n-cls.pt` başlangıç dosyasının resmî sürüm/hash eşleşmesinin kayıt altına alınması.
3. [ ] **AGPL-3.0 Bildirim Dosyası:** Ağırlıkların dağıtım lisansı olarak `LICENSE_AGPL.txt` dosyasının eklenmesi ve Apache-2.0 kod bildirimleriyle olan sınırının netleştirilmesi.

---

## 5. Mevcut Durumda Çalıştırma

Ağırlık dosyasına (`best.pt`, SHA-256: `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`) sahip araştırmacılar:
- Dosyayı `model/best.pt` konumuna yerleştirerek `inference/predict.py` veya `inference/example_usage.py` üzerinden tam Bayesian kalibrasyonlu sistemi çalıştırabilir.
- Ağırlık dosyası olmadan da `tools/verify_release.py` aracıyla tüm 68.558 mühürlü test örneğinin sayısal tahmin dizisini (`predictions/test_predictions.npz`) ve metriklerini bağımsız olarak doğrulayabilir.
