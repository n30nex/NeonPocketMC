# NeonPocketMC stack roadmap

This roadmap keeps one shared visual language while preserving separate firmware images for different chips, radios, and runtime costs. There is no universal image.

## Room Server builds

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
| `heltec_rcc6_room_server_full_tft` | NV3001B, 220 x 128 | AP/STA WebUI + MQTT | Full dashboard; experimental until the two-broker RAM burn passes |

The four filenames make the trade-off explicit for non-technical users. They share one source implementation and compile-time feature flags; they are not four code forks. The setup script will ask two plain questions—screen or headless, minimal or full—and select the matching image.

The full build keeps the existing broker preset catalog, including `mqtt1.meshcore.ca` and `mqtt2.meshcore.ca`, while allowing custom broker settings. Web management is authenticated, starts as a setup AP when needed, and reports the station IP after joining local 2.4 GHz Wi-Fi.

## Shared on-device interface

Every 220 x 128 build uses the same small native shell:

- node name, role, battery millivolts, and link state in the header;
- Home, RF, Diagnostics, and Power pages;
- role pages for companion messages, repeater recently-heard nodes, Room Server clients/posts, and MQTT broker state;
- first gesture wakes and is consumed, single press advances, double press performs the page action, and hold keeps the two-step power confirmation;
- 60-second TFT timeout while LoRa and the selected service remain active;
- notification bars and horizontal sweep motion that touch only a few eight-row framebuffer bands.

The UI reads copied snapshots. It never walks mutable radio, client, post, or MQTT structures while rendering.

## One-button messages

The first release uses six fixed quick replies—`OK`, `YES`, `NO`, `ON MY WAY`, `NEED HELP`, and `73`—with an 800 ms automatic highlight and a separate Yes/No send confirmation. This is fast, predictable, and inexpensive.

Full text entry follows as an optional alphabetic row/column scanner with `SPACE`, `BACKSPACE`, `SEND`, and `CANCEL`. It uses a fixed 160-byte buffer and no dictionary. T9, radial keyboards, continuously animated clocks, and gesture-heavy input are intentionally excluded because they add ambiguity or exceed the RCC6 display-transfer budget.

## Animated boot

Screen builds draw the NeonPocket mark from native display primitives, then animate the three-node mesh and outgoing packet sparks while reporting startup stages such as radio, storage, mesh, and service. A fatal radio or storage state replaces the animation with a stable explanation instead of a silent halt or boot-loop-looking screen.

## Release gates

The normal release gate stays deliberately small:

1. exact-target GitHub Actions build and checksum manifest;
2. clean boot, upright TFT, storage preservation, and normal button flow;
3. one LoRa transmit and receive receipt;
4. Web/MQTT connection proof for full RCC6 images;
5. for full RCC6 + TFT only, both MQTT slots active while the framebuffer and an additional 32 KB contiguous diagnostic allocation remain healthy for 30 minutes.

Battery percentage and automatic low-voltage shutdown remain disabled until each board's ADC is compared with a multimeter. The UI reports raw millivolts and warns below 3.45 V with 3.60 V hysteresis.
