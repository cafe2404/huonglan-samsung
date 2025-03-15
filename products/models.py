from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    type_code = models.CharField(max_length=50, unique=True)
    thumb_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'product_categories'
        ordering = ['id']
        verbose_name = 'Danh mục sản phẩm'
        verbose_name_plural = 'Quản lý danh mục sản phẩm'
            
class ProductFamily(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    family_record = models.IntegerField()
    family_id = models.CharField(max_length=50, unique=True)
    marketing_name = models.CharField(max_length=255,verbose_name="Tên thương mại")
    eng_name = models.CharField(max_length=255)
    product_group_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.marketing_name
    class Meta:
        db_table = 'product_families'
        ordering = ['-created_at']
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Quản lý sản phẩm'
        
class ProductModel(models.Model):
    product_family = models.ForeignKey(ProductFamily, on_delete=models.CASCADE, related_name="models")
    model_code = models.CharField(max_length=50, unique=True,verbose_name="Mã SKU")
    model_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255,verbose_name="Tên sản phẩm")
    thumb_url = models.URLField(null=True, blank=True)
    thumb_alt = models.CharField(max_length=255, null=True, blank=True)
    large_url = models.URLField(null=True, blank=True)
    pdp_url = models.URLField(null=True, blank=True)
    ratings = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    review_count = models.IntegerField(default=0)
    stock_status = models.CharField(max_length=50, default="inStock",verbose_name="Trạng thái")
    price = models.IntegerField(default=0,verbose_name="Giá")
    promotion_price = models.IntegerField(null=True, blank=True,verbose_name="Giá khuyến mãi")
    formatted_price_save = models.CharField(max_length=255, null=True, blank=True)
    marketing_message = models.TextField(null=True, blank=True)
    sales_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.display_name} - {self.model_code}"
    class Meta:
        db_table = 'product_models'
        ordering = ['-created_at']
        verbose_name = 'Biến thể sản phẩm'
        verbose_name_plural = 'Quản lý biến thể sản phẩm'
        
class ChipOption(models.Model):
    product_model = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="chip_options")
    chip_type = models.CharField(max_length=50)
    chip_code = models.CharField(max_length=50)
    chip_name = models.CharField(max_length=255)
    chip_local_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.chip_local_name} ({self.chip_type})"
    class Meta:
        db_table = 'chip_options'
        ordering = ['-created_at']
        verbose_name = 'Chip option'
        verbose_name_plural = 'Chip option'
        
class ProductImage(models.Model):
    product_model = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField()
    image_alt = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.image_url
    class Meta:
        db_table = 'product_images'
        ordering = ['-created_at']
        verbose_name = 'Hình ảnh biến thể'
        verbose_name_plural = 'Hình ảnh biến thể'