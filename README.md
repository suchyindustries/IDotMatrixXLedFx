# IDMxLedFX 🎨💡

**High-Performance Bridge Between LedFX and iDotMatrix LED Display**

Transform your iDotMatrix display into a blazing-fast LED visualizer with intelligent compression and optimization!

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LedFX Compatible](https://img.shields.io/badge/LedFX-Compatible-green.svg)](https://ledfx.app/)

## 🚀 What is IDMxLedFX?

IDMxLedFX is a **high-performance gateway** that connects [LedFX](https://ledfx.app/) to the **iDotMatrix 32x32 LED display**, enabling real-time audio-reactive visualizations with optimized frame rates and intelligent compression.

### 🎯 Key Features

- **⚡ Blazing Fast**: 20-30 FPS with intelligent PNG compression
- **🧠 Smart Optimization**: Automatic compression based on frame content
- **🔄 Frame Skip**: Skips identical frames for maximum efficiency  
- **📊 Real-time Stats**: Live FPS monitoring and compression analytics
- **🎨 Full Color**: 32x32 RGB matrix with 16.7M colors
- **🔌 Plug & Play**: Direct UDP connection to LedFX

## 🖥️ Compatible Display

**[iDotMatrix 32x32 Programmable LED Display](https://www.amazon.com/iDotMatrix-Programmable-Creative-Animations-Accessories/dp/B0CGJ57Y9M)**

Perfect for:
- Audio visualizations
- Ambient lighting
- Creative animations
- Real-time effects
- maaaany more

## 📦 Installation

### Prerequisites

1. **Python 3.7+**
2. **LedFX** installed and running
3. **iDotMatrix display** paired via Bluetooth

### Install Dependencies

```bash
pip install -r req.txt
```

### Requirements
```
numpy==2.3.2
pillow==11.3.0
simplepyble==0.10.3
```

## 🚀 Quick Start

### 1. Setup LedFX
- Install and configure [LedFX](https://ledfx.app/)
- Add a **WLED device** pointing to `127.0.0.1:21324`
- Configure 32x32 LED matrix (1024 pixels)

### 2. Update MAC Address
Edit `core_ultra_simple.py`:
```python
TARGET_MAC = "38:20:09:4D:FC:D4"  # Replace with your display's MAC
```

### 3. Run IDMxLedFX
```bash
python3 core_ultra_simple.py
```

### 4. Start Visualizing! 🎉
- Play music in LedFX
- Watch real-time visualizations on your iDotMatrix display
- Monitor FPS in console logs

## 📊 Expected Output

```
INFO:__main__:Simple LedFX receiver initialized on port 21324
INFO:__main__:Using Bluetooth adapter: hci0
INFO:__main__:Connecting to IDM-32x32 [38:20:09:4D:FC:D4]
INFO:__main__:Connection established! Starting Simple LedFX receiver...
INFO:__main__:FPS: 25.8
INFO:__main__:FPS: 27.1
INFO:__main__:FPS: 24.3
```

## 🛠️ Architecture

```
┌─────────┐    UDP     ┌─────────────┐    BLE      ┌─────────────┐
│  LedFX  │ ───────→   │ IDMxLedFX   │ ──────────→ │ iDotMatrix  │
│         │  Port      │             │ Optimized   │   Display   │
│         │  21324     │ • Compress  │ PNG Data    │   32x32     │
└─────────┘            │ • Optimize  │             └─────────────┘
                       │ • Monitor   │
                       └─────────────┘
```

## 🎮 Advanced Usage

### Custom Frame Rate
```python
UPDATE_INTERVAL = 0.04  # 25 FPS
UPDATE_INTERVAL = 0.033  # 30 FPS (default)
UPDATE_INTERVAL = 0.02   # 50 FPS (experimental)
```

### Bluetooth Adapter Selection
```python
# Auto-select first adapter
adapter = adapters[0]

# Manual selection
# adapter = adapters[1]  # Use second adapter
```

## 🔧 Troubleshooting

### Connection Issues
```bash
# Check Bluetooth
bluetoothctl scan on
bluetoothctl devices

# Check UDP port
netstat -an | grep 21324
```

### Low FPS
- **Dark scenes**: Should achieve 25-30 FPS
- **Colorful scenes**: Expect 15-25 FPS  
- **Below 10 FPS**: Check BLE connection strength

### No Display Output
1. Verify MAC address in code
2. Ensure iDotMatrix is powered and paired
3. Check LedFX WLED device configuration
4. Restart LedFX and IDMxLedFX

## 🏗️ Project Structure

```
IDMxLedFX/
├── core_ultra_simple.py    # Main application (recommended)
├── idm_display.py          # Display communication module
├── main.py                 # Display wrapper utilities
├── req.txt                 # Python dependencies
└── README.md               # This file
```

## 📈 Performance Tips

1. **Position matters**: Keep display close to Bluetooth adapter
2. **Dark themes**: Use darker color schemes for higher FPS
3. **USB extension**: Use USB extension cable for better BLE range
4. **Power cycle**: Restart display if connection becomes unstable

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

Areas for improvement:
- Additional LED matrix sizes
- More compression algorithms  
- WiFi connectivity option
- Audio-reactive effects

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Special Thanks

**iDotMatrix Community** - Inspiration from all the amazing projects:
- [Search results for "idotmatrix" repositories](https://github.com/search?q=idotmatrix&type=repositories)
- Every developer who contributed to iDotMatrix reverse engineering
- Open source community for making this possible

**Artificial Intelligence** - For helping optimize and debug this project
> *"AI made the impossible possible, and the complex simple."*

**LedFX Team** - For creating the amazing LED visualization software


> *"Last but not least, I wanna thank me
> I wanna thank me for believing in me
> I wanna thank me for doing all this hard work"* 
> 
> **— Snoop Dogg**

---

## 🌟 Show Your Support

If this project helped you create amazing LED visualizations, please:

⭐ **Star this repository**  
🐛 **Report issues**  
📢 **Share with the community**  
🤝 **Contribute improvements**

---

**Made with ❤️ for the LED universums**

*Happy visualizing! 🎨💫*
