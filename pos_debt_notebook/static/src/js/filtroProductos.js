odoo.define('pos_debt_notebook.models', function(require) {
    'use strict';
    console.log("ENTRAMOOOOOS");
    var models = require('point_of_sale.models');
    var PosModelSuper = models.PosModel.prototype;
    
    models.PosModel = models.PosModel.extend({
      // Sobreescribe el método original para cargar el cliente y sus productos.
      set_client: function(client){
        PosModelSuper.set_client.call(this, client);  
         console.log("OLEEE");
        if(client){
         
          this.reload_products_for_client(client);
        }
      },
  
      // Carga los productos para un cliente específico.
      reload_products_for_client: function(client) {
        var self = this;
        
        // Aquí debes decidir cómo filtrar los productos basándote en el cliente.
        // Por ejemplo, podrías tener una lógica que filtre productos basándote en el nombre del cliente.
        var product_model = _.find(this.models, function(model) {
          return model.model === 'product.product';
        });
        
        if (product_model) {
          var _super_loaded = product_model.loaded;
          
          product_model.loaded = function (self, products) {
            var filtered_products = _.filter(products, function (product) {
              return product.display_name && product.display_name[0].toLowerCase() === client.name[0].toLowerCase();
            });
            
            _super_loaded(self, filtered_products);
          };
          
          // Recarga los productos.
          return this.load_new_products();
        }
      },
      
      // Este método recarga los productos del POS.
      load_new_products: function(){
        var self = this;
        var def  = new $.Deferred();
        var fields = _.find(this.models,function(model){ return model.model === 'product.product'; }).fields;
        var domain = [['sale_ok','=',true],['available_in_pos','=',true]];
        var context = this.session.user_context;
        
        this.fetch(
            'product.product',
            fields,
            domain,
            context
        ).then(function(products){
            self.db.add_products(_.map(products, function(product){
              product.categ = _.findWhere(self.product_categories, {'id': product.categ_id[0]});
              return new models.Product({}, product);
            }));
            def.resolve();
        }, function(type, err){ def.reject(); });
        return def;
      },
    });
  });