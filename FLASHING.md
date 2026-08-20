# Flashing and setup

## Before you start

1. Identify the board exactly: **RC52** is nRF52840, **RCC6** is ESP32-C6, and Heltec **V3/V4** are distinct ESP32-S3 boards.
2. Choose the role: companion, repeater, or MQTT observer/repeater.
3. Attach the LoRa antenna before any transmit test.
4. Verify the downloaded SHA-256 value against `SHA256SUMS.txt`.

## RC52 companion or repeater

1. Connect the RC52 by USB.
2. Double-press reset to expose its UF2 drive.
3. Copy exactly one matching `.uf2` file to that drive.
4. Wait for the drive to disappear and the board to reboot.

Use the `.hex` only for advanced recovery/programmer workflows. Normal UF2 installation must not erase or replace the bootloader/SoftDevice.

The companion release offers separate BLE and native-USB UF2 files. USB mode carries the standard binary MeshCore companion protocol; it is not the text configuration CLI.

## Heltec WiFi LoRa 32 V3 or V4 companion

V3 and V4 images are not interchangeable. Download the app image from the exact board repository, then write it at `0x10000`:

```powershell
python -m esptool --chip esp32s3 --port COMx write-flash 0x10000 <matching-app-image.bin>
```

Do not erase the whole flash for a normal update. A full backup can contain private identity keys and must never be published. Use a recovery image at `0x0` only when the owning release explicitly calls for bootloader or partition recovery.

Each companion release offers separate BLE and native-USB app images. USB mode carries the standard binary MeshCore companion protocol; it is not the text configuration CLI.

## RCC6 Ultimate companion

The BLE, native-USB, and Web/AP images are separate firmware modes. Native USB carries the standard binary MeshCore companion protocol and is not the text configuration CLI.

Normal app-only update:

```powershell
python -m esptool --chip esp32c6 --port COM21 write-flash 0x10000 NeonPocketMC-RCC6-Ultimate-v2.3.0-rc.3-BLE-app.bin
```

Replace `COM21` and the filename as needed. Use the Web/AP app filename for Web mode.

The Web build starts its saved local 2.4 GHz Wi-Fi configuration when available. Otherwise it exposes its setup AP; the TFT shows the SSID, key, and address. The local WebUI uses HTTP authentication in station mode. TCP/5000 is for trusted private LANs and exposes the full MeshCore companion/admin protocol.

Optional battery commands in USB CLI Rescue are `set.batterysize <mAh>` (alias `np battery size <mAh>`) and `np battery offset <mV>`. Capacity is a runtime estimate; the voltage offset must be based on a multimeter comparison.

## RCC6 MQTT observer/repeater

1. Flash `NeonPocketMC-RCC6-Ultimate-Observer-v1.3.0-rc.1-app.bin` at `0x10000`.
2. Keep USB connected.
3. Extract and run the included configurator package for Windows or Linux.
4. Set the node name, radio preset or all custom radio values, region/channel configuration, Wi-Fi, MQTT broker, and credentials before deployment.
5. The firmware defaults to **3-byte packet hash mode**.
6. The setup tool reports the local-network address after Wi-Fi connects. You can also reopen the serial setup utility or check your router/DHCP client list.

The firmware also offers a setup WebUI and dashboard. Default broker choices prioritize `mqtt1.meshcore.ca` and `mqtt2.meshcore.ca`; every broker offered by the upstream MQTT observer integration remains available or can be entered manually.

Manual flasher and upstream integration references are maintained in the dedicated [RCC6 server release documentation](https://github.com/n30nex/NeonPocketMC-RCC6-Repeater/releases/tag/v1.3.0-rc.1).

## RCC6 recovery image

Use a `*-full-recovery-preserves-meshcore-settings.bin` image at `0x0` only to repair bootloader/partition/application regions:

```powershell
python -m esptool --chip esp32c6 --port COM21 write-flash 0x0 <recovery-image.bin>
```

Do not run a full-chip erase. Recovery resets NVS-backed BLE bonds and saved Wi-Fi but does not reach the SPIFFS data partition at `0xC90000`.

## ULP Solar Repeaters

Use the dedicated [ULP release](https://github.com/n30nex/NeonPocketMC-ULP-Solar-Repeaters/releases/tag/v1.0.0-rc.1) and choose the exact V3, V4, RAK4631, RAK3401 1 W, Xiao ESP32-S3, Xiao nRF52840, RCC6, or RC52 image. RCC6 and RC52 have separate headless and TFT files.

- ESP32 normal install: flash the matching `*-app.bin` at `0x10000`.
- nRF52 normal install: enter the board bootloader and copy the matching `.uf2` without erasing or replacing its SoftDevice/bootloader.
- Keep USB connected after restart and run `NeonPocketMC-ULP-Configurator.zip` to set the name, radio preset/region, transmit power, admin password, and power profile.
- New installs default to `ulp on` (balanced receive duty cycle). Existing saved settings remain authoritative; use `ulp on` once when upgrading an older repeater that had power saving disabled.
- RX duty cycling can miss packets. Validate coverage and current draw before a remote deployment.

None of these boards provides a universal raw-solar input. Use a protected battery and external MPPT/charge controller matched to the panel and cell; never wire an unregulated panel directly to VBAT or USB.

## Troubleshooting

For a blank screen, boot loop, or storage error, capture a 115200-baud log and report:

- exact hardware model and radio module;
- exact release filename and SHA-256;
- flash tool and address;
- whether an erase was performed;
- the complete boot log up to the failure.

Never publish private keys, channel secrets, Wi-Fi passwords, MQTT credentials, or a full flash backup.
