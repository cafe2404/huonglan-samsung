import requests
from django.core.management.base import BaseCommand
from products.models import ProductCategory, ProductFamily, ProductModel,ChipOption, ProductImage
from decimal import Decimal

SAMSUNG_API_URL = "https://searchapi.samsung.com/v6/front/epp/v2/product/finder/global"

class Command(BaseCommand):
    help = "Fetch product data from Samsung API and save to database"

    def handle(self, *args, **kwargs):
        site_code = "vn"
        company_code = "vn_doanhnghiepd"

        # Lấy danh sách type_code từ bảng ProductCategory
        categories = ProductCategory.objects.all()
        for category in categories:
            params = {
                "type": category.type_code,
                "siteCode": site_code,
                "start": 1,
                "num": 99999,
                "sort": "newest",
                "onlyFilterInfoYN": "N",
                "keySummaryYN": "Y",
                "companyCode": company_code,
                "pfType": "G",
            }
            response = requests.get(SAMSUNG_API_URL, params=params)
            data = response.json()
            result = data.get("response", {}).get("resultData", {})
            products = result.get("productList", [])
            
            for product in products:
                family, _ = ProductFamily.objects.update_or_create(
                    family_id=product.get("familyId", "UNKNOWN"),
                    defaults={
                        "category": category,
                        "family_record": int(product.get("familyRecord", 0)),
                        "marketing_name": product.get("fmyMarketingName", ""),
                        "eng_name": product.get("fmyEngName", ""),
                    }
                )
                for model in product.get("modelList", []):
                    product_model, created = ProductModel.objects.update_or_create(
                        model_code=model.get("modelCode", ""),
                        defaults={
                            "product_family": family,
                            "model_name": model.get("modelName", ""),
                            "display_name": model.get("displayName", ""),
                            "thumb_url": model.get("thumbUrl", ""),
                            "thumb_alt": model.get("thumbUrlAlt"),
                            "large_url": model.get("largeUrl", ""),
                            "pdp_url": model.get("pdpUrl", ""),
                            "price": int(model.get("price", 0)),
                            "promotion_price": int(model.get("promotionPrice", 0)) if model.get("promotionPrice") else 0,
                            "formatted_price_save" : model.get("formattedPriceSave", ""),
                            "ratings": Decimal(model.get("ratings")) if model.get("ratings") else 0.00 ,
                            "stock_status": model.get("stockStatusText", ""),
                            "review_count" : int(model.get("reviewCount")) if model.get("reviewCount") else 0,
                            "marketing_message": model.get("marketingMessage", ""),
                            "sales_text": model.get("salesText", ""),
                        }
                    )
                    gallery_images = model.get("galleryImage", []) if model.get("galleryImage") else []
                    gallery_image_alts = model.get("galleryImageAlt", [])
                    for i in range(len(gallery_images)):
                        ProductImage.objects.get_or_create(
                            image_url = gallery_images[i],
                            image_alt = gallery_image_alts[i],
                            product_model = product_model,
                        )
                        
                    for chip_option in model.get("fmyChipList", []):  
                        ChipOption.objects.update_or_create(
                            product_model=product_model,
                            chip_type=chip_option['fmyChipType'],  
                            chip_code=chip_option.get("fmyChipCode", ""),
                            defaults={
                                "chip_name": chip_option.get("fmyChipName", ""),
                                "chip_local_name": chip_option.get("fmyChipLocalName", ""),
                            }
                        )

            self.stdout.write(self.style.SUCCESS("✅ Fetched and saved Samsung products successfully!"))
