# NeonPocketMC stack roadmap

Suite `v1.1.0-rc.2` carries the first Room Server matrix, shared branding, animated companion startup, RCC6 Quick Reply, and the exact upstream boosted-RX-gain reset fix while preserving separate firmware images for different chips, radios, and runtime costs. There is no universal image.

## Released Room Server builds

Room Server source belongs beside the existing repeater/server firmware for each hardware family. The unified repository remains a catalog and never becomes a second copy of the firmware source.

### RC52

| Build | Display | Network services | Intended use |
|---|---|---|---|
| `heltec_rc52_room_server_headless` | Off | None | Lowest-overhead indoor or battery room server |
| `heltec_rc52_room_server_tft` | NV3001B, 220 x 128 | None | Local dashboard and USB/RF administration |

Both images use the same room-server core, RC52 radio power sequence, battery ADC, fail-closed storage, and real nRF52 system-off behavior. The TFT image adds one RGB565 framebuffer and a 60-second display timeout.

### RCC6

| Build | Display | Wi-Fi / MQTT | Intended use |
|---|---|---|---|
| `heltec_rcc6_room_server_minimal_headless` | Off | Off | Smallest local room server |
| `heltec_rcc6_room_server_minimal_tft` | NV3001B, 220 x 128 | Off | Local room dashboard without network overhead |
| `heltec_rcc6_room_server_full_headless` | Off | AP/STA WebUI + MQTT | Network-managed service node |
| `heltec_rcc6_room_server_full_tft` | NV3001B, 220 x 128 | AP/STA WebUI + MQTT | Full dashboard; experimental indexed-framebuffer profile |

The four filenames make the trade-off explicit for non-technical users. They share one source implementation and compile-time feature flags; they are not four code forks. The setup script asks plain role questions and refuses settings that do not exist in a minimal image.

The full build keeps the existing broker preset catalog, including `mqtt1.meshcore.ca` and `mqtt2.meshcore.ca`, while allowing custom broker settings. Web management is authenticated, starts as a setup AP when needed, and reports the station IP after joining local 2.4 GHz Wi-Fi.

## Shared on-device interface

Companion and service dashboards share the NeonPocket palette, native 220 x 128 geometry, fail-closed status screens, and low-overhead drawing rules. Companion builds provide:

- node name, role, battery millivolts, and link state in the header;
- Home, RF, Diagnostics, and Power pages;
- role pages for messages, nearby nodes, RF, Bluetooth, diagnostics, and power;
- first gesture wakes and is consumed, single press advances, double press performs the page action, and hold keeps the two-step power confirmation;
- 60-second TFT timeout while LoRa and the selected service remain active;
- notification bars and horizontal sweep motion that touch only a few eight-row framebuffer bands.

Room Server TFT builds instead prioritize room identity, clients, posts, RF state, and service health. UI rendering reads copied snapshots rather than walking mutable radio, client, post, or MQTT structures.

## One-button messages

The RCC6 companion now ships six fixed quick replies—`OK`, `YES`, `NO`, `ON MY WAY`, `NEED HELP`, and `73`—with an 800 ms automatic highlight and a separate send confirmation. This is fast, predictable, and inexpensive.

Full text entry follows as an optional alphabetic row/column scanner with `SPACE`, `BACKSPACE`, `SEND`, and `CANCEL`. It uses a fixed 160-byte buffer and no dictionary. T9, radial keyboards, continuously animated clocks, and gesture-heavy input are intentionally excluded because they add ambiguity or exceed the RCC6 display-transfer budget.

## Animated boot

RC52 and RCC6 companion builds draw the NeonPocket mark from native display primitives and animate the startup sequence. A fatal radio or storage state replaces the animation with a stable explanation instead of a silent halt or boot-loop-looking screen. Extending the same staged animation to every TFT service profile remains follow-up work.

## Release gates

The release gate stays deliberately small:

1. exact-target GitHub Actions build and checksum manifest;
2. clean boot, upright TFT, storage preservation, and normal button flow;
3. one LoRa transmit and receive receipt;
4. Web/MQTT connection proof for full RCC6 images;
5. for full RCC6 + TFT, successful indexed-framebuffer allocation and a 32 KB contiguous post-service diagnostic allocation.

The RCC6 qualification unit passed the 32 KB gate with a 58 KB largest free block and was then restored to the exact released BLE companion. A longer two-broker burn and fresh RC52 Room Server hardware smoke remain recommended before promotion beyond prerelease.

Battery percentage and automatic low-voltage shutdown remain disabled until each board's ADC is compared with a multimeter. The UI reports raw millivolts and warns below 3.45 V with 3.60 V hysteresis.
