from odoo import models, fields, api


class ShopByBrand(models.Model):
    _name = 'shop.brand'
    _inherit = ['image.mixin']
    _rec_name = 'brand_name'

    brand_name = fields.Char(string="Brand Name", required=True)
    brand_description = fields.Char(string="Description")
    image_1920 = fields.Image(attachment=True,)
    shop_by_brand = fields.Boolean("Shop BY Brand")
    # product_ids = fields.Many2one('product.product', 'Products')


class InheritProduct(models.Model):
    _inherit = 'product.template'

    brand_name_cat = fields.Many2one('shop.brand', string="Brand Name")

