"""Config flow for Heat Cost Allocator integration."""
from homeassistant import config_entries
from .const import DOMAIN

class HeatCostAllocatorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Heat Cost Allocator."""


    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            prefix = user_input.get("prefix", "").strip()
            area = user_input.get("area")
            if not prefix:
                errors["prefix"] = "required"
            else:
                return self.async_create_entry(
                    title=f"Heat Cost Allocator ({prefix})",
                    data={"prefix": prefix, "area": area}
                )
        return self.async_show_form(
            step_id="user",
            data_schema=self._get_data_schema(),
            errors=errors
        )

    def _get_data_schema(self):
        from homeassistant.helpers import config_validation as cv
        import voluptuous as vol
        return vol.Schema({
            vol.Required("prefix"): cv.string,
            vol.Optional("area"): str
        })
