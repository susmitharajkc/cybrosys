#-*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import ValidationError
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.osv import expression


class WebsiteSaleBrand(WebsiteSale):
    @http.route([
        '''/shop/brand/<model("shop.brand"):brand>''',
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, brand=None, search='', ppg=False, **post):
        Brand = request.env['shop.brand']
        Category = request.env['product.public.category']
        print("category", Category)

        if brand:
            brand = Brand.search([('id', '=', int(brand))], limit=1)
            print("brand", brand)
        else:
            brand = Brand
        if brand:
            url = "/shop/brand/%s" % slug(brand)
        print(url)

        product_obj = request.env['product.template']
        Product = product_obj.sudo().search([('active', '=', True), ('website_published', '=', True),
                                             ('brand_name_cat', '=', brand.id)])
        print(Product)
        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4
        print(ppr)
        pager = request.website.pager(
            url="/shop/brand/%s" % slug(brand),
            total=len(Product),
            page=page,
            step=ppg
        )
        products = product_obj.sudo().search([('active', '=', True), ('brand_name_cat', '=', brand.id),
                                              ('website_published', '=', True)],
                                             order="id desc", limit=20, offset=pager['offset'])
        print(products)
        keep = QueryURL('shop/brand')
        values = {
            'pager': pager,
            'products': products,
            'bins': TableCompute().process(products, ppg, ppr),
            'rows': ppr,
            'keep': keep,
            # 'parent_category_ids': [],
        }
        print(values)
        # if brand:
        #     values['main_object'] = brand
        return request.render("website_sale.products", values)


#######################################################################################################################

class ShopByBrand(http.Controller):

    @http.route(['/shop-by-brand',
                 '/shop-by-brand/page/<int:page>',
                 ], type='http', auth='public', website=True, sitemap=True)
    def brands(self, page=0, search='', **post):
        Brand = request.env['shop.brand'].sudo().search([('shop_by_brand', '=', True)])


        domain = []

        if search:
            domain = [('brand_name', 'ilike', search)]

        total_brands = request.env['shop.brand'].search(domain)
        total_count = len(total_brands)
        per_page = 5

        pager = request.website.pager(url='/shop-by-brand', total=total_count, page=page,
                                     step=per_page, scope=3, url_args=None)
        brand_set = Brand.search(domain, limit=per_page, offset=pager['offset'], order='id asc')
        print('category', brand_set)



        groups = request.env['shop.brand'].sudo().search([])
        print("group", groups)


        if Brand:
            for brand in Brand:
                print(brand)
                keep = QueryURL('/shop', brand=brand and int(brand), search=search,
                                order=post.get('order'))

        else:
            keep = None

        values = {
            'category': brand_set,
            'pager': pager,
            'keep': keep,
            'groups': groups
            }
        print("values", values)
        return http.request.render('shop_by_brand.shop_by', values)

