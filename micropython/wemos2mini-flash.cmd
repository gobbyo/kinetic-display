@echo on
set PORT=%1
esptool --port %PORT% erase_flash