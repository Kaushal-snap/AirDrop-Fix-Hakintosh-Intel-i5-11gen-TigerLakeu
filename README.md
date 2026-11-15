# AirDrop Fix – Hackintosh with Intel Wi-Fi (Sequoia 15.8.x)

AirDrop on an Intel Wi-Fi card (tested: AX201, ASUS Vivobook K513EA, i5-1135G7, macOS Sequoia 15.8.3 / 24H241, OpenCore).
Mac must stay connected to Wi-Fi; AirDrop works both ways with the iPhone (iPhone Wi-Fi may be off).

This repo only contains an installer script and notes. The kexts are NOT included; they come from the upstream projects:
- ForbiddenItlwm (retropineaple) 0.5.4-beta.2, Sequoia build: https://github.com/retropineaple/ForbiddenItlwm/releases
- BTLEAdvFixup 0.9.1 (Sequoia build), from the same release / its dependencies page
- Also needed: Lilu, IntelBluetoothFirmware, BlueToolFixup

## Install
1. Download the two kexts (Sequoia builds) into a folder next to `install_airdrop.py`:
   `ForbiddenItlwm.kext`, `BTLEAdvFixup.kext`
2. Run (EFI of your boot disk or pendrive):
   `python3 install_airdrop.py /Volumes/<EFI>/EFI/OC`
3. The script backs up config and old kexts to `~/efi_backup/airdrop_<time>/`, copies the kexts, disables
   AirportItlwm / itlwm / IntelBTPatcher, inserts BTLEAdvFixup + ForbiddenItlwm after Lilu/BT kexts, and adds the boot flags.
4. Reset NVRAM, boot, join Wi-Fi, wait a minute, then check:
   `ioreg -l -w0 | grep -E '"ItlwmAWDL(InterfaceBuild|BuildCheck)"|"ITLAWDLCoex(Added|Channel|CountryLearned)"'`
   Expected: BuildCheck `verified`, Added Yes, Channel 149, CountryLearned Yes.
5. iPhone: AirDrop "Everyone for 10 Minutes".

## Notes
- Beta driver running in the kernel: panic risk. Roll back with the backed-up config.plist.
- Without a Wi-Fi connection AWDL never syncs (no AW start event); this is a limitation of the driver design.
- If Wi-Fi drops, remove `-itlawdlcoexmulti`. Router on channel 36–48 or 157 gives better Mac->iPhone speed.
- Before updating macOS, boot once without `-btleadv`.
- Keep your SMBIOS (serial/MLB/UUID/ROM) private; never upload your config.plist.

Credits: retropineaple (ForbiddenItlwm), acidanthera (Lilu, BTLEAdvFixup), OpenIntelWireless.