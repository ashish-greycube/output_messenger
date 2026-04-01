import frappe
import requests
from frappe import _
from frappe.utils import cstr, get_link_to_form

def send_to_output_messenger(sender_id, target_id, message_text):
	"""
	Standalone function to send a message via Output Messenger.
	Can be called from anywhere in the system.
	"""
	try:
		## 1. Fetch Settings
		settings = frappe.get_single("Output Messenger Settings OM")
		if not settings.enable_output_messenger:
			return {"status": "disabled", "message": "Integration is disabled"}

		## 2. Prepare API Data
		url = settings.api_url
		api_key = settings.api_key
		# api_key = settings.get_password("api_key")
		
		headers = {
			"Content-Type": "application/json",
			"API-KEY": api_key
		}
		
		data = {
			"from": sender_id,
			"to": target_id,
			"message": message_text,
			"otr": 0,
			"notify": 1
		}

		## 3. Execute Request
		response = requests.post(url, headers=headers, json=data)
		
		## Log the response for debugging
		if response.status_code == 200:
			response_json = response.json()
			print(response_json, "===response from Output Messenger API===")
			# if len(response_json) > 0 and not response_json[0].get("success"):
			# 	log = frappe.log_error(
			# 		message=response_json, title=_("Output Messenger API Error")
			# 	)
			# 	frappe.msgprint("Error while sending the message {0}".format(get_link_to_form("Error Log", log.name)), alert=True)
			# 	return {"status": "error", "message": "API returned success status but result is false"}
			# else:
			return response.json()
		else:
			log = frappe.log_error(
				title=_("Output Messenger API Error"),
				message=f"Status: {response.status_code}\nResponse: {response.text}"
			)
			frappe.msgprint("Error while sending the message {0}".format(get_link_to_form("Error Log", log.name)), alert=True)
			return {"status": "error", "message": f"API returned status {response.status_code}"}

	except:
		error = frappe.get_traceback()
		log = frappe.log_error(title="Output Messenger Error", message=error)
		frappe.msgprint("Error while sending the message {0}".format(get_link_to_form("Error Log", log.name)), alert=True)
		return None