from pyModbusTCP.client import ModbusClient
from time import sleep
from dbhandler import DBHandler
from datetime import datetime


class ModbusPersistencia(object):
  """
  Classe que implementa funcionalidade de persistência de dados 
  lidos a partir do protocolo Modbus e também permite a busca de dados históricos
  """

  def __init__(self, server_ip, porta, tags_addrs, scan_time=1):
    """
    Construtor
    """
    self._cliente = ModbusClient(host=server_ip, port=porta)
    self._scan_time = scan_time
    self._tags_addrs = tags_addrs
    self._dbclient = DBHandler(
        'data\data.db', self._tags_addrs.keys(), 'modbusData')
    self._threads = []

  def guardar_dados(self):
    """
    Método para leitura de um dado da tabela MODBUS
    """
    try:
      self._cliente.open()
      data = {}
      while True:
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        for tag in self._tags_addrs:
          data[tag] = self._cliente.read_holding_registers(
              self._tags_addrs[tag], 1)[0]
        self._dbclient.insert_data(data)
        sleep(self._scan_time)
    except Exception as e:
      print("Erro na persistência dos dados: ", e.args)

  def acesso_dados_historicos(self, key, init, final):
    """
    Método que permite ao usuário acessar dados históricos
    """
    try:
      init = datetime.strptime(
          init, '%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
      final = datetime.strptime(
          final, '%d/%m/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
      result = self._dbclient.select_data([key], init, final)
      return result

    except Exception:
      return None
