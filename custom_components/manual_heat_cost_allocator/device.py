from .const import DOMAIN

def get_device_info(prefix, config_entry_id, area_id=None):
    return {
        "identifiers": {(DOMAIN, config_entry_id)},
        "name": f"{prefix} Heat Cost Allocator",
        "manufacturer": "Manual Heat Cost Allocator",
        "model": "Manual Heat Cost Allocator",
    }
