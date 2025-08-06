import time
import json
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_ds18x20
import adafruit_onewire.bus

# Initial sensors
# reading I2C for ADC
i2c = busio.I2C(board.SCL, board.SDA)

# read ADS1115
ads1 = ADS.ADS1115(i2c, address=0x48)
ads2 = ADS.ADS1115(i2c, address=0x49)

# read current sensors
chan_ir = AnalogIn(ads1, ADS.P0)
chan_is = AnalogIn(ads1, ADS.P1)
chan_it = AnalogIn(ads1, ADS.P2)
chan_in = AnalogIn(ads1, ADS.P3)

# read voltage sensors
chan_vrs = AnalogIn(ads2, ADS.P0)
chan_vst = AnalogIn(ads2, ADS.P1)
chan_vtr = AnalogIn(ads2, ADS.P2)
chan_vrn = AnalogIn(ads2, ADS.P3)

# read temp sensors DS18B20
ow_bus = adafruit_onewire.bus.OneWireBus(board.D4)
ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, ow_bus.scan()[0])

# read sensors data
def get_sensor_data():

    data = {
        "nama_trafo": "ULAZ2",
        "lokasi": "JL. GALANGAN KAPAL DP MESJID",
        "kapasitas_kva": 300,
        "timestamp": int(time.time()),
        "suhu": ds18b20.temperature,
        "arusR": chan_ir.voltage * 100,  
        "arusS": chan_is.voltage * 100,
        "arusT": chan_it.voltage * 100,
        "arusN": chan_in.voltage * 100,
        "tegRS": chan_vrs.voltage * 100,
        "tegST": chan_vst.voltage * 100,
        "tegTR": chan_vtr.voltage * 100,
        "tegRN": chan_vrn.voltage * 100
    }
    return data

# loop to get another data
while True:
    data_trafo = get_sensor_data()
    
    # save to txt
    with open("data_trafo.txt", "w") as f:
        json.dump(data_trafo, f, indent=4)
        
    print("Data updates!")
    time.sleep(60) 