from pyModbusTCP.server import DataBank, ModbusServer
from time import sleep
import random


class ServidorMODBUS():
  """
  Classe Servidor MODBUS
  """

  def __init__(self, host_ip, port):
    """
    Construtor
    """

    self._server = ModbusServer(host=host_ip, port=port, no_block=True)

  def run(self):
    """
     Execução do servidor
    """
    self._server.start()
    print("Servidor em execução")
    while True:
      self._server

      self._server.data_bank.set_holding_registers(
          1000, [random.randrange(400, 500)])  # temperatura
      self._server.data_bank.set_holding_registers(
          1001, [random.randrange(100000, 120000)])  # pressão
      self._server.data_bank.set_holding_registers(
          1002, [random.randrange(20, 40)])  # umidade
      self._server.data_bank.set_holding_registers(
          1003, [random.randrange(40, 100)])  # consumo

      print('======================')
      print("Tabela MODBUS")
      print(
          f'Holding Register \r\n R1000: {self._server.data_bank.get_holding_registers(1000)} \r\n R1001: {self._server.data_bank.get_holding_registers(1001)} \r\n R1002: {self._server.data_bank.get_holding_registers(1002)} \r\n R1003: {self._server.data_bank.get_holding_registers(1003)}')
      sleep(1)
