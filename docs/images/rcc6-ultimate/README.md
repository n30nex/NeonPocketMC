# Ultimate RCC6 capture provenance

These images were captured from the connected Heltec RadioCore RCC6 qualification unit through a diagnostic-only USB framebuffer export. They are actual 220×128 frames produced by the production Ultimate renderer.

- production UI source: `a99c3106b3968acbe45048a906f23271b2f58a63`
- capture harness source: `5b4c731851899ce33faa292f0ef7617e0ae6b1ac`
- capture application SHA-256: `3D6E522AA4356B84B4EE153F5CD33DE352FFA6267E47514C1B3A11C638BA5EB2`
- wire format: 220×128 little-endian RGB565 with a CRC32-checked header and trailer
- published scaling: 4× nearest-neighbor; no smoothing, recoloring, or compositing
- demo content: sanitized local messages, radio names, and RF statistics created only for capture

The capture harness is not part of either production firmware image. After capture, its isolated `/np/` demo history was cleared and the qualification unit's saved NVS, OTA metadata, and SPIFFS were restored byte-for-byte with its production Ultimate Web application. Every restored region passed flash verification before the device rejoined its LAN.
