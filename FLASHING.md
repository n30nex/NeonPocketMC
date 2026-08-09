# Flashing and setup

## Before you start

1. Identify the board: **RC52** is nRF52840; **RCC6** is ESP32-C6.
2. Choose the role: companion, repeater, or MQTT observer/repeater.
3. Attach the LoRa antenna before any transmit test.
4. Verify the downloaded SHA-256 value against `SHA256SUMS.txt`.

## RC52 companion or repeater

1. Connect the RC52 by USB.
2. Double-press reset to expose its UF2 drive.
3. Copy exactly one matching `.uf2` file to that drive.
4. Wait for the drive to disappear and the board to reboot.

Use the `.hex` only for advanced recovery/programmer workflows. Normal UF2 installation must not erase or replace the bootloader/SoftDevice.

## RCC6 companion

The BLE and Web/AP images are separate firmware modes.

Normal app-only update:

```powershell
python -m esptool --chip esp32c6 --port COM21 write-flash 0x10000 NeonPocketMC-RCC6-1.1-RC1-BLE-app.bin
```

Replace `COM21` and the filename as needed. Use the Web/AP app filename for Web mode.

The Web/AP build starts its saved local 2.4 GHz Wi-Fi configuration when available. Otherwise it exposes its setup AP; the TFT shows the SSID, key, and address. The local WebUI uses HTTP authentication in station mode. TCP/5000 is for trusted private LANs and exposes the full MeshCore companion/admin protocol.

## RCC6 MQTT observer/repeater

1. Flash `NeonPocketMC-RCC6-Repeater-v1.0.0-rc.2-app.bin` at `0x10000`.
2. Keep USB connected.
3. Extract and run the included configurator package for Windows or Linux.
4. Set the node name, radio preset or all custom radio values, region/channel configuration, Wi-Fi, MQTT broker, and credentials before deployment.
5. The firmware defaults to **3-byte packet hash mode**.
6. The setup tool reports the local-network address after Wi-Fi connects. You can also reopen the serial setup utility or check your router/DHCP client list.

The firmware also offers a setup WebUI and dashboard. Default broker choices prioritize `mqtt1.meshcore.ca` and `mqtt2.meshcore.ca`; every broker offered by the upstream MQTT observer integration remains available or can be entered manually.

Manual flasher and upstream integration references are maintained in the dedicated [RCC6 repeater release documentation](https://github.com/n30nex/NeonPocketMC-RCC6-Repeater/releases/tag/v1.0.0-rc.2).

## RCC6 recovery image

Use a `*-full-recovery-preserves-meshcore-settings.bin` image at `0x0` only to repair bootloader/partition/application regions:

```powershell
python -m esptool --chip esp32c6 --port COM21 write-flash 0x0 <recovery-image.bin>
```

Do not run a full-chip erase. Recovery resets NVS-backed BLE bonds and saved Wi-Fi but does not reach the SPIFFS data partition at `0xC90000`.

## Troubleshooting

For a blank screen, boot loop, or storage error, capture a 115200-baud log and report:

- exact hardware model and radio module;
- exact release filename and SHA-256;
- flash tool and address;
- whether an erase was performed;
- the complete boot log up to the failure.

Never publish private keys, channel secrets, Wi-Fi passwords, MQTT credentials, or a full flash backup.
