"""
Script para popular o banco de dados com dados de exemplo
para demonstração do Sistema de Gerenciamento de Frota
"""

import sqlite3
import datetime
from main import SistemaGerenciamentoFrota

def popular_dados_exemplo():
    """Popula o banco com dados de exemplo para demonstração"""
    
    print("Populando banco de dados com dados de exemplo...")
    
    # Inicializar sistema
    sistema = SistemaGerenciamentoFrota()
    
    # Viaturas de exemplo
    viaturas_exemplo = [
        ("PM-0001", "Chevrolet Tracker", 2022, "P. Militar", 15000),
        ("CBM-0001", "Mercedes Sprinter", 2020, "Corpo de Bombeiros", 45000),
        ("PC-0001", "Volkswagen Amarok", 2021, "P. Civil", 35000),
        ("PF-0001", "Ford Ranger", 2023, "P. Federal", 8000),
        ("PM-0002", "Honda CB 600", 2022, "P. Militar - ROCAM", 18000),
        ("PM-0003", "Hyundai Creta", 2023, "P. Militar - PROERD", 26500),
    ]
    
    # Cadastrar viaturas
    for num_vtr, modelo, ano, orgao, odometro in viaturas_exemplo:
        sistema.cadastrar_viatura(num_vtr, modelo, ano, orgao, odometro)
        print(f"Viatura {num_vtr} cadastrada")
    print()
    
    # Adicionar algumas atualizações de odômetro (simulando registros semanais)
    atualizacoes_odometro = [
        ("PM-0001", 15250, "Atualização semanal - patrulhamento urbano"),
        ("PM-0001", 15500, "Atualização semanal - operação especial"),
        ("BM-0002", 25300, "Atualização quinzenal - chamadas de emergência"),
        ("PC-0003", 35180, "Atualização semanal - investigações"),
        ("PF-0004", 8450, "Atualização mensal - operações federais"),
    ]
    
    for num_vtr, odometro, obs in atualizacoes_odometro:
        sistema.atualizar_odometro(num_vtr, odometro, obs)
        print(f"Odômetro {num_vtr} atualizado para {odometro:,} km")
    print()
    
    # Registrar algumas manutenções (para simular histórico)
    manutencoes_exemplo = [
        ("PM-0001", "Troca de Óleo", "Óleo 5W30 sintético, filtro original"),
        ("BM-0002", "Revisão Geral", "Revisão dos 25.000 km - tudo ok"),
        ("PC-0003", "Troca de Óleo", "Manutenção preventiva"),
        ("PC-0003", "Revisão de Freios", "Substituição de pastilhas dianteiras"),
        ("PF-0004", "Troca de Óleo", "Primeiro serviço do veículo"),
    ]
    
    for num_vtr, tipo, obs in manutencoes_exemplo:
        sistema.registrar_manutencao(num_vtr, tipo, obs)
        print(f"Manutenção '{tipo}' registrada para {num_vtr}")
    print()
    
    print("Dados de exemplo inseridos com sucesso no banco de dados.")
    

if __name__ == "__main__":
    popular_dados_exemplo()
