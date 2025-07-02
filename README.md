# RASTREIA+ — Sistema de Gerenciamento de Frota

## 📋 Descrição
Sistema desenvolvido para órgãos governamentais e militares (Polícia Militar, Civil, Federal, Corpo de Bombeiros, etc.) para gerenciamento completo de frotas de viaturas.

## 🎯 Objetivo
Protótipo para seminário acadêmico demonstrando uma solução tecnológica que pode beneficiar serviços comunitários através do controle eficiente de manutenções de viaturas.
Desenvolvido para a disciplina de **Prática Profissional e Inserção Comunitária** do curso de Ciência da Computação da Unoesc Videira.

## ⚡ Funcionalidades

### 🚗 Gestão de Viaturas
- **Cadastro completo** de viaturas (nº, modelo, ano, órgão)
- **Controle de odômetro** com histórico de atualizações

### 🔧 Controle de Manutenções
- **6 tipos de manutenção pré-configurados**:
    - Revisão Geral (10.000 km ou 180 dias)
    - Troca de Óleo (10.000 km ou 1 ano)
    - Troca de Filtro de Ar (10.000 km ou 1 ano)
    - Revisão de Freios (20.000 km ou 1 ano)
    - Troca de Pneus (40.000 km ou 3 anos)
    - Troca de Bateria (60.000 km ou 4 anos)

### 🚨 Sistema de Alertas
- **Alertas automáticos** para manutenções próximas do vencimento
- **Códigos de cor** para priorização:
    - 🔴 **VENCIDO** - Manutenção já passou do prazo
    - 🟠 **URGENTE** - Vence em até 7 dias ou 100 km
    - 🟡 **ATENÇÃO** - Vence em até 30 dias ou 500 km

### 📊 Relatórios e Histórico
- **Histórico completo** de cada viatura
- **Listagem** de todas as viaturas ativas
- **Rastreamento** de atualizações de odômetro
- **Registro** de todas as manutenções realizadas

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python** - Linguagem principal
- **SQLite** - Banco de dados local integrado

### Características Técnicas
- ✅ **Banco SQLite integrado** - Sem configuração externa
- ✅ **Interface CLI intuitiva** - Fácil operação
- ✅ **Código bem estruturado** - Manutenção simplificada

## 🚀 Como Executar

### Pré-requisitos
- Python 3 (preferencialmente no path)
- Nenhuma biblioteca externa necessária (apenas bibliotecas padrão do Python)

### Execução
```bash
python3 main.py
```

### Primeiro Uso
1. Execute o programa
2. Escolha a opção **1** para cadastrar uma viatura
3. Preencha os dados solicitados
4. Use a opção **2** para atualizar o odômetro regularmente
5. Use a opção **3** para registrar manutenções realizadas
6. Monitore os alertas através da opção **5**

## 📱 Interface do Sistema

### Menu Principal
```
==========================================
              MENU PRINCIPAL
==========================================
1. Cadastrar Nova Viatura
2. Atualizar Odômetro
3. Registrar Manutenção
4. Listar Viaturas
5. Ver Alertas de Manutenção
6. Histórico de Viatura
7. Tipos de Manutenção
0. Sair
==========================================
```

## 💡 Casos de Uso

### Para Gestores
- **Visão geral** de toda a frota
- **Alertas proativos** para manutenções
- **Relatórios** para tomada de decisão

### Para Operadores
- **Cadastro simples** de viaturas
- **Atualização rápida** de odômetro
- **Registro fácil** de manutenções
- **Consulta de histórico** detalhado

## 🏆 Benefícios para a Comunidade

### Eficiência Operacional
- **Redução de custos** com manutenções preventivas
- **Maior disponibilidade** das viaturas
- **Planejamento** melhor de recursos

### Segurança Pública
- **Viaturas sempre** em condições adequadas
- **Resposta mais rápida** a emergências
- **Confiabilidade** do equipamento

### Transparência
- **Histórico completo** de manutenções
- **Controle** de gastos públicos e prestação de contas facilitada

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais
- **viaturas** - Dados básicos das viaturas
- **registros_odometro** - Histórico de odômetro
- **tipos_manutencao** - Tipos de manutenção disponíveis
- **manutencoes** - Manutenções realizadas

### Arquivo Gerado
- **frota.db** - Banco SQLite criado automaticamente

## 🔍 Exemplo de Uso Prático

1. **Cadastrar viatura**: Viatura PM-0001, Hilux 2023, Polícia Militar
2. **Atualizar odômetro**: Semanalmente, conforme uso
3. **Receber alerta**: Sistema avisa quando manutenção está próxima
4. **Registrar manutenção**: Após realizada, registrar no sistema
5. **Acompanhar histórico**: Visualizar todo o histórico da viatura

## 🎓 Aplicação Acadêmica

Este protótipo demonstra:
- **Aplicação prática** da programação
- **Solução de problemas reais** da sociedade
- **Uso de banco de dados** em projetos
- **Interface amigável** ao usuário

## 📈 Possíveis Expansões

### Funcionalidades Futuras
- Interface web responsiva
- Integração com APIs de oficinas
- Notificações automáticas por email/SMS
- Dashboard com gráficos e métricas
- Integração com sistemas GPS
- Controle de combustível
- Gestão de motoristas

---

**Desenvolvido para o Seminário de Ciência da Computação**  
*Demonstrando como a tecnologia pode servir à comunidade*
