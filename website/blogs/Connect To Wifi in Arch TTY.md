# Connect To Wifi in Arch TTY

1. Set keyboard layout

    ```
    loadkeys us
    ```

1. Run iwctl

    ```
    iwctl
    ```
    this should get you into the iwctl prompt
    
1. Check available devices
    ```
    [iwd]# device list
    ```
    For most cases it is going to be 'wlan0'

1. Connect to desired AP
    ```
    [iwd]# station <device> scan
[iwd]# station <device> get-networks
[iwd]# station <device> connect <SSID>
[iwd]# exit
    ```