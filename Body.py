class Body:
    def __init__(self, mass, heat_capacity, temperature):
        if mass <= 0:
            print("Warning: mass should be greater than 0.")
        if heat_capacity <= 0:
            print("Warning: heat capacity should be greater than 0.")
        if temperature < 0:
            print("Warning: temperature should be 0 or greater.")
        self.mass = mass
        self.heat_capacity = heat_capacity
        self.temperature = temperature

    def add_heat(self, heat_joules):
        delta_temperature = heat_joules / (self.mass * self.heat_capacity)
        self.temperature += delta_temperature
        return self.temperature


if __name__ == "__main__":
    test_body = Body(mass=100, heat_capacity=0.15, temperature=200)
    test_body2 = Body(mass = -100,heat_capacity=0.15, temperature=200)
    test_body3 = Body(mass = 100,heat_capacity=-0.15, temperature=200)
    test_body4 = Body(mass = 100,heat_capacity=0.15, temperature=-200)
    print(test_body.add_heat(20))
    print(test_body.add_heat(-40))

    print(test_body2.add_heat(20))
    print(test_body2.add_heat(-40))

    print(test_body3.add_heat(20))
    print(test_body3.add_heat(-40))
    
    