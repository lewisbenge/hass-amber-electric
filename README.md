# Home Assistant Plugin for Amber Electricity Real-Time Pricing

A custom component for Home Assistant (www.home-assistant.io) to pull the latest energy prices from the Amber Electric (https://www.amberelectric.com.au/) REST API based on Post Code. 

# How to install

Copy custom_components/amberelectric to your hass data directory (where your configuration.yaml lives). It should go into the same directory structure (YOUR_CONFIG_DIRECTORY/custom_components/amberelectric)

Add a sensor into your configuration.yaml file that defines the Post Code you want to lookup. 

`
sensor:
  - platform: amberelectric
    postcode: '2000'

`

# Ideas 

This project is early in it's creation. If you have ideas on how you want to use the Amber real-time data inside Home Assistant please let me know and I'll try my best to update to code to reflect the various use-cases. 
