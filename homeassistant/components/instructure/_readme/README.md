---
title: Canvas
description: Instructions on how to integrate the Canvas integration into Home Assistant.
ha_category:
  - Sensor
  - Calendar
  - Link
ha_config_flow: true
ha_release: 0.88
ha_iot_class: Cloud Polling
ha_domain: instructure
ha_platforms:
  - sensor
ha_codeowners:
  - '@theowiik',
  - '@elias-carlson',
  - '@erikwessman',
  - '@Caodongying',
  - '@F-MertGultekin',
  - '@Lemi007',
ha_integration_type: integration
---

<!-- Some stuff to include :salute:

- What the integration is and why someone would use it
    - Screenshots and maybe quick overview of features
- Add instructions/explanation for:
    - Config flow
        - Canvas host + token
        - Rooms
    - Adding the cards to the dashboard
        - "Standard" sensors
        - Calendar
        - Quick links
            - yaml file (manually or in frontend)
-->

The Canvas integrations allows you to get an overview of your courses, including assignments, announcements, grades, and more.

- [Configuration](#configuration)
  - [Personal Access Token](#personal-access-token)
- [Adding the services](#adding-the-services)
  - [Sensors](#sensors)
  - [Assignments Calendar](#assignments-calendar)
  - [Quick Links](#quick-links)

<!-- Overview image -->
![Cat](http://placekitten.com/g/300/100)

## Configuration

1. Browse to your Home Assistant instance.
2. Go to [Settings > Devices & Services](https://my.home-assistant.io/redirect/integrations).
3. In the bottom right corner, select the [**⊕ Add Integration**](https://my.home-assistant.io/redirect/config_flow_start?domain=instructure) button.
4. From the list, select **Canvas**.
5. Follow the instructions on screen to complete the setup.

The host should be without the domain extension, e.g **`chalmers`** and not **`chalmers.se`**.

### Personal Access Token

Your personal access token can be generated in **Canvas > Account > Settings > Approved integrations** by clicking the **⊕ New access token** `https://{host}.instructure.com/profile/settings`

## Adding the services

![Screenshot of a Home Assistant dashboard with the Canvas integration.](dashboard.png)

### Sensors

To add one of the assignments, announcements, inbox, or grades sensors to your dashboard, navigate to the integration in [**Settings > Devices & Services**](https://my.home-assistant.io/redirect/integrations) and click on **Services**. In the table of services, click on the one you want to add, and press **Add to dashboard**.

### Assignments Calendar

To add the assignments calendar, go to your dashboard, click on the three dots in the top right and select **Edit dashboard**. Then, click on **Add card** in the bottom right and select the **Calendar**. Here, choose **`canvas calendar assignments`** as the entity and press **Save**

### Quick Links

idk, yaml or smth

<!-- image of a cat below -->
