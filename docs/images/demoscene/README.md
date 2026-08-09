# NeonPocketMC demo-scene capture

`neonpocket-splash.gif` is assembled from 27 direct 220×128 RGB565 framebuffer captures at 125 ms intervals from 0 through 3200 ms. Every frame passed an independent CRC32 check before it was written.

Capture provenance:

- Hardware: Heltec RCC6 + NV3001B TFT
- Stable USB identity: ESP32-C6 base MAC `f0:f5:bd:0b:aa:e0`
- Production source base: `n30nex/NeonPocketMC-RCC6` main `587f93bd783c67f7a2b507ae390d989eb2543322`
- Temporary capture branch: `7bfe635da14287df4a32232e101440d8effc7985`
- Exact diagnostic build: [GitHub Actions run 31342813438](https://github.com/n30nex/NeonPocketMC-RCC6/actions/runs/31342813438)
- Diagnostic app SHA-256: `0b3df86a99cc071680dbdbbbbc18c3625f1c68f2ef4a9ef46986a9d363fcf317`
- GIF dimensions: 660×384 (3× nearest-neighbor presentation of native 220×128 frames)
- GIF frames: 27
- GIF duration: 3870 ms including the final hold
- GIF SHA-256: `e73c95fb121059f6e30c1aa40d99e1d28bbdeb668c8a3c3d77e8c9763af3ff45`

The capture-only serial command and framebuffer export are absent from production BLE and Web/AP environments. The qualification RCC6 was restored to the physically tested production BLE app immediately after capture.
