# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
import operator

class inher_user(models.Model):
	_inherit = "res.users"

	menu_ids = fields.Many2many('ir.ui.menu',string="Display Name")

class inher_menus(models.Model):
	_inherit = 'ir.ui.menu'

	hide_for_user =fields.Many2many('res.users',string="User Name")
	group_name = fields.Many2many('res.groups',sting="Group Name")


	@api.model
	@api.returns('self')
	def get_user_parent_roots(self):
		user_list =[]
		main = self.search([])
		for i in main:
			for h_user in i.hide_for_user:
				user_list.append(h_user.id)
		return user_list

	@api.model
	@api.returns('self')
	def get_user_group(self):
		group_list =[]
		menus = self.search([])
		for i in menus:
			for groups in i.group_name:
				group_list.append(groups)
		return group_list

	@api.model
	@tools.ormcache_context('self._uid', 'debug', keys=('lang',))
	def load_menus(self, debug):

		main_list = []
		lat_list = []
		menu_sub_roots = []

		users = self.env.user

		grp_list_1 = []
		grp_list_main = []
		grp_f_list = []
		xml_list = []


		fields = ['name', 'sequence', 'parent_id', 'action', 'web_icon', 'web_icon_data']

		menu_roots = self.get_user_roots()
		menu_roots_ids = self.get_user_roots()

		groups_menu = self.get_user_group()
		for g_sub in groups_menu:
			grp_list_1.append(g_sub)
			xml_names = g_sub._get_xml_ids().get(g_sub.id)
			xml_list.append(xml_names)

		groups = self.env.user.groups_id
		for g_main in groups:
			grp_list_main.append(g_main)

		for i in menu_roots_ids:
			main_list.append(i.id)

		menu_ro = self.get_user_parent_roots()

		if self.env.user.has_group('user_menu_hide_show_app.user_menu_hide_show_group'):
			if menu_ro:
				if self._uid in menu_ro:
					for i in menu_ro:
						for menus in menu_roots:
							for menu_us in menus.hide_for_user:
								if menu_us.id == i:
									lat_list.append(menus.id)
								
		if groups_menu:
			for m in menu_roots_ids:
				for m_groups in m.group_name:
					xml_names = m_groups._get_xml_ids().get(m_groups.id)
					for names in xml_names:
						if self.env.user.has_group(names):
							grp_f_list.append(m.id)

		if self.env.user.has_group('user_menu_hide_show_app.user_menu_hide_show_group'):
			merg_lst = lat_list + grp_f_list
			com_list = list(set(merg_lst))
			menu_sub_roots = set(main_list) - set(com_list)
			menu_roots = self.search([('id','in', list(menu_sub_roots)),('parent_id', '=', False)])

		if users.menu_ids:
			for menus in users.menu_ids:
				lat_list.append(menus.id)
				menu_sub_roots = set(main_list) - set(lat_list)
			menu_roots = self.search([('id','in', list(menu_sub_roots)),('parent_id', '=', False)])
		
		menu_roots_data = menu_roots.read(fields) if menu_roots else []
		menu_root = {
			'id': False,
			'name': 'root',
			'parent_id': [-1, ''],
			'children': menu_roots_data,
			'all_menu_ids': menu_roots.ids,
		}

		if not menu_roots:
			return menu_root

		menus = self.search([('id', 'child_of', menu_roots.ids)])
		menu_items = menus.read(fields)
		
		menu_items.extend(menu_roots_data)
		menu_root['all_menu_ids'] = menus.ids
		
		menu_items_map = {menu_item["id"]: menu_item for menu_item in menu_items}
		for menu_item in menu_items:
			parent = menu_item['parent_id'] and menu_item['parent_id'][0]
			if parent in menu_items_map:
				menu_items_map[parent].setdefault(
					'children', []).append(menu_item)

		for menu_item in menu_items:
			menu_item.setdefault('children', []).sort(key=operator.itemgetter('sequence'))

		(menu_roots + menus)._set_menuitems_xmlids(menu_root)

		return menu_root