from .device import get_device_info
"""Sensor platform for Heat Cost Allocator."""
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.util import dt as dt_util
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Heat Cost Allocator sensors from a config entry."""
    prefix = config_entry.data.get("prefix", "")
    area_id = config_entry.data.get("area")
    sensor = HeatCostAllocatorSensor(hass, prefix, config_entry.entry_id, area_id)
    average_sensor = HeatCostAllocatorAverageDailyConsumption(hass, prefix, config_entry.entry_id, area_id)
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["sensor_entity"] = sensor
    async_add_entities([sensor, average_sensor])

class HeatCostAllocatorSensor(SensorEntity):
    """Representation of a Heat Cost Allocator sensor."""

    _attr_icon = "mdi:numeric"

    def __init__(self, hass, prefix, config_entry_id=None, area_id=None):
        self.hass = hass
        self._prefix = prefix
        self._config_entry_id = config_entry_id
        self._area_id = area_id
        self._attr_name = f"{prefix} Heat Cost Allocator Value"
        self._attr_unique_id = f"{prefix}_heat_cost_allocator_value"
        self._attr_native_unit_of_measurement = "units"
        self._attr_native_value = None  # Don't set initial value

    @property
    def device_info(self):
        return get_device_info(self._prefix, self._config_entry_id, self._area_id)

    @property
    def native_value(self):
        # Always read from hass.data if available, per device
        value = None
        if DOMAIN in self.hass.data and "values" in self.hass.data[DOMAIN]:
            value = self.hass.data[DOMAIN]["values"].get(self._config_entry_id)
        if value is not None:
            return int(value)
        return self._attr_native_value  # Will be None until value is set

    def update_value(self, value: int):
        self._attr_native_value = int(value)
        self.async_write_ha_state()


class HeatCostAllocatorAverageDailyConsumption(SensorEntity):
    """Representation of average daily consumption sensor."""

    _attr_icon = "mdi:chart-line"

    def __init__(self, hass, prefix, config_entry_id=None, area_id=None):
        self.hass = hass
        self._prefix = prefix
        self._config_entry_id = config_entry_id
        self._area_id = area_id
        self._attr_name = f"{prefix} Heat Cost Allocator Average Daily"
        self._attr_unique_id = f"{prefix}_heat_cost_allocator_average_daily"
        self._attr_native_unit_of_measurement = "units/day"
        self._attr_native_value = None
        self._attr_state_class = "measurement"

    @property
    def device_info(self):
        return get_device_info(self._prefix, self._config_entry_id, self._area_id)

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()
        # Initial update
        await self.async_update()

    async def async_update(self):
        """Update the sensor value."""
        # Get the sensor entity ID for this device (the main value sensor)
        main_sensor_entity_id = f"sensor.{self._prefix.lower().replace(' ', '_')}_heat_cost_allocator_value"
        
        # Get current value from the state
        current_state = self.hass.states.get(main_sensor_entity_id)
        if not current_state or current_state.state == "unknown":
            return
        
        try:
            current_value = float(current_state.state)
            current_date = current_state.last_updated
        except (ValueError, TypeError):
            return
        
        # Get history for the last 31 days to find value before the 30-day window
        now = dt_util.now()
        start_time = now - timedelta(days=31)
        
        try:
            from homeassistant.components.history import async_get_history
            
            history = await async_get_history(
                self.hass,
                main_sensor_entity_id,
                start_time,
                now,
            )
            
            if history and main_sensor_entity_id in history:
                states = history[main_sensor_entity_id]
                if isinstance(states, list) and len(states) >= 1:
                    # Get the first state (oldest) which is before the 30-day window
                    old_state = states[0]
                    
                    try:
                        old_value = float(old_state.get("state", 0))
                        # Parse the last_changed timestamp
                        old_date_str = old_state.get("last_changed")
                        if old_date_str:
                            old_date = dt_util.parse_datetime(old_date_str)
                        else:
                            return
                    except (ValueError, TypeError):
                        return
                    
                    if not old_date:
                        return
                    
                    # Calculate consumption (difference)
                    consumption = current_value - old_value
                    
                    # Calculate days between old_date and current_date
                    days_diff = (current_date - old_date).days
                    
                    # Calculate average per day
                    if days_diff > 0 and consumption >= 0:
                        average_daily = consumption / days_diff
                        self._attr_native_value = round(average_daily, 2)
        except Exception:
            # If history is not available, leave value as None
            pass
