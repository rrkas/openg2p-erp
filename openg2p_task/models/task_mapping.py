class EventItem:
    def __init__(
        self,
        type_ref,
        subtype_ref,
        entity_type,
        default_status_ref="task_status_available",
    ):
        self.type_ref = type_ref
        self.subtype_ref = subtype_ref
        self.entity_type = entity_type
        self.default_status_ref = default_status_ref


event_map = {
    # General
    "program_create": EventItem(
        type_ref="task_type_general",
        subtype_ref="task_subtype_create_program",
        entity_type="openg2p.program",
    ),
    "program_update": EventItem(
        type_ref="task_type_general",
        subtype_ref="task_subtype_update_program",
        entity_type="openg2p.program",
    ),
    "program_category_create": EventItem(
        type_ref="task_type_general",
        subtype_ref="task_subtype_create_program_category",
        entity_type="openg2p.program.enrollment_category",
    ),
    "program_category_update": EventItem(
        type_ref="task_type_general",
        subtype_ref="task_subtype_update_program_category",
        entity_type="openg2p.program.enrollment_category",
    ),
    # ODK
    "odk_config_create": EventItem(
        type_ref="task_type_odk",
        subtype_ref="task_subtype_odk_create_config",
        entity_type="odk.submissions",
    ),
    "odk_config_update": EventItem(
        type_ref="task_type_odk",
        subtype_ref="task_subtype_odk_update_config",
        entity_type="odk.submissions",
    ),
    "odk_pull": EventItem(
        type_ref="task_type_odk",
        subtype_ref="task_subtype_odk_pull",
        entity_type="odk.submissions",
    ),
    # Registration
    "regd_create": EventItem(
        type_ref="task_type_regd",
        subtype_ref="task_subtype_regd_create",
        entity_type="openg2p.registration",
    ),
    "regd_update": EventItem(
        type_ref="task_type_regd",
        subtype_ref="task_subtype_regd_update",
        entity_type="openg2p.registration",
    ),
    "regd_change_stage": EventItem(
        type_ref="task_type_regd",
        subtype_ref="task_subtype_regd_change_stage",
        entity_type="openg2p.registration",
    ),
    "regd_to_beneficiary": EventItem(
        type_ref="task_type_regd",
        subtype_ref="task_subtype_regd_make_beneficiary",
        entity_type="openg2p.beneficiary",
    ),
    # Beneficiary
    "beneficiary_create": EventItem(
        type_ref="task_type_beneficiary",
        subtype_ref="task_subtype_beneficiary_create",
        entity_type="openg2p.beneficiary",
    ),
    "beneficiary_update": EventItem(
        type_ref="task_type_beneficiary",
        subtype_ref="task_subtype_beneficiary_update",
        entity_type="openg2p.beneficiary",
    ),
    "beneficiary_enroll": EventItem(
        type_ref="task_type_beneficiary",
        subtype_ref="task_subtype_beneficiary_enroll_programs",
        entity_type="openg2p.beneficiary",
    ),
    "beneficiary_transaction_batch_create": EventItem(
        type_ref="task_type_beneficiary",
        subtype_ref="task_subtype_beneficiary_create_transaction_batch",
        entity_type="openg2p.disbursement.batch.transaction",
    ),
    "beneficiary_transaction_batch_update": EventItem(
        type_ref="task_type_beneficiary",
        subtype_ref="task_subtype_beneficiary_update_transaction_batch",
        entity_type="openg2p.disbursement.batch.transaction",
    ),
    "beneficiary_transaction_single_create": EventItem(
        type_ref="task_type_beneficiary",
        subtype_ref="task_subtype_beneficiary_create_transaction_single",
        entity_type="openg2p.disbursement.single.transaction",
    ),
    "beneficiary_transaction_single_update": EventItem(
        type_ref="task_type_beneficiary",
        subtype_ref="task_subtype_beneficiary_update_transaction_single",
        entity_type="openg2p.disbursement.single.transaction",
    ),
}
