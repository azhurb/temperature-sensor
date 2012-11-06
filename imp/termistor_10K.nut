class Termistor
{
    constructor(pin){
        hardware["pin" + pin].configure(ANALOG_IN);
    }
    
    function read(){
        return hardware.pin9.read();
    }
    
    function getTemperature(){
        local temp = math.log(((655350000/read()) - 10000));
        temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * temp * temp ))* temp );
        temp = temp - 273.15;
        return temp;
    }
}

local sensor = Termistor(9);

local output = OutputPort("Temperature", "number");

imp.configure("Termistor 10K", [], [output]);

function capture(){
    imp.wakeup(5, capture);
    local temp = sensor.getTemperature();
    output.set(temp);
    server.show(format("%1.1fºC", temp));
}

imp.configure("Termistor 10K", [], [output]);

capture();
