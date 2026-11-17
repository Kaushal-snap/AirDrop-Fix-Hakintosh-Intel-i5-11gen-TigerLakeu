<div align="center">

# Intel Wi-Fi AirDrop · Hackintosh

**Tiger Lake-U · ASUS VivoBook K513EA · macOS Sequoia**

![macOS](https://img.shields.io/badge/macOS-Sequoia%2015-7B61FF?style=for-the-badge&logo=apple)
![Wi-Fi](https://img.shields.io/badge/Wi--Fi-Intel-0071C5?style=for-the-badge&logo=intel)
![Status](https://img.shields.io/badge/Status-Experimental-orange?style=for-the-badge)

</div>

A helper script and setup notes for experimenting with AirDrop/AWDL on an Intel Wi-Fi Hackintosh. The original test notes identify an AX201 adapter in an ASUS VivoBook K513EA with an Intel Core i5-1135G7 and macOS Sequoia 15.8.3 (24H241).

This repository does not bundle third-party kext binaries. Obtain compatible builds from their upstream maintainers and review their licenses.

## Components referenced

- ForbiddenItlwm — Sequoia-compatible build from upstream
- BTLEAdvFixup
- Lilu
- IntelBluetoothFirmware
- BlueToolFixup

Confirm current upstream release notes and dependency requirements before installing. Historical version numbers may be outdated.

## Installation outline

1. Back up the EFI you actually boot and prepare a separate USB test EFI.
2. Obtain required kexts from their official upstream release pages.
3. Place the expected kext bundles beside `install_airdrop.py`.
4. Review the script and confirm its target OpenCore directory.
5. Run:

```bash
python3 install_airdrop.py /Volumes/<EFI>/EFI/OC
```

6. Inspect the resulting `config.plist` and kext order before rebooting.
7. Reset NVRAM only if required by the configuration and verify Wi-Fi, Bluetooth and AirDrop separately.

## Diagnostics

The original test notes use:

```bash
ioreg -l -w0 | grep -E '"ItlwmAWDL(InterfaceBuild|BuildCheck)"|"ITLAWDLCoex(Added|Channel|CountryLearned)"'
```

Values such as build verification and coexistence state are historical test expectations, not guarantees on other versions or hardware.

## Known limitations and risks

- The referenced ForbiddenItlwm build was a beta; kernel panics and regressions are possible.
- AWDL depends on the Wi-Fi driver, Bluetooth stack, macOS build and router environment.
- The original notes describe a requirement to remain connected to Wi-Fi for AWDL synchronization.
- Router channel suggestions are environment-specific, not universal fixes.

## Privacy

Never publish `SystemSerialNumber`, `MLB`, `SystemUUID`, `ROM`, Wi-Fi credentials, personal identifiers, or unredacted diagnostic logs.

## Contributing

Include exact hardware IDs, macOS build, OpenCore version and sanitized logs. Describe the tested hardware/software combination.

## Disclaimer

Experimental Hackintosh community project. No warranty is provided. Keep a known-good EFI backup and follow upstream licenses and documentation.
