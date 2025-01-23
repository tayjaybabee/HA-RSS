# RSS Alerts Integration for Home Assistant

This integration allows you to create an RSS feed based on the state of an entity in Home Assistant. The feed can be accessed via an HTTP endpoint and provides updates on the specified entity's state.

## Installation

1. Clone this repository into your Home Assistant `custom_components` directory:
    ```bash
    git clone https://github.com/yourusername/rss_alerts.git custom_components/rss_alerts
    ```

2. Add the following configuration to your `configuration.yaml`:
    ```yaml
    rss_alerts:
      entity_id: sensor.example_sensor
    ```

3. Restart Home Assistant.

## Configuration

In your `configuration.yaml`, specify the entity ID you want to monitor:
```yaml
rss_alerts:
  entity_id: sensor.example_sensor
```

## Usage

Once the integration is set up, you can access the RSS feed at:
```
http://<your_home_assistant_url>/api/rss_alerts
```

The feed will include entries for the current state of the specified entity and any alerts if the state indicates a problem.

## Example

If the entity `sensor.example_sensor` has a state of `problem`, the RSS feed will include an alert entry:
```xml
<item>
  <title>ALERT - Problem detected!</title>
  <link>http://example.com/alerts</link>
  <description>sensor.example_sensor reported a problem!</description>
</item>
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Support

If you have any questions or need help, feel free to open an issue on GitHub.
