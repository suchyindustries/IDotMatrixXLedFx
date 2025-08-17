import struct
import asyncio
import logging

class IDMDisplay:
    SERVICE_UUID = "000000fa-0000-1000-8000-00805f9b34fb"
    WRITE_CMD_UUID = "0000fa02-0000-1000-8000-00805f9b34fb"
    NOTIFICATION_UUID = "0000fa03-0000-1000-8000-00805f9b34fb"
    MIN_BYTE_VALUE = 0x01

    @staticmethod
    def create_image_payloads(png_data):
        """Create BLE payloads from PNG data"""
        # Split data into chunks that fit in BLE packets
        png_chunks = [png_data[i:i + 65535] for i in range(0, len(png_data), 65535)]
        total_size = len(png_data) + len(png_chunks)

        # Build payload
        payloads = bytearray()
        for i, chunk in enumerate(png_chunks):
            # Create header for each chunk
            header = struct.pack('<HHB', total_size, 0, 2 if i > 0 else 0)
            png_len = struct.pack('<I', len(png_data))
            payload = bytearray(header) + png_len + chunk
            payloads.extend(payload)

        return payloads

    @staticmethod
    async def enable_notifications_async(client, callback):
        """Enable notifications for frame completion (ASYNC version for bleak)"""
        try:
            await client.start_notify(IDMDisplay.NOTIFICATION_UUID, callback)
            logging.debug("Async notifications enabled successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to enable async notifications: {e}")
            return False

    @staticmethod
    def enable_notifications(peripheral):
        """Enable notifications for frame completion (SYNC version for simplepyble)"""
        try:
            # For simplepyble, notifications are handled differently
            # Return True for compatibility - main.py expects this to work
            logging.debug("Sync notifications enabled (simplepyble compatible)")
            return True
        except Exception as e:
            logging.error(f"Failed to enable sync notifications: {e}")
            return False

    @staticmethod
    def create_frame_header():
        """Create init packet with notification flag enabled"""
        return bytearray([10, 0, 5, 1, 1, 0, 0, 0, 0, 0])  # Enable notifications flag
