import logging
import voluptuous as vol

from aiohttp import web
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.components.http import HomeAssistantView
from homeassistant.const import CONF_ENTITY_ID

# We'll use feedgen to build RSS feeds
from feedgen.feed import FeedGenerator

_LOGGER = logging.getLogger(__name__)

DOMAIN = "rss_alerts"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_ENTITY_ID): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA
)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the RSS Alerts integration via configuration.yaml."""
    conf = config.get(DOMAIN)
    if conf is None:
        _LOGGER.warning("rss_alerts config not found in configuration.yaml, using defaults")
        entity_id = "sensor.example_sensor"
    else:
        entity_id = conf.get(CONF_ENTITY_ID)

    # Register our HTTP endpoint at /api/rss_alerts
    hass.http.register_view(RSSAlertsView(hass, entity_id))
    return True


class RSSAlertsView(HomeAssistantView):
    """Handle requests to the /api/rss_alerts endpoint."""

    url = "/api/rss_alerts"
    name = "api:rss_alerts"
    requires_auth = False  # Set True if you need Home Assistant authentication

    def __init__(self, hass: HomeAssistant, entity_id: str):
        """Initialize the view."""
        self._hass = hass
        self._entity_id = entity_id

    async def get(self, request):
        """Handle the incoming HTTP GET request to produce the RSS feed."""
        # Gather data from Home Assistant
        state = self._hass.states.get(self._entity_id)

        # Build the RSS feed
        fg = FeedGenerator()
        fg.title("Home Assistant RSS Alerts")
        fg.link(href="http://example.com/rss_alerts", rel="self")
        fg.description("RSS feed with alerts or states from Home Assistant")

        # Always add an item describing the current state
        if state:
            fe = fg.add_entry()
            fe.title(f"State of {self._entity_id}")
            fe.link(href="http://example.com/entity_info")  # example link
            fe.description(f"Current state: {state.state}")

        # Example: add an alert item if the state is 'problem'
        if state and state.state.lower() == "problem":
            alert_entry = fg.add_entry()
            alert_entry.title("ALERT - Problem detected!")
            alert_entry.link(href="http://example.com/alerts")
            alert_entry.description(f"{self._entity_id} reported a problem!")

        # Generate RSS feed as a string
        rss_xml = fg.rss_str(pretty=True).decode("utf-8")

        # Return the RSS data with the correct content type
        return web.Response(
            text=rss_xml,
            content_type="application/rss+xml"
        )
