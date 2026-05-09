class SignalController:
    def get_green_time(self, vehicles):
        return min(60, 10 + vehicles * 2)
