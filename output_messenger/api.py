import frappe
import json
from frappe import _
from output_messenger.messenger import send_to_output_messenger
from frappe.utils import get_url_to_form

@frappe.whitelist()
def send_output_notification_to_users(recipients_list, notes, doctype, docname):
    sender_id = frappe.db.get_value("User", frappe.session.user, "custom_output_user_id")
    doc_link = get_url_to_form(doctype, docname)
    html_link = '<a href="{doc_link}" target="_blank">{doctype} {docname}</a>'.format(doc_link=doc_link, doctype=doctype, docname=docname)
    # Above message is related to 
    if notes:
        message_text = notes + " \n\n Above message is related to: \n" + html_link
    else:
        message_text = "Above message is related to: \n" + html_link

    recipients_list = json.loads(recipients_list)
    # print("===recipients_list===", recipients_list)
    if len(recipients_list) > 0:
        for recipient in recipients_list:
            recipient_id = frappe.db.get_value("User", recipient, "custom_output_user_id")
            if recipient_id:
                send_to_output_messenger(sender_id, recipient_id, message_text)
                # print("====Output Messenger: sender - {0}, receiver - {1} ".format(sender_id, recipient_id))

        frappe.msgprint(_("Message Sent to {0} Recipient On Output Messenger").format(len(recipients_list)))