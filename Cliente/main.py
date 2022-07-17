import numpy as np
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from threading import Thread
from modbuspersistencia import ModbusPersistencia
from datetime import datetime


class Client(BoxLayout):
  __tags_addrs: dict[str, int] = {
      'temperatura': 1000,
      'pressao': 1001,
      'umidade': 1002,
      'consumo': 1003,
  }
  __graph = None

  def connect(self) -> None:
    self.__ip = str(self.ids.ip.text or '')
    self.__port = int(self.ids.port.text or 0)
    try:
      self.__client = ModbusPersistencia(
          self.__ip, self.__port, self.__tags_addrs)
      self.ids.search.disabled = False
      self.ids.connect.disabled = True
      Thread(target=self.__client.guardar_dados, daemon=True).start()
    except Exception as e:
      print(e)

  def searchData(self) -> None:
    if (self.ids.address.text and self.ids.initialDate.text and self.ids.finalDate.text):
      addr = int(self.ids.address.text)
      key = list(self.__tags_addrs.keys())[
          list(self.__tags_addrs.values()).index(addr)]
      startDate = str(self.ids.initialDate.text)
      endDate = str(self.ids.finalDate.text)
      result = self.__client.acesso_dados_historicos(key, startDate, endDate)
      if (result):
        timestamps = [row[result['cols'].index(
            'timestamp')] for row in result['data']]
        values = [row[result['cols'].index(key)] for row in result['data']]
        self.buildGraph({'timestamps': timestamps, 'values': values}, key)

  def buildGraph(self, data: dict, key) -> None:
    if (self.__graph):
      self.__graph.parent.remove_widget(self.__graph)
      plt.clf()

    day = data['timestamps'][0][8:10] + '/' + \
        data['timestamps'][0][5:7] + '/' + data['timestamps'][0][0:4]
    hour = data['timestamps'][0][11:19]

    # NORMALIZAÇÃO DOS SEGUNDOS APÓS A HORA INICIAL
    timeToPlot = [datetime.strptime(
        timestamp[0:19], "%Y-%m-%d %H:%M:%S").timestamp() for timestamp in data['timestamps']]
    timeToPlot = [(time - timeToPlot[0]) for time in timeToPlot]

    plt.plot(np.array(timeToPlot), np.array(data['values']))
    plt.xlabel("Tempo (s)")
    plt.xlim(0, max(timeToPlot))
    plt.ylabel(key.capitalize())
    plt.ylim(0.95*min(data['values']), 1.05*max(data['values']))
    plt.title(f'{key.capitalize()} - {day}. Tempo a partir de {hour}')
    plt.grid(True, color='lightgray')
    self.__graph = FigureCanvasKivyAgg(plt.gcf())
    self.ids.window.add_widget(self.__graph)


class ClientApp(App):
  def build(self):
    return Client()


if __name__ == '__main__':
  Config.set('graphics', 'resizable', False)
  Config.write()
  Config.set('graphics', 'width', '1000')
  Config.set('graphics', 'heigth', '600')
  Config.write()

  ClientApp().run()
