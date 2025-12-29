"""Services for Heat Cost Allocator integration."""
from homeassistant.core import HomeAssistant, ServiceCall
from .const import DOMAIN

async def async_setup_services(hass: HomeAssistant):
    """Set up services for Heat Cost Allocator."""

    async def cleanup_statistics(call: ServiceCall):
        """Remove zero value statistics from heat cost allocator entities."""
        from homeassistant.components import statistics
        
        # Get the statistics component
        stats = hass.data.get("statistics", {})
        
        # Find all heat cost allocator number entities
        entity_registry = hass.helpers.entity_registry.async_get(hass)
        for entity in entity_registry.entities.values():
            if entity.domain == "number" and entity.platform == DOMAIN:
                entity_id = entity.entity_id
                
                # Access statistics data
                from homeassistant.components.statistics import StatisticsData
                
                # Clear zero values from history stats
                if entity_id in stats:
                    stats_data = stats[entity_id]
                    if isinstance(stats_data, dict):
                        # Remove entries where value is 0
                        stats_data = {k: v for k, v in stats_data.items() if v.get("value") != 0}
                        stats[entity_id] = stats_data

    hass.services.async_register(
        DOMAIN,
        "cleanup_zero_statistics",
        cleanup_statistics,
        description="Clean up zero value statistics from Heat Cost Allocator number entities"
    )
