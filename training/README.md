# TurkeyLandCover V2 — Eğitim Metodolojisi ve Kaynak Belgeleri

Bu dizin, yayımlanan `best.pt` model ağırlıklarının (SHA-256: `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`) eğitim metodolojisini ve ilgili kaynak kodlarını (Corresponding Source) belgeler.

---

## 1. Gerçek V2 Eğitim Yöntemi (Fiilen Uygulanan Yöntem)

Yayımlanan final checkpoint'i üreten gerçek TurkeyLandCover V2 yöntemi üç aşamadan oluşur:

1. **Veri Düzeyinde Sınıf Dengelemesi (Data-Level Balancing):**
   - Türkiye genelinden toplanan 50.000 yamalık dengeli havuz (`v2-balanced-train-50k`, EVREN Veri Sürümü: `01a12cb1-05c8-7c80-b321-2c51ae68b55a`).
   - Sınıf dengesizliği eğitim öncesinde veri seçim katmanında dengelenmiştir.
2. **EVREN Standart Stock Classification Trainer (Server-Side Execution):**
   - Eğitim, EVREN GPU kümesinde standart (stock) Ultralytics `ClassificationTrainer` motoru ile yürütülmüştür.
   - Özel bir kayıp fonksiyonu veya özel sampler **kullanılmamıştır**; standart unweighted Cross-Entropy kaybı ve standart DataLoader kullanılmıştır.
   - Mimarisi: Ultralytics YOLO11n-cls (`ultralytics==8.3.0`).
   - Hiperparametreler: 10 epoch, batch size 64, görüntü boyutu 128×128, AdamW optimizer, lr0=0.001, seed=20261011.
3. **Eğitim Sonrası Donmuş Prior Düzeltmesi (Post-Training Prior Adjustment):**
   - Model çıkarımında, dengelenmiş eğitim öncül dağılımı ile hedef Türkiye arazi öncül dağılımı arasındaki kaymayı telafi etmek amacıyla sabit Bayesian logit kalibrasyonu uygulanır ($\tau=0,50$).
   - Formül: $\text{corrected\_logits} = \text{raw\_logits} + 0,50 \times (\log(p_{\text{target}}) - \log(p_{\text{train\_balanced}}))$.
   - Bu adım `config/calibration_config.json` ve `inference/predict.py` içinde dondurulmuştur.

---

## 2. Eğitim Başlatıcısı (Client Launcher) ve Sunucu Trainer'ı Ayrımı

Eğitim sürecinde iki farklı bileşen bulunmaktadır:

- **Eğitim Başlatıcısı (`run_exp_v2_balanced_50k.py`):**
  - İstemci tarafında çalışan otomasyon betiğidir.
  - Hiperparametreleri yapılandırır, EVREN eğitim API'sine (`POST /training/jobs`) iş yükünü iletir, pre-epoch doğrulama kapısını (50.000 yama, 1 GPU, veri sürümü kimliği) kontrol eder ve tamamlanan `best.pt` ağırlıklarını sunucudan indirir.
- **Sunucuda Çalışan Trainer (Server-Side Stock Engine):**
  - EVREN kümesinde doğrudan upstream Ultralytics kütüphanesinin standart `ClassificationTrainer` sınıfı (`ultralytics.models.yolo.classify.train.ClassificationTrainer`) tarafından çalıştırılmıştır.
  - Sürüme sabitlenmiş upstream kaynak kodu: [`https://github.com/ultralytics/ultralytics/tree/v8.3.0`](https://github.com/ultralytics/ultralytics/tree/v8.3.0).

---

## 3. Tarihsel ve Uygulanmamış Deney Kodu: `v2_training_pipeline.py`

- **Durumu:** **`TARİHSEL / UYGULANMAMIŞ DENEY KODU` (Abandoned / Unapplied Design)**
- **Açıklama:** Bu dosya, V2 geliştirme aşamasında hipotez olarak tasarlanan (EXP-V2-E) ancak **uygulanmayan** `MulticlassFocalLoss` ($\gamma=1.5$) ve `WeightedRandomSampler` kodlarını içerir.
- **Uyarı:** Yayımlanan `best.pt` ağırlıkları bu dosya ile **eğitilmemiştir**. Model, yukarıda açıklandığı üzere veri düzeyinde dengeleme + standart Cross-Entropy ile eğitilmiştir. Bu dosya yalnızca araştırma geçmişi ve soykütük şeffaflığı amacıyla korunmaktadır.

---

## 4. Eğitim Havuzu ve Soykütük Bilgisi

- **Staged Havuz:** EVREN üzerinde 50.000 öğe (`Direct-to-SHM`).
- **Raporlanan İç Eğitim Maruziyeti:** Sunucu loglarında 40.253 yama bildirilmiştir.
- **Eğitim Manifestosu:** `UNKNOWN` (iç eğitime giren 40.253 satırlık alt küme listesi sunucu veritabanından dışa aktarılmamıştır; AGPL-3.0 Madde 6 kapsamında zorunlu bir kaynak kod şartı değildir).
- **Başlangıç Ağırlığı:** Checkpoint üstverisinde `/mnt/evren_data/cache/ultralytics/yolo11n-cls.pt` kayıtlıdır; tarihsel hash'i `UNKNOWN` olarak belgelenmiştir.
