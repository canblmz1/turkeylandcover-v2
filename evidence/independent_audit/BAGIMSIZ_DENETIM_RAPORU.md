# TurkeyLandCover V2 — Bağımsız Kanıt Denetimi

**Tarih:** 12 Ekim 2026  
**Kapsam:** Yüklenen ZIP'in gerçek dosyalarından salt okunur, yerel yeniden hesaplama.  
**Karar:** **SAYISAL TUTARLILIK GEÇTİ. Eğitim kökeni ve tam eğitim/sızıntı denetimi KISMEN DOĞRULANABİLİYOR. Yayın metadatasında düzeltme gerekli.**

## 1. Gerçekten yapılan işlemler

Yüklenen `TurkeyLandCover_V2_Kanit_Paketi.zip` açıldı. İçindeki betikler çalıştırılmadı; bağımsız NumPy/pandas kodu yazıldı. NPZ dosyaları `allow_pickle=False` ile okundu. Checkpoint yalnızca ZIP içeriği ve pickle opcode'ları üzerinden, nesne yükleme veya kod çalıştırma olmadan incelendi. `torch.load`, model çıkarımı, eğitim, model güncellemesi ve EVREN çağrısı yapılmadı. Kaynak dosyalar değiştirilmedi.

Bu denetim **kayıtlı logit → donmuş düzeltme → tahmin → metrik** zincirini doğrular. Ham görüntüler olmadığından **görüntü → checkpoint → logit** zincirini yeniden çalıştırmaz. Hash eşleşmesi dosya bütünlüğünü gösterir; tek başına eğitim tarihçesini, etiket doğruluğunu veya testi geçmişte kaç kez kullandığınızı kanıtlamaz.

## 2. Arşiv ve dosya bütünlüğü — GEÇTİ

- ZIP boyutu: **8.438.657 bayt**.
- ZIP SHA-256: `694fd687c5b23e4573c76b66f4d726cb47c87cfafd8728537c27ec3d36669fb1`.
- Toplam arşiv girdisi: **30 dosya**.
- `SHA256SUMS.txt` içinde listelenen **29 dosyanın 29'u eşleşiyor**. Liste dosyası ayrıca ZIP'in 30. girdisi; kendi hash'ini içermiyor.
- `models/best.pt`: **3.201.787 bayt**, SHA-256 `8aa73d67dd65b315f825333f4ae9582827f553242ab104b11b0f410464c9ff5a`.
- Test NPZ SHA-256: `d5b63a61813f8ec9ea2d417e3c08ff4b90cf0973efd53b1503351520c9254c64`.

Kaynaklar: orijinal ZIP, `SHA256SUMS.txt`; bağımsız çıktı: `independent_audit_results.json / hash_verification`.

## 3. Final testin ham tahminlerden yeniden hesabı — GEÇTİ

| Ölçüt | Bağımsız hesap |
|---|---:|
| Kayıtlı test örneği | 68.558 |
| Benzersiz test örneği kimliği | 68.558 |
| Mükerrer kimlik | 0 |
| Doğru tahmin | 59.076 |
| Yanlış tahmin | 9.482 |
| Top-1 doğruluk | %86,169375 |
| Top-5 doğruluk | %99,985414 — 68.548 doğru |
| Macro-F1, sekiz sınıf | 0,672094391 |
| Balanced Accuracy, sekiz sınıf | %73,982644 |
| Weighted-F1 | 0,863542648 |
| En düşük sınıf F1 | 0,413793103 |

68.558 × 8 raw logit değerinin tamamı sonlu. Donmuş `tau=0.50`, `epsilon=1e-12` ve scriptteki tam sayı sınıf frekanslarıyla prior düzeltmesi yeniden hesaplandı. Yeniden oluşturulan `argmax` tahminleri ile kayıtlı `pred_idx` arasında **0 fark** var. Sınıf sırası hem NPZ hem checkpoint metadatasıyla uyumlu.

Ham tahminlerden oluşturulan karışıklık matrisi, hem kayıtlı CSV hem sonuç JSON'uyla **tamamen aynı**. Metrik farkları yalnızca en fazla yaklaşık 1e-16 kayan nokta yuvarlaması seviyesinde. Önceki sohbetin `59.074` sayısı yanlıştı; mevcut kanıt dosyaları **59.076** sayısını doğruluyor.

Kaynak: `predictions/test_predictions.npz`, `results/confusion_matrix_raw.csv`, `results/v2_final_test_results.json`; yöntem: `reproduce_audit.py`.

## 4. Stage 3 geliştirme sonucu da yeniden üretildi — GEÇTİ

50.000 geliştirme örneğinin logits dosyasından, yalnızca önceden tanımlı 0.00–1.00 aralığındaki 11 tau değeri yeniden hesaplandı. Bu **geliştirme artefaktı denetimidir**; final testte yeni tau denenmedi.

- Tau tablosunun tüm temel metrikleri kayıtlı JSON'la yaklaşık 1e-16 hassasiyetinde eşleşiyor.
- Önceden yazılmış seçim kuralı yeniden uygulandığında **tau=0.50** çıkıyor.
- Seçilen adayın geliştirme doğruluğu: **43.434 / 50.000 = %86,868**.
- Geliştirme toplu Macro-F1: **0,670587520**.
- İlde mevcut sınıflarla hesaplanan ortalama il Macro-F1: **0,681883816**.
- LOPO'nun 7 seçimi kayıtla eşleşiyor; 5 il için diğer 6 il tau=0.50 seçiyor. LOPO dışarıda bırakılan il F1 ortalaması **0,666514615**.

**Sınır:** NATURAL modelin checkpoint'i ve ham tahminleri pakette yok. `NATURAL=0.5901` karşılaştırması betikte referans sabit olarak bulunuyor; bu denetimde o ayrı modelin skorunu bağımsız yeniden üretmedim. BALANCED ve onun Stage 3 düzeltmesi, mevcut geliştirme logits'leri üzerinde doğrulanabildi.

## 5. Önceki il ortalaması eleştirisinin düzeltilmesi

Önceki sohbet yanıtındaki `0.6819 → 0.5443`, aynı metrik tanımlarını karşılaştırmıyordu. Geliştirme seçimi her ilde **yalnızca gerçek etiketi bulunan sınıfları**, ilk test tablosu ise **sekiz sınıfın tamamını** ortalamış.

| Aynı tanımla karşılaştırma | Geliştirme | Final test | Test − geliştirme |
|---|---:|---:|---:|
| Toplu Macro-F1, sekiz sınıf | 0,670588 | 0,672094 | +0,001507 |
| Ortalama il Macro-F1, ilde mevcut sınıflar | 0,681884 | 0,671503 | −0,010381 |
| Ortalama il Macro-F1, sekiz sınıf | 0,592506 | 0,544347 | −0,048159 |

Dolayısıyla önceki **−0,1376** düşüş yorumu geçersizdi. Dondurulmuş tau seçimindeki mevcut-sınıf tanımıyla düşüş yaklaşık **1,04 F1 yüzde puanı**. Sekiz-sınıf tanımıyla ayrıca yaklaşık **4,82 puan** düşüş var; onu gizlemek de doğru değil. Toplu skor tek başına bütün illerde ve sınıflarda eşit performans anlamına gelmiyor.

Kaynak: `scripts/run_stage3_prior_correction.py:116–142`, `scripts/evaluate_v2_final_test.py:99–168`, iki NPZ; çıktılar: `test_province_metrics_recomputed.csv`, `development_province_metrics_recomputed.csv`.

## 6. Validation manifestinin farklı hash'i açıklanabildi — GEÇTİ

Donmuş YAML'de validation CSV hash'i `2a8d29be49c6887094ec8c53f949fdec5b377ee5b11491a7b2884114f601749f`.
Paketlenen dosyanın hash'i `edf44566cd51c1263bd371f2a571867b7a039857bbee7079c87981d63c425ae5`.

**Salt bir uyuşmazlık bulmakla kalınmadı:** Paketlenen CSV'den yalnızca sonradan eklenen `canonical_class` sütunu çıkarılıp aynı CRLF biçimiyle bellekte yazılınca, eski donmuş hash **birebir yeniden elde edildi**. Bu, asıl sütunların tüm satır değerleri ve sıralamasının eski temsil ile aynı olduğunu; hash farkının etiket sütunu eklenmesiyle açıklanabildiğini gösteriyor.

Validation NPZ'nin 50.000 sample ID/il/etiket eşleşmesi mevcut manifestle tam uyumlu. Bu açıklama yayın paketine eklenmeli; eski manifest tarihçesi silinmemeli.

Kaynak/yeniden üretim: `audit_manifest_lineage.py`, `validation_manifest_lineage.json`.

## 7. Checkpoint içinden bulunan gerçek konfigürasyon farkı

Donmuş YAML'nin 12. satırında `pretrained: false` yazıyor. Checkpoint'in `train_args` verisi ise:

```text
pretrained = true
model = /mnt/evren_data/cache/ultralytics/yolo11n-cls.pt
data = /dev/shm/evren-01a12f84-8c82-7d92-8d15-05d042eea100
batch = 64
imgsz = 128
epochs = 10
optimizer = AdamW
lr0 = 0.001
lrf = 0.01
seed = 20261011
```

Checkpoint metadatasında sürüm **8.3.0**, sekiz beklenen sınıf adı ve **1–10 epoch eğitim sonuç kayıtları** var. Bunlar gerçek dosya içinde görüldü; bu, yeni bir EVREN sunucu sorgusu değildir.

**Sonuç:** Sıfırdan/rastgele başlatılarak eğitildiği iddiası bu dosyayla desteklenmiyor; kayıt önceden eğitilmiş ağırlık kullanımını belirtiyor. Bu farklılık mevcut tahminlerin matematiğini bozmaz. Ancak deneyin nasıl anlatılacağını ve NATURAL ile aynı başlangıcın kullanıldığı iddiasını etkiler. NATURAL checkpoint metadatası burada bulunmadığından eşit başlangıç doğrulanamadı.

**Düzeltme:** Tarihsel YAML'yi sessizce değiştirip yeni hash'i eski dondurma gibi göstermeyin. Ayrı bir düzeltme notunda planlanan `false` ile kayıtlı `true` farkını açıklayın. `RECORDED_EXECUTION_AND_INFERENCE.json` gerçek checkpoint metadatasını ve donmuş inference parametrelerini kaydediyor. Kaynak ağırlığın tam hash'i bu pakette yok.

## 8. Paketin eğitim kökeni sınırları

`metadata_and_splits/v2_evren_dataset_versions.json` içinde üç kayıt da `version_id: null`, `item_count: null`, `status_code: 422`. Bu dosya, başarıyla oluşturulmuş son sürüm kayıtlarının kanıtı değil; eski başarısız girişimin kaydı. Donmuş YAML'de dolu sürüm ID'leri bulunması bu dosyanın güncel olmadığıyla uyumlu, fakat canlı sunucu teyidi yerine geçmez.

Paket ayrıca gerçek NATURAL/BALANCED 50K eğitim manifestlerini, çözülmüş internal-train item listesini, NATURAL checkpoint'ini ve ayrı ham Slurm/EVREN iş loglarını içermiyor. `MISSING_FILES.txt` içindeki “eksik dosya yok” cümlesi, pakete dahil edilmesi hedeflenen liste açısından okunabilir; bütün eğitim geçmişinin bağımsız kanıtlandığı anlamına gelmez.

Test ve validation arasında sample ID ve il örtüşmesi **0** olarak yeniden hesaplandı. Eğitim illeri listesi split-summary'de var, fakat gerçek eğitim örnek listesi olmadan train/test örnek kesişimini bağımsız doğruladığımı söylemiyorum.

## 9. Etiket kaynağı, dışlanan örnekler ve test erişim sayısı

69.512 test manifest satırının **68.558'i** tahmin NPZ'sinde var; **954 satır** yok. Eksik örneklerin tamamı `excluded_test_manifest_rows.csv` içinde listelendi. Değerlendirme kodu bu eleme kararını `sample_id`'nin görüntü ZIP'inde bulunup bulunmamasına göre veriyor. Script, her eksik satırın gerçekten deniz/sınır/nodata olduğunu ayrıca kanıtlamıyor. Raporda “954 görüntüsü çözümlenemeyen manifest satırı” demek, yalnızca bu paketle desteklenebilir ifadedir.

Test manifestinde sınıf etiketi sütunu yok. NPZ'deki ground truth etiketleri sayısal olarak doğrulanabildi, ancak bağımsız kaynak rasterı/etiket üretim kaydı veya etiketli kaynak ZIP olmadan semantik etiket doğruluğu doğrulanmadı. Görüntülerin pakete konmaması önceki isteğe uygundu; bu bir yolsuzluk kanıtı değildir, denetimin sınırıdır.

“Test daha önce hiç kullanılmadı / tam bir kez çalıştırıldı” ifadesi raporlarda beyan ediliyor. Mevcut dosya ve hash'ler geçmişte başka işlem yapılmadığını tek başına kanıtlamaz. Bu denetimde ise **hiçbir yeni görüntü çıkarımı veya test parametresi denemesi yapılmadı**.

## 10. Güven aralıkları — yeniden üretildi, sınırı korunmalı

Mevcut tahminler üzerinde seed=20261012, B=1000 ile rapordaki resampling yeniden yapıldı. Kayıtlı aralıklarla fark yaklaşık 1e-16 düzeyinde:

| Ölçüt | %95 aralık |
|---|---:|
| Top-1 | %85,905292 – %86,443595 |
| Macro-F1 | 0,655683 – 0,687631 |
| Balanced Accuracy | %72,465394 – %75,659767 |

Script örnekleri tek tek, yerine koyarak çekiyor. Bu nedenle aralıklar **patch düzeyinde**; coğrafi blok/il resampling'i içermiyor. Türkiye'nin tüm coğrafyasına ilişkin belirsizlik olarak sunulmamalı. Bu denetimde yöntem değiştirilmedi ve yeni coğrafi güven aralığı üretilmedi.

## 11. Sonucun doğru okunması

Toplu testte sekiz sınıfın hepsinde en az bir doğru tahmin var. Bu “Türkiye'nin her yerinde kör sınıf kalmadı” anlamına gelmez. Örneğin Edirne alt kümesinde iki shrubland örneğinin ikisi de yanlış. Sınıf bazında built_up precision yaklaşık **%49,70**, bare/sparse precision **%30,96**, wetland recall **%35,82**. Bunlar modelin sınırlılıklarıdır; toplu doğrulukla gizlenmemeli.

Önerilen ifade:

> “TurkeyLandCover V2'nin saklı tahmin artefaktları bağımsız olarak yeniden hesaplandı. 68.558 değerlendirme örneğinde Top-1 %86,1694 ve sekiz-sınıf Macro-F1 0,672094 doğrulandı. Mevcut sınıflar üzerinden hesaplanan ortalama il Macro-F1, geliştirmede 0,681884 ve finalde 0,671503. İncelenen checkpoint önceden eğitilmiş YOLO11n-cls kullanımını kaydediyor. Eğitim örneği geçmişi, kaynak etiketler ve canlı platform kökeni bu paket üzerinden tamamen bağımsız doğrulanmış değil.”

Bu dosyalardan SOTA, foundation-model, askeri operasyonel hazırlık, kusursuz olasılık kalibrasyonu, tüm Türkiye için hatasızlık veya kesin kurumsal ilgi sonucu çıkarılmıyor.

## 12. Şimdiki karar ve işin sınırı

**Yeni eğitim gerekli değil. Skorları değiştirmek için tau/öncül/checkpoint aramayın.** Sayısal denetim işi tamamlandı; V2'nin mevcut geliştirmesini uzatma gerekçesi kalmadı.

Yayın paketi için kalan işler kayıt düzeltmesi ve eksik köken belgelerinin, elde mevcutsa, eklenmesidir: ön-eğitim sapmasını açıkça yazmak; eski 422 sürüm dosyasını güncel başarı kaydı diye sunmamak; validation etiket sütunu/hash soyunu belgelemek; asıl eğitim manifestleri ve NATURAL kayıtları bulunmuyorsa doğrulama sınırını açıkça yazmak. Bunlar sağlanmadan “uçtan uca tam tekrarlanabilir ve her eğitim/sızıntı kapısı bağımsız doğrulandı” denmemeli. Sınırlılıklarıyla birlikte araştırma prototipi ve bu sayısal denetimin sonuçları paylaşılabilir.

## 13. Dosyalar ve yeniden üretim

- `independent_audit_results.json`: bütün ham denetim sayıları, tau tablosu, iller, sınıflar, hash kontrolleri.
- `reproduce_audit.py`: NumPy/pandas ile yeni çıkarım olmadan metrik denetimi.
- `checkpoint_embedded_metadata.json`: çalıştırılmadan okunan checkpoint metadata.
- `audit_checkpoint_metadata.py`: güvenli, yalnızca primitive metadata opcode parser'ı.
- `validation_manifest_lineage.json`, `audit_manifest_lineage.py`: eski validation hash'inin birebir geri kurulması.
- `RECORDED_EXECUTION_AND_INFERENCE.json`: kayıtlı çalışma ve donmuş inference değerleri.
- `SOURCE_EVIDENCE_EXCERPTS.md`: ZIP dosyalarından satır numaralı dayanaklar.
- `*_recomputed.csv`: yeniden hesaplanan karışıklık matrisi, sınıf/il tabloları ve geliştirme tau tablosu.

Gerekli paketler: `numpy`, `pandas`. Ham resim, CUDA ve Ultralytics kurulumu gerekmez.

```text
python reproduce_audit.py <acilmis_kanit_klasoru> <ayri_denetim_klasoru>
python audit_checkpoint_metadata.py <acilmis_kanit_klasoru> <ayri_denetim_klasoru>
python audit_manifest_lineage.py <acilmis_kanit_klasoru> <ayri_denetim_klasoru>
```

Kaynak ZIP dosyası ve içindeki tarihsel raporlar değişmeden korunmuştur. Bu rapor yeni bir eğitim veya preregistration kaydı değildir.
