#!/usr/bin/env python3
import logging
import time
import simplepyble
from PIL import Image
from io import BytesIO
from idm_display import IDMDisplay

logging.basicConfig(level=logging.INFO)

SERVICE_UUID = "000000fa-0000-1000-8000-00805f9b34fb"
WRITE_CMD_UUID = "0000fa02-0000-1000-8000-00805f9b34fb"

class IDMDisplayWrapper:
    _frame_counter = 0
    _last_send_time = 0
    _notifications_enabled = False
    
    @staticmethod
    def send_frame(peripheral, pixels, size=(32, 32)):
        """Send frame using PNG compression with notification support"""
        current_time = time.time()
        IDMDisplayWrapper._frame_counter += 1
        
        # Enable notifications if not already enabled
        if not IDMDisplayWrapper._notifications_enabled:
            if IDMDisplay.enable_notifications(peripheral):
                IDMDisplayWrapper._notifications_enabled = True
                logging.info("Frame completion notifications enabled")
        
        # Create RGB image from pixels
        img = Image.new('RGB', size)
        if isinstance(pixels, dict):
            for (x, y), color in pixels.items():
                img.putpixel((x, y), color)
        else:
            img.putdata(pixels)
        
        # Convert to PNG for efficient BLE transfer
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        png_data = img_byte_arr.getvalue()
        
        # Create and send payloads
        payloads = IDMDisplay.create_image_payloads(png_data)
        chunks = [payloads[i:i + 512] for i in range(0, len(payloads), 512)]
        
        # Initialize display with notification-enabled header
        init_data = IDMDisplay.create_frame_header()
        peripheral.write_request(SERVICE_UUID, WRITE_CMD_UUID, bytes(init_data))
        
        # Send chunks
        for chunk in chunks:
            peripheral.write_request(SERVICE_UUID, WRITE_CMD_UUID, bytes(chunk))
            # No need for sleep delay since we'll wait for notification
        
        IDMDisplayWrapper._last_send_time = time.time()

if __name__ == "__main__":
    print("This is a library module. Run core.py instead.")


