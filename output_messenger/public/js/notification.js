frappe.ui.form.on("Notification", {
	refresh: function (frm) {
		console.log("Refreshing Notification form");
		frm.set_query("custom_notification_sender_om", () => {
			return {
				filters: {
					custom_output_user_id: ["!=", undefined] || ["!=", ""],
					enabled: 1,
				},
			};
		});

		frm.set_df_property(
			"column_break_5",
			"depends_on",
			"eval:in_list(['Email', 'SMS', 'WhatsApp', 'Wati Whatsapp', 'Output Messenger'], doc.channel)"
		);
		get_receiver_options(frm);
	},
	document_type: function (frm) {
		get_receiver_options(frm);
	},
	channel: function (frm) {
		get_receiver_options(frm);
	},
	onload_post_render: function (frm) {
		get_receiver_options(frm);
	},

});

let get_receiver_options = function(frm){
	if (frm.doc.channel === "Output Messenger") {
		let fields = frappe.get_doc("DocType", frm.doc.document_type).fields;
		let receiver_fields = [];
		
		receiver_fields = get_receiver_fields(fields, function (df) {
			return df.options == "Email";
		});
		// console.log("Receiver fields for Output Messenger:", receiver_fields);
		frm.fields_dict.recipients.grid.update_docfield_property("receiver_by_document_field",	"options",	[""].concat(["owner"]).concat(receiver_fields));
	}
}


let get_select_options = function (df, parent_field) {
				// Append parent_field name along with fieldname for child table fields
				let select_value = parent_field ? df.fieldname + "," + parent_field : df.fieldname;
				let path = parent_field ? parent_field + " > " + df.fieldname : df.fieldname;

				return {
					value: select_value,
					label: path + " (" + __(df.label, null, df.parent) + ")",
				};
			};

let get_receiver_fields = function (
		fields,
		is_extra_receiver_field = (_) => {
			return false;
		}
	) {
		// finds receiver fields from the fields or any child table
		// by default finds any link to the User doctype
		// however an additional optional predicate can be passed as argument
		// to find additional fields
		let is_receiver_field = function (df) {
			return (
				is_extra_receiver_field(df) ||
				(df.options == "User" && df.fieldtype == "Link") ||
				(df.options == "Customer" && df.fieldtype == "Link")
			);
		};
		let extract_receiver_field = function (df) {
			// Add recipients from child doctypes into select dropdown
			if (frappe.model.table_fields.includes(df.fieldtype)) {
				let child_fields = frappe.get_doc("DocType", df.options).fields;
				return $.map(child_fields, function (cdf) {
					return is_receiver_field(cdf)
						? get_select_options(cdf, df.fieldname)
						: null;
				});
			} else {
				return is_receiver_field(df) ? get_select_options(df) : null;
			}
		};
		return $.map(fields, extract_receiver_field);
	};