odoo.define('point_of_sale.StockProduct', function (require) {
"use strict";

    var models = require('point_of_sale.models');
//    models.load_fields('stock.quant', ['inventory_quantity']);
//    console.log("this props",this.props);
//    models.load_fields('product.product', ['qty_available']);
//
//    console.log(models);
//    console.log("xxxxxxxxxxxx");
//    models.load_fields('product.product', ['type', 'qty_available', 'uom_name']);
//    console.log(this);

    models.load_fields('product.product', ['qty_available','uom_name']);
    console.log("hi",models)


//z
//
//    models.load_fields('product.product', ['qty_available']);
//
//
//    models.load_models([{
//    model:  product.product,
//    fields: qty_available,
//  }]);
//  console.log(this)

});
//
//    console.log(models);
//    console.log("xxxxxxxxxxxx");
//    models.load_fields('product.product', 'qty_available');
////
//    models.load_models({
//        model: 'product.product',
//        fields: ['qty_avaliable',],

//        loaded: function (self, invoices) {
//          var invoices_ids = _.pluck(invoices, 'id');
//          self.prepare_invoices_data(invoices);
//          self.invoices = invoices;
//          self.db.add_invoices(invoices);
//          self.get_invoice_lines(invoices_ids);
//      }
//});

