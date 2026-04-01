import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def after_migrate():
	create_custom_fields_in_core_doctype()
	
def create_custom_fields_in_core_doctype():
	custom_fields = {
		"User" : [
			{
				"fieldname": "custom_column_break_1",
				"fieldtype": "Column Break",
				"insert_after": "enabled",
				"is_custom_field": 1,
				"is_system_generated": 0,
			},
			{
				"fieldname": "custom_output_user_id",
				"fieldtype": "Data",
				"label": "Output Messenger User ID",
				"insert_after": "custom_column_break_1",
				"is_custom_field": 1,
				"is_system_generated": 0,
			},
		],
		"Notification": [
			{
				"fieldname": "custom_notification_sender_om",
				"fieldtype": "Link",
				"label": "Notification Sender",
				"insert_after": "sender",
				"options":"User",
				"is_custom_field": 1,
				"is_system_generated": 0,
				"depends_on": "eval:doc.channel=='Output Messenger'",
				"mandatory_depends_on": "eval:doc.channel=='Output Messenger'",
			},
		]
	}
	
	print("Adding Landed Cost custom field in Item.....")
	for dt, fields in custom_fields.items():
		print("*******\n %s: " % dt, [d.get("fieldname") for d in fields])
	create_custom_fields(custom_fields)

	# add Channel option
	channels = frappe.get_meta("Notification").get_options("channel").split("\n")
	if not "Output Messenger" in channels:
		channels.append("Output Messenger")
		make_property_setter(
			"Notification", "channel", "options", "\n".join(channels), ""
		)