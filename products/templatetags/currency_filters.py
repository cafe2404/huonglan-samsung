from django import template

register = template.Library()

@register.filter
def format_currency(value):
    try:
        value = int(value)
        return f"{value:,.0f} VND".replace(",", ".")
    except (ValueError, TypeError):
        return "Chưa có giá"
