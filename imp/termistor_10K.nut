function thermister(raw_adc) {
    server.log(raw_adc);
    local temp = math.log(((655350000/raw_adc) - 10000));
    server.log(temp);
    temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * temp * temp ))* temp );
    server.log(temp);
    temp = temp - 273.15;
    return temp;
}

local output = OutputPort("Temperature", "number");

imp.configure("Termistor 10K", [], [output]);

hardware.pin9.configure(ANALOG_IN);

while(true){
    local temp = thermister(hardware.pin9.read());
    output.set(temp);
    server.show(format("%1.1fºC", temp));  
    server.log("sleep");
    imp.sleep(5.0);
}