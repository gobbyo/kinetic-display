import sys
import time
import secrets

from common.config import Config
from picowifiserver import PicoWifi
from syncRTC import syncRTC

CONFIG_FILE = "config.json"
NTP_HOST = "pool.ntp.org"
MIN_VALID_YEAR = 2024
NTP_PORT = 123
NTP_TIMEOUT_SECONDS = 5


def get_network_module():
    return __import__("network")


def create_rtc():
    machine_module = __import__("machine")
    return machine_module.RTC()


def ensure_pico_w_runtime():
    if sys.platform != "rp2":
        raise RuntimeError("This test must run on Raspberry Pi Pico W (expected sys.platform == 'rp2').")

    network_module = get_network_module()
    if not hasattr(network_module, "WLAN") or not hasattr(network_module, "STA_IF"):
        raise RuntimeError("network.WLAN STA mode is unavailable; Pico W Wi-Fi hardware/runtime is required.")


def verify_rtc_hardware(rtc):
    probe_time = (2030, 1, 2, 2, 3, 4, 5, 0)
    rtc.datetime(probe_time)
    readback = rtc.datetime()

    if readback[0] != probe_time[0] or readback[1] != probe_time[1] or readback[2] != probe_time[2]:
        raise RuntimeError("RTC hardware write/readback failed.")


def verify_network_ntp_reachability(host, timeout_seconds=NTP_TIMEOUT_SECONDS):
    try:
        socket = __import__("usocket")
    except ImportError:
        socket = __import__("socket")

    addr_info = socket.getaddrinfo(host, NTP_PORT, 0, socket.SOCK_DGRAM)
    if not addr_info:
        raise RuntimeError("DNS resolution for NTP host failed.")

    ntp_address = addr_info[0][-1]
    request = bytearray(48)
    request[0] = 0x1B

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        udp_socket.settimeout(timeout_seconds)
        udp_socket.sendto(request, ntp_address)
        response, _ = udp_socket.recvfrom(48)
    finally:
        udp_socket.close()

    if len(response) < 48:
        raise RuntimeError("Invalid NTP response payload.")

    return ntp_address


def ensure_wifi_connected(wifi_client):
    network_module = get_network_module()
    connected = wifi_client.connect_to_wifi_network()
    if not connected:
        raise RuntimeError("Failed to connect to Wi-Fi using credentials in secrets.py.")

    wlan = network_module.WLAN(network_module.STA_IF)
    if not wlan.isconnected():
        raise RuntimeError("Wi-Fi reported disconnected after connection attempt.")

    return wlan.ifconfig()[0]


def validate_synced_datetime(datetime_tuple):
    if datetime_tuple[0] < MIN_VALID_YEAR:
        raise RuntimeError("RTC year is not valid after sync: {}".format(datetime_tuple[0]))


def run_sync_rtc_hardware_test():
    print("\n=== syncRTC Hardware + Network Integration Test ===")
    ensure_pico_w_runtime()

    config = Config(CONFIG_FILE)
    timezone = config.read("timeZone", default=None)
    timezone_display = timezone if timezone else "None (UTC expected)"
    print("Configured timezone: {}".format(timezone_display))

    rtc = create_rtc()
    verify_rtc_hardware(rtc)
    rtc.datetime((1970, 1, 1, 0, 0, 0, 0, 0))

    wifi_client = PicoWifi(CONFIG_FILE, secrets.usr, secrets.pwd)
    try:
        local_ip = ensure_wifi_connected(wifi_client)
        print("Wi-Fi connected. Local IP: {}".format(local_ip))

        ntp_address = verify_network_ntp_reachability(NTP_HOST)
        print("NTP server reachable at {}".format(ntp_address))

        rtc_sync = syncRTC(config)
        sync_ok = rtc_sync.syncclock(rtc, max_retries=3, ntp_host=NTP_HOST)
        if not sync_ok:
            raise RuntimeError("syncRTC.syncclock() returned False.")

        synced_time = rtc.datetime()
        validate_synced_datetime(synced_time)
        print("RTC after sync: {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            synced_time[0], synced_time[1], synced_time[2],
            synced_time[4], synced_time[5], synced_time[6]
        ))

        print("RESULT: PASS")

    finally:
        try:
            wifi_client.disconnect_from_wifi_network()
        except Exception as disconnect_error:
            print("Wi-Fi disconnect warning: {}".format(disconnect_error))


if __name__ == "__main__":
    try:
        run_sync_rtc_hardware_test()
    except Exception as test_error:
        print("RESULT: FAIL - {}".format(test_error))
        raise
