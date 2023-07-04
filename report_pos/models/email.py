from odoo import _, api, exceptions, fields, models
import base64


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def has_attribute(self, attribute):
        return hasattr(self, attribute)

    def button_send_email(self):
        self.ensure_one()

        # Genera el informe PDF
        report = self.env.ref('report_pos.pos_order_report')
        pdf = report._render_qweb_pdf(self.id)

        # Crea un nuevo adjunto con el PDF
        attachment = self.env['ir.attachment'].create({
            'name': 'pedido.pdf',
            'type': 'binary',
            'datas': base64.b64encode(pdf[0]),
            'res_model': 'pos.order',
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })

        # Abre el asistente para enviar correo con el adjunto
        compose_form = self.env.ref('mail.email_compose_message_wizard_form')
        compose = self.env['mail.compose.message'].create({
            'composition_mode': 'comment',
            'res_id': self.id,
            'model': 'pos.order',
            'template_id': False,
            'no_auto_thread': False,
            'attachment_ids': [(4, attachment.id)]
        })
        return {
            'name': 'Enviar correo',
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'res_id': compose.id,
            'view_mode': 'form',
            'view_id': compose_form.id,
            'target': 'new',
        }
