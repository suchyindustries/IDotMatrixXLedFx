import socket
import logging
import time
import simplepyble
from main import IDMDisplayWrapper
import numpy as np

# Constants
UDP_PORT = 21324  # WLED UDP port
DISPLAY_SIZE = (32, 32)
NUM_PIXELS = DISPLAY_SIZE[0] * DISPLAY_SIZE[1]
TARGET_MAC = "38:20:09:4D:FC:D4"
UPDATE_INTERVAL = 0.033  # ~30fps

WLED_NOTIFIER_DNRGB = 4  # Direct RGB with start index

logging.basicConfig(level=logging.INFO)

class SimpleLEDReceiver:
    """Prosty, niezawodny odbiornik LedFX bez skomplikowanych funkcji"""

    def __init__(self, peripheral):
        self.peripheral = peripheral
        self.frame_buffer = np.zeros((DISPLAY_SIZE[1], DISPLAY_SIZE[0], 3), dtype=np.uint8)
        self.frame_count = 0
        self.last_fps_time = time.time()

        # Setup UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        self.sock.bind(("0.0.0.0", UDP_PORT))
        self.sock.setblocking(False)

        logging.info(f"Simple LedFX receiver initialized on port {UDP_PORT}")

    def process_wled_packet(self, data):
        """Process WLED UDP packet"""
        if len(data) < 4 or data[0] != WLED_NOTIFIER_DNRGB:
            return False

        try:
            start_index = (data[2] << 8) | data[3]
            rgb_data = data[4:]

            num_leds = len(rgb_data) // 3
            for i in range(num_leds):
                if start_index + i >= NUM_PIXELS:
                    break

                base = i * 3
                if base + 2 >= len(rgb_data):
                    continue

                x = (start_index + i) % DISPLAY_SIZE[0]
                y = (start_index + i) // DISPLAY_SIZE[0]

                if y < DISPLAY_SIZE[1]:
                    self.frame_buffer[y, x] = [rgb_data[base], rgb_data[base+1], rgb_data[base+2]]

            return True

        except Exception as e:
            logging.error(f"Error processing WLED packet: {e}")
            return False

    def send_frame_simple(self):
        """Wyślij ramkę używając sprawdzonej metody z main.py"""
        try:
            # Konwertuj ramkę do listy pikseli dla IDMDisplayWrapper
            pixels = [(int(r), int(g), int(b)) for r, g, b in self.frame_buffer.reshape(-1, 3)]

            # Użyj sprawdzonej metody z main.py
            IDMDisplayWrapper.send_frame(self.peripheral, pixels, size=DISPLAY_SIZE)
            return True

        except Exception as e:
            logging.error(f"Error sending frame: {e}")
            return False

    def run(self):
        """Main loop - prosty i niezawodny"""
        last_time = time.time()

        try:
            while True:
                current_time = time.time()

                if current_time - last_time >= UPDATE_INTERVAL:
                    frame_updated = False

                    # Process packets - do 10 naraz dla wydajności
                    packets_processed = 0
                    while packets_processed < 10:
                        try:
                            data, addr = self.sock.recvfrom(4096)
                            if self.process_wled_packet(data):
                                frame_updated = True
                            packets_processed += 1
                        except BlockingIOError:
                            break
                        except Exception as e:
                            logging.error(f"UDP receive error: {e}")
                            break

                    # Send frame if updated
                    if frame_updated:
                        if self.send_frame_simple():
                            self.frame_count += 1

                            if self.frame_count % 100 == 0:
                                fps = 100 / (current_time - self.last_fps_time)
                                logging.info(f"FPS: {fps:.1f}")
                                self.last_fps_time = current_time

                    last_time = current_time
                else:
                    # Dynamiczny sleep
                    sleep_time = UPDATE_INTERVAL - (current_time - last_time)
                    if sleep_time > 0:
                        time.sleep(min(sleep_time, 0.01))

        except KeyboardInterrupt:
            logging.info("Simple receiver interrupted by user")
        finally:
            self.cleanup()

    def cleanup(self):
        if hasattr(self, 'sock'):
            self.sock.close()

def main():
    # Standard BLE initialization (dokładnie jak w main.py)
    adapters = simplepyble.Adapter.get_adapters()
    if not adapters:
        logging.error("No Bluetooth adapters found.")
        return

    adapter = adapters[0]
    logging.info(f"Using Bluetooth adapter: {adapter.identifier()}")

    adapter.scan_for(2000)
    peripherals = adapter.scan_get_results()

    target_peripheral = None
    for p in peripherals:
        if p.address() == TARGET_MAC:
            target_peripheral = p
            break

    if not target_peripheral:
        logging.error(f"IDM display with MAC {TARGET_MAC} not found.")
        return

    logging.info(f"Connecting to {target_peripheral.identifier()} [{target_peripheral.address()}]")
    target_peripheral.connect()

    if not target_peripheral.is_connected():
        logging.error("Failed to connect to IDM display.")
        return

    logging.info("Connection established! Starting Simple LedFX receiver...")

    # Run the simple receiver
    receiver = SimpleLEDReceiver(target_peripheral)
    receiver.run()

    if target_peripheral.is_connected():
        target_peripheral.disconnect()
        logging.info("Disconnected from device")

if __name__ == "__main__":
    main()
