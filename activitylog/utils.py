# utils.py

def get_model_changes(old_instance, new_instance):
    changes = {}

    for field in old_instance._meta.fields:
        field_name = field.name

        # Skip auto fields
        if field_name in ["updated_at", "created_at"]:
            continue

        old_value = getattr(old_instance, field_name)
        new_value = getattr(new_instance, field_name)

        if old_value != new_value:
            changes[field_name] = {
                "old": str(old_value),
                "new": str(new_value),
            }

    return changes