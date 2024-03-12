This is an integration of Home Assistant to read data of solar invertor via datalogger, as of now the integration is implementing a small part of the functionalities possible with the platform of http://api.shinemonitor.com or http://android.shinemonitor.com. The http://api.shinemonitor.com platform supports, as far as I understand it, multiple applications interfaces. Each implementation requires a companykey, I reused SmartESS companykey. So, in order to use this integration user should be registered with SmartESS app. 

To use this integration, first copy the files into the custom_components, then add the below configurations into the configuration.yaml file under sensor section

  - platform: "solardatalogger"
    name: "Solar Data Logger"
    password: "password"
    username: "username"
    companykey: "bnrl_frRFjEz8Mkn"
    scan_interval: 360

    
