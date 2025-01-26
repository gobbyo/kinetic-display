@echo on
set PORT=%1
esptool --port %PORT% --baud 1000000 write_flash -z 0x1000 "firmware-LOLIN_S2_MINI-v1.23.0-604-g82e838b70.bin"