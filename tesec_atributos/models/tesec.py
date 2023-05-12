# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models, tools


class Tesec(models.Model):
    _inherit = "project.project"

    @api.model
    def create(self, vals):
        self = super(Tesec, self).create(vals)
        #obras = self.env['project.project'].search([])
        obras = self.env['project.project'].with_context(active_test=False).search([])
        max_key = 0
        for obra in obras:
            try:
                key_int = int(obra.key)
                if key_int > max_key:
                    max_key = key_int
            except ValueError:
                pass

        print("el mayor numero es: "+str(max_key))
        print("Hay "+str(len(obras)))
        for obra in obras:
            print(obra.name+" - "+obra.key)
        #if(len(obras)<10):
        #    self.key = ''.join(("000",str(len(obras))))
        #if((len(obras)<100)and(len(obras)>=10)):
        #    self.key = ''.join(("00",str(len(obras))))
        #if((len(obras)<1000)and(len(obras)>=100)):
        #    self.key = ''.join(("0",str(len(obras))))
        #if((len(obras)<10000)and(len(obras)>=1000)):
        if((max_key+1)<10):
            self.key = ''.join(("000",str(max_key+1)))
        if((max_key+1) and (max_key+1)>=10):
            self.key = ''.join(("00",str(max_key+1)))
        if((max_key+1)<1000)and((max_key+1)>=100):
            self.key = ''.join(("0",str(max_key+1)))
        if((max_key+1)<10000)and((max_key+1)>=1000):
            self.key = str(max_key+1)
        return self