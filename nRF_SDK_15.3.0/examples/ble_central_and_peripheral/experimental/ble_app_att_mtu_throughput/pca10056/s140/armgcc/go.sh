printf "r\nsavebin _build/downloaded_test.bin 0x3000 0x10\nexit\n" > _build/test-softdevice.jlink
touch _build/downloaded_test.bin
JLinkExe -device nrf52840_xxaa -if swd -speed 4000 _build/test-softdevice.jlink
arm-none-eabi-objcopy -Iihex -Obinary /home/aaron/School/CS_397_WirelessIOT/nu-wirelessiot-base/software/nrf52x-base/sdk/nrf5_sdk_15.3.0/components/softdevice/s140/hex/s140_nrf52_6.1.1_softdevice.hex _build/softdevice_bin.bin
dd skip=12288 count=16 if=_build//softdevice_bin.bin of=_build/softdevice_test.bin bs=1
rm -f _build//softdevice_bin.bin
diff -q _build/downloaded_test.bin _build/softdevice_test.bin || make flash_softdevice
printf "r\n" > _build/flash.jlink
printf "loadfile _build/nrf52840_xxaa.hex \nr\ng\nexit\n" >> _build/flash.jlink
JLinkExe -device nrf52840_xxaa -if swd -speed 4000 _build/flash.jlink
