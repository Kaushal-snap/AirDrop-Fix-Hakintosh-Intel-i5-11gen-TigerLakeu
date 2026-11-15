#!/usr/bin/env python3
"""Install ForbiddenItlwm (Sequoia 15.8.x) + BTLEAdvFixup into an OpenCore EFI and edit config.plist.
Usage:  python3 install_airdrop.py /Volumes/1401/EFI/OC
Everything it replaces is backed up to ~/efi_backup/airdrop_<time>/ first."""
import os, sys, shutil, time, plistlib

oc = sys.argv[1].rstrip('/')
here = os.path.dirname(os.path.abspath(__file__))
cfg = os.path.join(oc, 'config.plist')
kexts = os.path.join(oc, 'Kexts')
assert os.path.isfile(cfg) and os.path.isdir(kexts), 'not an OpenCore folder: ' + oc

bk = os.path.expanduser('~/efi_backup/airdrop_' + time.strftime('%H%M%S'))
os.makedirs(bk)
shutil.copy(cfg, bk)
print('backup folder:', bk)

# 1. kexts
for k in ('ForbiddenItlwm.kext', 'BTLEAdvFixup.kext'):
    dst = os.path.join(kexts, k)
    if os.path.exists(dst):
        shutil.move(dst, os.path.join(bk, k))
    shutil.copytree(os.path.join(here, k), dst)
for old in ('AirportItlwm.kext', 'itlwm.kext'):
    src = os.path.join(kexts, old)
    if os.path.exists(src):
        shutil.copytree(src, os.path.join(bk, old))   # keep a copy; folder stays, entry is disabled below
os.system('xattr -cr "%s" "%s" 2>/dev/null' % (os.path.join(kexts, 'ForbiddenItlwm.kext'), os.path.join(kexts, 'BTLEAdvFixup.kext')))

# 2. config.plist
p = plistlib.load(open(cfg, 'rb'))
add = p['Kernel']['Add']
names = [e['BundlePath'] for e in add]
print('kext order before:', names)
for e in add:
    if e['BundlePath'] in ('AirportItlwm.kext', 'itlwm.kext', 'IntelBTPatcher.kext'):
        e['Enabled'] = False
add[:] = [e for e in add if e['BundlePath'] not in ('ForbiddenItlwm.kext', 'BTLEAdvFixup.kext')]
need = ('Lilu.kext', 'IntelBluetoothFirmware.kext', 'BlueToolFixup.kext')
pos = max(i for i, e in enumerate(add) if e['BundlePath'] in need) + 1
tmpl = next(e for e in add if e['BundlePath'] == 'Lilu.kext')
def entry(name, comment):
    e = dict(tmpl)
    e.update({'BundlePath': name, 'Comment': comment, 'Enabled': True,
              'ExecutablePath': 'Contents/MacOS/' + name[:-5], 'PlistPath': 'Contents/Info.plist',
              'MinKernel': '24.0.0', 'MaxKernel': '24.99.99'})
    return e
add.insert(pos, entry('BTLEAdvFixup.kext', 'AirDrop BLE advertising (Sequoia)'))
add.insert(pos + 1, entry('ForbiddenItlwm.kext', 'Intel Wi-Fi + AirDrop (Sequoia)'))
print('kext order after: ', [e['BundlePath'] + ('' if e['Enabled'] else '(off)') for e in add])

flags = ('-btleadv -itlawdlcoexprobe -itlawdliface -itlawdlnativeup -itlawdlcoexrx -itlawdlcoextx '
         '-itlawdlcoexmulti -itlawdlcoexdata -itlawdlmitx -itlawdlelicit -itlawdlcaps -itlawdlsvcmerge '
         '-itlawdlawsync itlawdlintcoal=4 -itlawdlcoexbatx -itlawdlcoexpeerpause -itlawdlcoexbatrace '
         'itlawdltxqueue=4096').split()
g = p['NVRAM']['Add']['7C436110-AB2A-4BBB-A880-FE41995C9F82']
cur = g['boot-args'].split()
g['boot-args'] = ' '.join(cur + [f for f in flags if f not in cur])
print('boot-args:', g['boot-args'])
dele = p['NVRAM']['Delete']['7C436110-AB2A-4BBB-A880-FE41995C9F82']
assert 'boot-args' in dele, 'boot-args must be in NVRAM > Delete for this GUID'

plistlib.dump(p, open(cfg, 'wb'), sort_keys=False)
print('done. Reset NVRAM, boot from this stick, join Wi-Fi.')
