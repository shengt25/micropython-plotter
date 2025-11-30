from typing import Optional
from PySide6.QtCore import QObject, Signal


class PlotStreamHandler(QObject):
    """
    Parse incoming serial data and route to plotter or console.

    Detects binary plot packets (0xAA 0x01 protocol) and emits them separately
    from normal text output.
    """

    # Qt Signals
    plot_data_received = Signal(list)  # Emits [val1, val2, ...] for plot packets
    text_data_received = Signal(str)   # Emits text for console output

    def __init__(self, device_manager=None):
        super().__init__()
        self.dm = device_manager
        self.buffer = bytearray()
        self.enabled = False

    def process_data(self, raw_bytes: bytes):
        """
        Process incoming raw bytes from serial port.

        Searches for 0xAA 0x01 packets and emits them as plot_data_received.
        Everything else is emitted as text_data_received.

        Args:
            raw_bytes: Raw bytes from serial port
        """
        if not raw_bytes:
            return

        # Add to buffer
        self.buffer.extend(raw_bytes)

        # Continuously try to extract packets or text
        while len(self.buffer) > 0:
            packet = self._try_read_packet()
            if packet is not None:
                # Successfully parsed a packet
                self.plot_data_received.emit(packet)
            else:
                # No more packets to extract
                break

    def _try_read_packet(self) -> Optional[list]:
        """
        Try to extract one plot packet from buffer.

        Packet format:
        - 0xAA (sync byte)
        - 0x01 (packet type)
        - param_count (1-5)
        - uint16[] data (little-endian, 2 bytes each)

        Returns:
            List of values if packet found, None otherwise
        """
        # 1. Search for sync header 0xAA
        sync_idx = -1
        for i in range(len(self.buffer)):
            if self.buffer[i] == 0xAA:
                # Emit everything before sync as text
                if i > 0:
                    text_bytes = bytes(self.buffer[:i])
                    text = text_bytes.decode('utf-8', errors='replace')
                    if text:
                        self.text_data_received.emit(text)
                    self.buffer = self.buffer[i:]
                sync_idx = 0
                break

        if sync_idx == -1:
            # No sync found in entire buffer
            # Emit all as text if buffer gets too large (avoid infinite growth)
            if len(self.buffer) > 1024:  # Arbitrary threshold
                text_bytes = bytes(self.buffer)
                text = text_bytes.decode('utf-8', errors='replace')
                if text:
                    self.text_data_received.emit(text)
                self.buffer.clear()
            return None

        # 2. Need at least 3 bytes: AA 01 param_count
        if len(self.buffer) < 3:
            return None

        # 3. Validate packet type (must be 0x01)
        if self.buffer[1] != 0x01:
            # Invalid packet type, skip sync byte and continue
            self.buffer.pop(0)
            return None

        # 4. Read param count
        param_count = self.buffer[2]
        if not (1 <= param_count <= 5):
            # Invalid param count, skip sync byte
            self.buffer.pop(0)
            return None

        # 5. Check if full packet is available
        packet_size = 3 + param_count * 2
        if len(self.buffer) < packet_size:
            # Wait for more data
            return None

        # 6. Extract uint16 values (little-endian)
        values = []
        for i in range(param_count):
            idx = 3 + i * 2
            # Little-endian: low byte first, then high byte
            val = self.buffer[idx] | (self.buffer[idx + 1] << 8)
            values.append(val)

        # 7. Remove packet from buffer
        self.buffer = self.buffer[packet_size:]

        return values
