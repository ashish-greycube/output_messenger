import frappe
import json
from frappe.email.doctype.notification.notification import (
	Notification,
	get_context,
)
from frappe.utils import cstr, get_link_to_form
from output_messenger.messenger import send_to_output_messenger

class OutputMessengerNotification(Notification):
	def send(self, doc):
		context = get_context(doc)
		# context = {"doc": doc, "alert": self, "comments": None}
		# if doc.get("_comments"):
		# 	context["comments"] = json.loads(doc.get("_comments"))

		# if self.is_standard:
		# 	self.load_standard_properties(context)


		if self.channel == "Output Messenger":
			try:
				# Resolve recipients to Emails/Usernames
				recipients, cc, bcc = self.get_list_of_recipients(doc, context)
				# print(recipients, cc, bcc,  "=====recipients=====")
				user = recipients + cc + bcc
				
				# Map to Output Messenger IDs from User DocType
				messenger_ids = frappe.get_all(
					"User",
					filters={"name": ["in", user], "enabled": 1},
					pluck="custom_output_user_id"
				)

				# Get Sender ID from current session
				if self.custom_notification_sender_om:
					sender_id = frappe.db.get_value("User", self.custom_notification_sender_om, "custom_output_user_id")
				
				if not sender_id:
					sender_id = frappe.db.get_value("User", frappe.session.user, "custom_output_user_id")

				message_text = frappe.render_template(self.message, context)

				# print(messenger_ids, "===messenger_ids===")
				if len(messenger_ids) > 0:
					for target_id in messenger_ids:
						if target_id:
							# print(target_id, "=====senddd", "=="*20)
							send_to_output_messenger(sender_id, target_id, message_text)
				# print("====================send notification to output messenger=====================")
				# print("*"*100)
				frappe.logger().info(f"Output Messenger: Sent to {len(messenger_ids)} users.")  ## add in logs folder

			except:
				error = frappe.get_traceback()
				log = frappe.log_error(title="Failed to send Output Messenger notification", message=error)
				frappe.msgprint("Error while sending the message {0}".format(get_link_to_form("Error Log", log.name)), alert=True)
		else:
			# v16 logic: super() automatically finds the next class in the chain (e.g., Wati Whatsapp)
			return super().send(doc)