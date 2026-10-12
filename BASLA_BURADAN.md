# TurkeyLandCover V2 — buradan başla

**Bu dosya aynı V2 modelinin düzeltilmiş yayın adayıdır. Yeni eğitim değildir.**

## Ne yapıldı?

Yayın metinleri denetimle eşleştirildi. Model, τ=0,50, prior vektörleri, eski dondurma dosyaları, çıkarım kodu ve mevcut tahminler değiştirilmedi. Eski yazıların değiştirilen kopyaları `history/rc1/` içinde durur.

## Bilgisayarında kullanım

Bu ZIP'i eski proje klasörünün üzerine açma; ayrı bir klasöre çıkar. Önce `README.md`, sonra `MODEL_CARD.md` dosyasını oku. Türkçe teknik tanıtım metni `SSB_EVREN_TEKNIK_NOT.md` içindedir.

İsteğe bağlı dosya kontrolü, açtığın klasördeki terminalde:

```text
python tools/verify_release.py --hashes-only
```

Mevcut Python ortamında NumPy varsa, kaydedilmiş tahminlerin sayısal kontrolü:

```text
python tools/verify_release.py
```

Bu komutlar model eğitmez, model ağırlığını açmaz, yeni görüntü tahmini üretmez, internet veya kredi kullanmaz. Kurulu ortamı değiştirmene gerek yok; NumPy yoksa hash kontrolüyle yetinebilirsin.

## Sonuç ne?

68.558 kayıtlı örnek, 59.076 doğru tahmin, %86,1694 doğruluk ve 0,672094 Macro-F1. Doğrulanan bölüm kayıtlı tahminlerin matematiğidir; bütün eğitim geçmişi ve görüntüden yeni çıkarım bağımsız olarak doğrulanmış değildir.

## Yayın durumu
 
Bu sürüm denetlenmiş araştırma yayın adayıdır (`v2.0-rc2-docfix`). Model ağırlıkları (`best.pt`), üst lisans netleştirilinceye dek kamuya açık dağıtımdan alıkonulmuştur (bkz. `WEIGHTS_DISTRIBUTION_STATUS.md`). Kod (Apache 2.0), dondurulmuş kalibrasyon yapılandırması, test manifestleri (CC BY 4.0), bağımsız denetim kanıtları ve 68.558 örneğin kayıtlı tahmin dizisi (`predictions/test_predictions.npz`) eksiksiz olarak kamuya açıktır. Tüm paketi MIT lisanslı diye sunma.
 
Yeni araştırma veya eğitim açılması gerekmiyor. Sayısal zincir (kayıtlı logit → donmuş düzeltme → tahmin → metrik) bağımsız olarak doğrulanabilir durumdadır.
