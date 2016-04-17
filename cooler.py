import smbus
import time
import json
import urllib2
import urllib
import requests

range = 200
bus = smbus.SMBus(1)
# I2C address 0x29
# Register 0x12 has device ver.
# Register addresses must be OR'ed with 0x80
bus.write_byte(0x29,0x80|0x12)
ver = bus.read_byte(0x29)
# version # should be 0x44
if ver == 0x44:
    print "Device found\n"
    bus.write_byte(0x29, 0x80|0x00) # 0x00 = ENABLE register
    bus.write_byte(0x29, 0x01|0x02) # 0x01 = Power on, 0x02 RGB sensors enabled
    bus.write_byte(0x29, 0x80|0x14) # Reading results start register 14, LSB then MSB
    data = bus.read_i2c_block_data(0x29, 0)
    original_clear = clear = data[1] << 8 | data[0]
    original_red = data[3] << 8 | data[2]
    original_green = data[5] << 8 | data[4]
    original_blue = data[7] << 8 | data[6]
    while True:
        data = bus.read_i2c_block_data(0x29, 0)
        clear = clear = data[1] << 8 | data[0]
        red = data[3] << 8 | data[2]
        green = data[5] << 8 | data[4]
        blue = data[7] << 8 | data[6]
        crgb = "C: %s, R: %s, G: %s, B: %s\n" % (int(round(clear,-2)), int(round(red,-2)), int(round(green,-2)), int(round(blue,-2)))
        print crgb
        time.sleep(.5)
        # this sends the color profile when a change is detected
        if clear < (original_clear - range) or clear > (original_clear + range):
            input_data = { 'unit_id': '1',
                           'c_value': int(round(clear, -2)),
                           'r_value': int(round(red, -2)),
                           'g_value': int(round(green, -2)),
                           'b_value': int(round(blue, -2))
                         }
            url = "https://coolscandeluxe.herokuapp.com/datadump"
            r = requests.post(url, data=json.dumps(input_data),
                              headers={'Content-Type': 'application/json'})
            response = r.text
            print response
            time.sleep(2)
            data = bus.read_i2c_block_data(0x29, 0)
            original_clear = clear = data[1] << 8 | data[0]
            original_red = data[3] << 8 | data[2]
            original_green = data[5] << 8 | data[4]
            original_blue = data[7] << 8 | data[6]
    else:
        print "Device not Found"
