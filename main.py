"""RASTREIA+ - Sistema de Gerenciamento de Frota
Desenvolvido para órgãos governamentais e militares
A ser exibido em seminário do curso de Ciência da Computação
"""

import sqlite3
import datetime
from typing import List, Tuple, Optional

class SistemaGerenciamentoFrota:
    def __init__(self, db_name: str = "frota.db"):
        """Inicializa o sistema e cria o banco de dados"""
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Cria as tabelas necessárias no banco de dados"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Tabela de viaturas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS viaturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_vtr TEXT UNIQUE NOT NULL,
                modelo TEXT NOT NULL,
                ano INTEGER NOT NULL,
                orgao TEXT NOT NULL,
                odometro_atual INTEGER DEFAULT 0,
                data_cadastro TEXT NOT NULL,
                ativa BOOLEAN DEFAULT 1
            )
        ''')
        
        # Tabela de registros de odômetro
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros_odometro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                viatura_id INTEGER NOT NULL,
                odometro INTEGER NOT NULL,
                data_registro TEXT NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (viatura_id) REFERENCES viaturas (id)
            )
        ''')
        
        # Tabela de tipos de manutenção
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tipos_manutencao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                intervalo_km INTEGER NOT NULL,
                intervalo_dias INTEGER NOT NULL,
                descricao TEXT
            )
        ''')
        
        # Tabela de manutenções realizadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS manutencoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                viatura_id INTEGER NOT NULL,
                tipo_manutencao_id INTEGER NOT NULL,
                odometro_realizada INTEGER NOT NULL,
                data_realizada TEXT NOT NULL,
                proximo_odometro INTEGER NOT NULL,
                proxima_data TEXT NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (viatura_id) REFERENCES viaturas (id),
                FOREIGN KEY (tipo_manutencao_id) REFERENCES tipos_manutencao (id)
            )
        ''')
        
        conn.commit()
        
        # Inserir tipos de manutenção padrão se não existirem
        self._inserir_tipos_manutencao_padrao(cursor)
        conn.commit()
        conn.close()
    
    def _inserir_tipos_manutencao_padrao(self, cursor):
        """Insere os tipos de manutenção padrão no sistema"""
        tipos_padrao = [
            ("Revisão Geral", 10000, 180, "Revisão completa do veículo"),
            ("Troca de Óleo", 10000, 365, "Troca de óleo do motor e filtro"),
            ("Troca de Filtro de Ar", 10000, 365, "Substituição do filtro de ar"),
            ("Revisão de Freios", 20000, 365, "Verificação e manutenção do sistema de freios"),
            ("Troca de Pneus", 40000, 1095, "Substituição dos pneus"),
            ("Troca de Bateria", 60000, 1460, "Substituição da bateria")
        ]
        
        for nome, km, dias, desc in tipos_padrao:
            cursor.execute('''
                INSERT OR IGNORE INTO tipos_manutencao (nome, intervalo_km, intervalo_dias, descricao)
                VALUES (?, ?, ?, ?)
            ''', (nome, km, dias, desc))
    
    def cadastrar_viatura(self, num_vtr: str, modelo: str, ano: int, orgao: str, odometro_inicial: int = 0) -> bool:
        """Cadastra uma nova viatura no sistema"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''
                INSERT INTO viaturas (num_vtr, modelo, ano, orgao, odometro_atual, data_cadastro)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (num_vtr.upper(), modelo, ano, orgao, odometro_inicial, data_atual))
            
            viatura_id = cursor.lastrowid
            
            # Registrar odômetro inicial
            if odometro_inicial > 0:
                cursor.execute('''
                    INSERT INTO registros_odometro (viatura_id, odometro, data_registro, observacoes)
                    VALUES (?, ?, ?, ?)
                ''', (viatura_id, odometro_inicial, data_atual, "Odômetro inicial no cadastro"))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def atualizar_odometro(self, num_vtr: str, novo_odometro: int, observacoes: str = "") -> bool:
        """Atualiza o odômetro de uma viatura"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Verificar se a viatura existe e obter odômetro atual
            cursor.execute('SELECT id, odometro_atual FROM viaturas WHERE num_vtr = ? AND ativa = 1', (num_vtr.upper(),))
            resultado = cursor.fetchone()
            
            if not resultado:
                conn.close()
                return False
            
            viatura_id, odometro_atual = resultado
            
            if novo_odometro < odometro_atual:
                conn.close()
                return False  # Odômetro não pode diminuir
            
            data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Atualizar odômetro na viatura
            cursor.execute('''
                UPDATE viaturas SET odometro_atual = ? WHERE id = ?
            ''', (novo_odometro, viatura_id))
            
            # Registrar a atualização
            cursor.execute('''
                INSERT INTO registros_odometro (viatura_id, odometro, data_registro, observacoes)
                VALUES (?, ?, ?, ?)
            ''', (viatura_id, novo_odometro, data_atual, observacoes))
            
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False
    
    def registrar_manutencao(self, num_vtr: str, tipo_manutencao: str, data_manutencao: datetime.datetime, observacoes: str = "") -> bool:
        """Registra uma manutenção realizada"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Obter dados da viatura
            cursor.execute('SELECT id, odometro_atual FROM viaturas WHERE num_vtr = ? AND ativa = 1', (num_vtr.upper(),))
            viatura_resultado = cursor.fetchone()
            
            if not viatura_resultado:
                conn.close()
                return False
            
            viatura_id, odometro_atual = viatura_resultado
            
            # Obter dados do tipo de manutenção
            cursor.execute('SELECT id, intervalo_km, intervalo_dias FROM tipos_manutencao WHERE nome = ?', (tipo_manutencao,))
            tipo_resultado = cursor.fetchone()
            
            if not tipo_resultado:
                conn.close()
                return False
            
            tipo_id, intervalo_km, intervalo_dias = tipo_resultado
            
            # Usar a data recebida como parâmetro
            data_str = data_manutencao.strftime("%Y-%m-%d %H:%M:%S")
            
            # Calcular próxima manutenção
            proximo_odometro = odometro_atual + intervalo_km
            proxima_data = data_manutencao + datetime.timedelta(days=intervalo_dias)
            proxima_data_str = proxima_data.strftime("%Y-%m-%d %H:%M:%S")
            
            # Registrar manutenção
            cursor.execute('''
                INSERT INTO manutencoes (viatura_id, tipo_manutencao_id, odometro_realizada, 
                                       data_realizada, proximo_odometro, proxima_data, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (viatura_id, tipo_id, odometro_atual, data_str, proximo_odometro, proxima_data_str, observacoes))
            
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False
    
    def listar_viaturas(self) -> List[Tuple]:
        """Lista todas as viaturas ativas"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT num_vtr, modelo, ano, orgao, odometro_atual, data_cadastro
            FROM viaturas 
            WHERE ativa = 1
            ORDER BY num_vtr
        ''')
        
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    
    def obter_alertas_manutencao(self, dias_antecedencia: int = 30, km_antecedencia: int = 500) -> List[Tuple]:
        """Obtém alertas de manutenções próximas do vencimento"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        data_limite = datetime.datetime.now() + datetime.timedelta(days=dias_antecedencia)
        data_limite_str = data_limite.strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            SELECT v.num_vtr, v.modelo, v.odometro_atual, tm.nome, 
                   m.proximo_odometro, m.proxima_data,
                   (m.proximo_odometro - v.odometro_atual) as km_restantes,
                   julianday(m.proxima_data) - julianday('now') as dias_restantes
            FROM manutencoes m
            JOIN viaturas v ON m.viatura_id = v.id
            JOIN tipos_manutencao tm ON m.tipo_manutencao_id = tm.id
            WHERE v.ativa = 1 
            AND (m.proxima_data <= ? OR (m.proximo_odometro - v.odometro_atual) <= ?)
            AND m.id IN (
                SELECT MAX(id) FROM manutencoes 
                WHERE viatura_id = m.viatura_id AND tipo_manutencao_id = m.tipo_manutencao_id
            )
            ORDER BY dias_restantes, km_restantes
        ''', (data_limite_str, km_antecedencia))
        
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    
    def obter_historico_viatura(self, num_vtr: str) -> dict:
        """Obtém o histórico completo de uma viatura"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Dados da viatura
        cursor.execute('SELECT * FROM viaturas WHERE num_vtr = ? AND ativa = 1', (num_vtr.upper(),))
        dados_viatura = cursor.fetchone()
        
        if not dados_viatura:
            conn.close()
            return {}
        
        viatura_id = dados_viatura[0]
        
        # Histórico de odômetro
        cursor.execute('''
            SELECT odometro, data_registro, observacoes
            FROM registros_odometro 
            WHERE viatura_id = ?
            ORDER BY data_registro DESC
            LIMIT 10
        ''', (viatura_id,))
        historico_odometro = cursor.fetchall()
        
        # Histórico de manutenções
        cursor.execute('''
            SELECT tm.nome, m.odometro_realizada, m.data_realizada, 
                   m.proximo_odometro, m.proxima_data, m.observacoes
            FROM manutencoes m
            JOIN tipos_manutencao tm ON m.tipo_manutencao_id = tm.id
            WHERE m.viatura_id = ?
            ORDER BY m.data_realizada DESC
        ''', (viatura_id,))
        historico_manutencoes = cursor.fetchall()
        
        conn.close()
        
        return {
            'viatura': dados_viatura,
            'odometro': historico_odometro,
            'manutencoes': historico_manutencoes
        }
    
    def listar_tipos_manutencao(self) -> List[Tuple]:
        """Lista todos os tipos de manutenção disponíveis"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT nome, intervalo_km, intervalo_dias, descricao FROM tipos_manutencao ORDER BY intervalo_km')
        resultado = cursor.fetchall()
        conn.close()
        return resultado


def imprimir_cabecalho():
    """Imprime o cabeçalho do sistema"""
    print("=" * 61)
    print("RASTREIA+".center(61))
    print("Gerenciamento de frota para órgãos governamentais e militares")
    print("=" * 61)


def imprimir_menu():
    """Imprime o menu principal"""
    print("\n" + "=" * 40)
    print("              MENU PRINCIPAL")
    print("=" * 40)
    print("1. Cadastrar Nova Viatura")
    print("2. Atualizar Odômetro")
    print("3. Registrar Manutenção")
    print("4. Listar Viaturas")
    print("5. Ver Alertas de Manutenção")
    print("6. Histórico de Viatura")
    print("7. Tipos de Manutenção")
    print("0. Sair")
    print("=" * 40)


def cadastrar_viatura_menu(sistema):
    """Menu para cadastrar nova viatura"""
    print("\n--- CADASTRAR NOVA VIATURA ---")
    
    num_vtr = input("Número da viatura: ").strip().upper()
    if not num_vtr:
        print("Número da viatura é obrigatório!")
        return
    
    modelo = input("Modelo da viatura: ").strip()
    if not modelo:
        print("Modelo é obrigatório!")
        return
    
    try:
        ano = int(input("Ano da viatura: "))
        if ano < 1990 or ano > datetime.datetime.now().year + 1:
            print("Ano inválido!")
            return
    except ValueError:
        print("Ano deve ser um número!")
        return
    
    orgao = input("Órgão (ex: Polícia Militar, Bombeiros): ").strip()
    if not orgao:
        print("Órgão é obrigatório!")
        return
    
    try:
        odometro = int(input("Odômetro atual (0 se novo): ") or "0")
        if odometro < 0:
            print("Odômetro não pode ser negativo!")
            return
    except ValueError:
        print("Odômetro deve ser um número!")
        return
    
    if sistema.cadastrar_viatura(num_vtr, modelo, ano, orgao, odometro):
        print(f"Viatura {num_vtr} cadastrada com sucesso!")
    else:
        print(f"Erro ao cadastrar viatura. Número {num_vtr} já existe!")


def atualizar_odometro_menu(sistema):
    """Menu para atualizar odômetro"""
    print("\n--- ATUALIZAR ODÔMETRO ---")
    
    num_vtr = input("Número da viatura: ").strip().upper()
    if not num_vtr:
        print("Número da viatura é obrigatório!")
        return
    
    try:
        novo_odometro = int(input("Novo odômetro: "))
        if novo_odometro < 0:
            print("Odômetro não pode ser negativo!")
            return
    except ValueError:
        print("Odômetro deve ser um número!")
        return
    
    observacoes = input("Observações (opcional): ").strip()
    
    if sistema.atualizar_odometro(num_vtr, novo_odometro, observacoes):
        print(f"Odômetro da viatura {num_vtr} atualizado para {novo_odometro:,} km!")
    else:
        print("Erro ao atualizar odômetro. Verifique se o número da viatura existe e o novo valor é válido!")


def registrar_manutencao_menu(sistema):
    """Menu para registrar manutenção"""
    print("\n--- REGISTRAR MANUTENÇÃO ---")
    
    # Listar tipos de manutenção
    tipos = sistema.listar_tipos_manutencao()
    print("\nTipos de manutenção disponíveis:")
    for i, (nome, km, dias, desc) in enumerate(tipos, 1):
        print(f"{i}. {nome} - {desc}")
    
    try:
        escolha = int(input(f"\nEscolha o tipo (1-{len(tipos)}): "))
        if escolha < 1 or escolha > len(tipos):
            print("Opção inválida!")
            return
        tipo_escolhido = tipos[escolha - 1][0]
    except ValueError:
        print("Opção deve ser um número!")
        return
    
    num_vtr = input("Número da viatura: ").strip().upper()
    if not num_vtr:
        print("Número da viatura é obrigatório!")
        return
    
    observacoes = input("Observações (opcional): ").strip()
    
    # Permitir ao usuário informar a data da manutenção (apenas data, formato DD/MM/YYYY)
    data_input = input("Data da manutenção (Enter para hoje): ").strip()
    if data_input:
        try:
            data_manutencao = datetime.datetime.strptime(data_input, "%d/%m/%Y")
        except ValueError:
            print("Data inválida! Use o formato DD/MM/YYYY.")
            return
    else:
        data_manutencao = datetime.datetime.now()
    
    if sistema.registrar_manutencao(num_vtr, tipo_escolhido, data_manutencao, observacoes):
        print(f"Manutenção '{tipo_escolhido}' registrada para viatura {num_vtr}!")
    else:
        print("Erro ao registrar manutenção. Verifique se o número da viatura existe!")


def listar_viaturas_menu(sistema):
    """Menu para listar viaturas"""
    print("\n--- LISTA DE VIATURAS ---")
    
    viaturas = sistema.listar_viaturas()
    
    if not viaturas:
        print("Nenhuma viatura cadastrada!")
        return
    
    print(f"\n{'Nº Viatura':<12} {'Modelo':<20} {'Ano':<6} {'Órgão':<20} {'Odômetro':<12} {'Cadastro':<12}")
    print("-" * 84)
    
    for num_vtr, modelo, ano, orgao, odometro, data_cadastro in viaturas:
        data_fmt = datetime.datetime.strptime(data_cadastro, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
        print(f"{num_vtr:<12} {modelo:<20} {ano:<6} {orgao:<20} {odometro:>8,} km  {data_fmt:<12}")


def ver_alertas_menu(sistema):
    """Menu para ver alertas de manutenção"""
    print("\n--- ALERTAS DE MANUTENÇÃO ---")
    
    alertas = sistema.obter_alertas_manutencao()
    
    if not alertas:
        print("Nenhum alerta de manutenção!")
        return
    
    print(f"\n{'Nº Viatura':<12} {'Modelo':<20} {'Manutenção':<20} {'Km Rest.':<10} {'Dias Rest.':<12} {'Status'}")
    print("-" * 87)
    
    for num_vtr, modelo, odometro_atual, manutencao, proximo_odo, proxima_data, km_rest, dias_rest in alertas:
        if dias_rest <= 0 or km_rest <= 0:
            status = "🔴 VENCIDO"
        elif dias_rest <= 14 or km_rest <= 250:
            status = "🟠 URGENTE"
        else:
            status = "🟡 ATENÇÃO"
        
        km_rest_str = f"{int(km_rest):,}" if km_rest > 0 else "0"
        dias_rest_str = f"{int(dias_rest)}" if dias_rest > 0 else "0"
        
        print(f"{num_vtr:<12} {modelo:<20} {manutencao:<20} {km_rest_str:<10} {dias_rest_str:<12} {status}")


def historico_viatura_menu(sistema):
    """Menu para ver histórico de viatura"""
    print("\n--- HISTÓRICO DE VIATURA ---")
    
    num_vtr = input("Número da viatura: ").strip().upper()
    if not num_vtr:
        print("Número da viatura é obrigatório!")
        return
    
    historico = sistema.obter_historico_viatura(num_vtr)
    
    if not historico:
        print(f"Viatura {num_vtr} não encontrada!")
        return
    
    # Dados da viatura
    viatura = historico['viatura']
    print(f"\nDADOS DA VIATURA {num_vtr}")
    print(f"Modelo: {viatura[2]}")
    print(f"Ano: {viatura[3]}")
    print(f"Órgão: {viatura[4]}")
    print(f"Odômetro Atual: {viatura[5]:,} km")
    
    # Histórico de odômetro
    print(f"\nHISTÓRICO DE ODÔMETRO (últimos 10 registros)")
    if historico['odometro']:
        print(f"{'Odômetro':<12} {'Data':<12} {'Observações'}")
        print("-" * 50)
        for odometro, data, obs in historico['odometro']:
            data_fmt = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
            obs_fmt = obs[:30] + "..." if obs and len(obs) > 30 else (obs or "")
            print(f"{odometro:>8,} km  {data_fmt:<12} {obs_fmt}")
    else:
        print("Nenhum registro de odômetro encontrado.")
    
    # Histórico de manutenções
    print(f"\n🔧 HISTÓRICO DE MANUTENÇÕES")
    if historico['manutencoes']:
        print(f"{'Manutenção':<20} {'Realizada':<12} {'Próxima':<12} {'Próx. Km':<10}")
        print("-" * 60)
        for nome, odo_real, data_real, prox_odo, prox_data, obs in historico['manutencoes']:
            data_real_fmt = datetime.datetime.strptime(data_real, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
            prox_data_fmt = datetime.datetime.strptime(prox_data, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
            print(f"{nome:<20} {data_real_fmt:<12} {prox_data_fmt:<12} {prox_odo:>8,}")
    else:
        print("Nenhuma manutenção registrada.")


def tipos_manutencao_menu(sistema):
    """Menu para listar tipos de manutenção"""
    print("\n--- TIPOS DE MANUTENÇÃO ---")
    
    tipos = sistema.listar_tipos_manutencao()
    
    print(f"\n{'Manutenção':<25} {'Intervalo KM':<12} {'Intervalo Dias':<15} {'Descrição'}")
    print("-" * 80)
    
    for nome, km, dias, desc in tipos:
        print(f"{nome:<25} {km:>8,} km   {dias:>10} dias    {desc}")


def main():
    """Função principal do sistema"""
    imprimir_cabecalho()
    
    # Inicializar sistema
    try:
        sistema = SistemaGerenciamentoFrota()
        print("Sistema inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar sistema: {e}")
        return
    
    while True:
        imprimir_menu()
        
        try:
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "0":
                print("\nObrigado por usar o Sistema de Gerenciamento de Frota!")
                break
            elif opcao == "1":
                cadastrar_viatura_menu(sistema)
            elif opcao == "2":
                atualizar_odometro_menu(sistema)
            elif opcao == "3":
                registrar_manutencao_menu(sistema)
            elif opcao == "4":
                listar_viaturas_menu(sistema)
            elif opcao == "5":
                ver_alertas_menu(sistema)
            elif opcao == "6":
                historico_viatura_menu(sistema)
            elif opcao == "7":
                tipos_manutencao_menu(sistema)
            else:
                print("Opção inválida! Tente novamente.")
            
            if opcao != "0":
                input("\nPressione Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\nSistema encerrado pelo usuário!")
            break
        except Exception as e:
            print(f"\nErro inesperado: {e}")
            input("Pressione Enter para continuar...")


if __name__ == "__main__":
    main()