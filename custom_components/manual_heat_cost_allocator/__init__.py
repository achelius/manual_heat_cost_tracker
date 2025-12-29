"""Heat Cost Allocator integration for Home Assistant."""


from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Heat Cost Allocator integration."""
    # Register services in the global domain
    from .services import async_setup_services
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if "services_registered" not in hass.data[DOMAIN]:
        await async_setup_services(hass)
        hass.data[DOMAIN]["services_registered"] = True
    return True


async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Heat Cost Allocator from a config entry."""
    # Ensure services are registered
    from .services import async_setup_services
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if "services_registered" not in hass.data[DOMAIN]:
        await async_setup_services(hass)
        hass.data[DOMAIN]["services_registered"] = True
    
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["sensor", "number"])
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    unload_ok = True
    for platform in ["sensor", "number"]:
        res = await hass.config_entries.async_forward_entry_unload(entry, platform)
        unload_ok = unload_ok and res
    return unload_ok
