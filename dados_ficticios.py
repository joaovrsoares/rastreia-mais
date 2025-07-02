"""
Script para popular o banco de dados com dados fictícios
Sistema de Gerenciamento de Frota - Demonstração
"""

import random
import datetime
import sqlite3
from main import SistemaGerenciamentoFrota

def popular_dados_exemplo():
    """Popula o banco com dados de exemplo"""
    
    print("Populando banco de dados com dados de exemplo...")
    print("=" * 50)
    
    # Inicializar sistema
    sistema = SistemaGerenciamentoFrota()
    
<<<<<<< HEAD
    # Viaturas de exemplo com dados 
    viaturas = [
        ("PM-0001", "Chevrolet Tracker", 2022, "P. Militar"),
        ("CBM-0001", "Mercedes Sprinter", 2020, "Corpo de Bombeiros"),
        ("PC-0001", "Volkswagen Amarok", 2021, "P. Civil"),
        ("PF-0001", "Ford Ranger", 2023, "P. Federal"),
        ("PM-0002", "Honda CB 600", 2022, "P. Militar - ROCAM"),
        ("PM-0003", "Hyundai Creta", 2023, "P. Militar - PROERD"),
=======
    # Viaturas de exemplo
    viaturas_exemplo = [
        ("PM-0001", "Chevrolet Tracker", 2022, "P. Militar", 15000),
        ("CBM-0001", "Mercedes Sprinter", 2020, "Corpo de Bombeiros", 45000),
        ("PC-0001", "Volkswagen Amarok", 2021, "P. Civil", 35000),
        ("PF-0001", "Ford Ranger", 2023, "P. Federal", 8000),
        ("PM-0002", "Honda CB 600", 2022, "P. Militar - ROCAM", 18000),
        ("PM-0003", "Hyundai Creta", 2023, "P. Militar - PROERD", 26500),
>>>>>>> be8ff95ede5ebdb0921998a2b25ac192dad7091a
    ]
    
    # 1. Cadastrar viaturas com odômetros aleatórios
    print("Cadastrando viaturas...")
    for num_vtr, modelo, ano, orgao in viaturas:
        # Gerar odômetro baseado na idade do veículo (10k-30k km por ano)
        idade = datetime.datetime.now().year - ano
        odometro_base = random.randint(10000, 30000) * idade
        if idade == 0:  # Veículo novo
            odometro_base = random.randint(1000, 8000)
        
        sistema.cadastrar_viatura(num_vtr, modelo, ano, orgao, odometro_base)
        print(f"  {num_vtr} - {modelo} ({odometro_base:,} km)")
    
    # 2. Registrar manutenções com odômetros específicos para criar alertas diversos
    print("\nRegistrando histórico de manutenções...")
    
    # Configurações específicas para cada viatura para criar alertas variados
    configuracoes_manutencao = [
        # (num_vtr, tipo, dias_atras, odometro_na_manutencao)
        ("PM-0001", "Troca de Óleo", 380, 25340),      # VENCIDO por DATA (>365 dias)
        ("CBM-0001", "Revisão Geral", 120, 28750),     # VENCIDO por KM (~11k km rodados)
        ("PC-0001", "Revisão de Freios", 350, 38950),  # URGENTE por DATA (~15 dias)
        ("PF-0001", "Troca de Óleo", 300, 22180),      # URGENTE por KM (~8k km rodados)
        ("PM-0002", "Revisão Geral", 160, 35650),      # ATENÇÃO por DATA (~20 dias)
        ("PM-0003", "Troca de Óleo", 200, 15750),      # ATENÇÃO por KM (~7.5k km rodados)
    ]
    
    for num_vtr, tipo, dias_atras, odometro_manutencao in configuracoes_manutencao:
        data_manutencao = datetime.datetime.now() - datetime.timedelta(days=dias_atras)
        
        # Ajustar temporariamente o odômetro para o valor na época da manutenção
        conn = sqlite3.connect("frota.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE viaturas SET odometro_atual = ? WHERE num_vtr = ?", 
                      (odometro_manutencao, num_vtr.upper()))
        conn.commit()
        conn.close()
        
        # Registrar a manutenção
        sistema.registrar_manutencao(num_vtr, tipo, data_manutencao, 
                                   f"Manutenção {tipo.lower()} realizada")
        print(f"  {num_vtr}: {tipo} (há {dias_atras} dias, {odometro_manutencao:,} km)")
    
    # 3. Atualizar odômetros para valores atuais 
    print("\nAtualizando odômetros atuais...")
    observacoes = [
        "Patrulhamento urbano", "Operação especial", "Chamadas de emergência", 
        "Investigações", "Operações federais", "Ronda escolar"
    ]
    
    # Odômetros atuais calculados para criar os alertas desejados
    odometros_atuais = [
        ("PM-0001", 26890),  # +1550 km desde manutenção
        ("CBM-0001", 39850), # +11100 km desde manutenção (VENCIDO por KM)
        ("PC-0001", 58920),  # +19970 km desde manutenção (próximo do limite)
        ("PF-0001", 30280),  # +8100 km desde manutenção (URGENTE por KM)
        ("PM-0002", 42150),  # +6500 km desde manutenção
        ("PM-0003", 23380),  # +7630 km desde manutenção
    ]
    
    for num_vtr, odometro_atual in odometros_atuais:
        # Simular algumas atualizações
        for i in range(random.randint(2, 4)):
            incremento = random.randint(100, 400)
            obs = random.choice(observacoes)
            sistema.atualizar_odometro(num_vtr, incremento, obs)
        
        # Definir odômetro final específico
        conn = sqlite3.connect("frota.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE viaturas SET odometro_atual = ? WHERE num_vtr = ?", 
                      (odometro_atual, num_vtr.upper()))
        conn.commit()
        conn.close()
        
        print(f"  {num_vtr}: {odometro_atual:,} km")
    
    print("\n" + "=" * 50)
    print("Dados de exemplo inseridos com sucesso!")


if __name__ == "__main__":
    popular_dados_exemplo()
