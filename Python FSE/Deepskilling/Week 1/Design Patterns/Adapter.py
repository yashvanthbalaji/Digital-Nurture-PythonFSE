class OldCharger:
    def old_charge(self):
        print("Charging with Old Charger")


class ChargerAdapter:
    def __init__(self, charger):
        self.charger = charger

    def charge(self):
        self.charger.old_charge()


old_charger = OldCharger()

adapter = ChargerAdapter(old_charger)

adapter.charge()