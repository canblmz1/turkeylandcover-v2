# TurkeyLandCover V2 — Bağımsız Denetim Çıktıları

Başlangıç dosyası: BAGIMSIZ_DENETIM_RAPORU.md

Bu paket orijinal kanıt ZIP'ini değiştirmeden gerçekleştirilen denetimin çıktısıdır.
Yeni eğitim, yeni görüntü çıkarımı veya testte tau araması yapılmadı.

Özet karar: Sayısal tutarlılık GEÇTİ. Eğitim kökeni ve train/test sızıntı kanıtları kısmen doğrulanabilir.
Yayın metadatasında pretrained=false/true farkı ve eski 422 sürüm kayıtları açıklanmalıdır.

Gereken Python paketleri: numpy, pandas. CUDA, torch veya ultralytics gerekmez.

Kaynak kanıt ZIP'i ayrı bir klasöre açıldıktan sonra:

python reproduce_audit.py <acilmis_kanit_klasoru> <ayri_denetim_klasoru>
python audit_checkpoint_metadata.py <acilmis_kanit_klasoru> <ayri_denetim_klasoru>
python audit_manifest_lineage.py <acilmis_kanit_klasoru> <ayri_denetim_klasoru>

RECORDED_EXECUTION_AND_INFERENCE.json sonradan kaydedilen yürütme metadatasıdır;
tarihsel donmuş konfigürasyonun veya yeni preregistration kaydının yerine geçmez.
