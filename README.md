# Home Assistant Plugin for Amber Electric Real-Time Pricing

A custom component for Home Assistant (www.home-assistant.io) to pull the latest energy prices from the Amber Electric (https://www.amberelectric.com.au/) REST API based on Post Code. 

# How to install

Copy custom_components/amberelectric to your hass data directory (where your configuration.yaml lives). It should go into the same directory structure (YOUR_CONFIG_DIRECTORY/custom_components/amberelectric)

Add a sensor into your configuration.yaml file that defines the Post Code you want to lookup. 

```yaml
sensor:
  - platform: amberelectric
    postcode: '2000'
```
Once deployed, you should see 2 sensors added to your Home Assistant entities list, one reflects the current solar feed-in tarrif, and the second is the real-time grid price charged by Amber (including their network fees). 

#Analysing Price Predictions

The 12 hour price predictions from Amber for both solar FiT and grid usage are available as an attribute of the sensor. To use this data-set in automation or scenes, it is best to return the array using a template to achieve what you need. 

The following example uses a template to return the prices based on most expense:

```python
{% for price_forecast in states.sensor.amber_general_usage_price.attributes["price_forcecast"] | sort(attribute='price') | reverse %}
{{price_forecast['pricing_period']}}: {{price_forecast['price']}}
{%- endfor -%}
```

Typically within a template you want to return a single value, to this example would need to be tailored to your specific use-case. You can experiment with Templates in the Developer Tools section of your Home Assistant portal.

# Ideas 

This project is early in it's creation. If you have ideas on how you want to use the Amber real-time data inside Home Assistant please let me know and I'll try my best to update to code to reflect the various use-cases. 
