import os
import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

# Inicializa o Faker com seed fixa para garantir reprodutibilidade
fake = Faker('pt_BR')
Faker.seed(42)
random.seed(42)

# Configuração de caminhos
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../../data/synthetic")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Parâmetros de geração
NUM_CUSTOMERS = 100
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 10, 1)


def generate_customers():
    """Gera a tabela de clientes (CRM B2B) com diferentes segmentos e perfis de comportamento."""
    segments = ['Enterprise', 'Mid-Market', 'SMB']
    industries = ['SaaS', 'Varejo', 'Logística', 'Financeiro', 'Indústria', 'Saúde']
    status_list = ['Ativo', 'Ativo', 'Ativo', 'Ativo', 'Churned']

    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        customer_id = f"CUST-{i:04d}"
        company_name = fake.company()
        segment = random.choice(segments)
        industry = random.choice(industries)
        created_at = fake.date_time_between(start_date=START_DATE, end_date=datetime(2025, 6, 1))

        # Atribui perfis de risco controlados para testes do AI Copilot
        # 15% das contas terão perfil de risco explícito (queda de receita)
        risk_profile = 'Normal'
        if i % 7 == 0:
            risk_profile = 'Risco Churn'
        elif i % 10 == 0:
            risk_profile = 'Potencial Expansão'

        customers.append({
            "customer_id": customer_id,
            "company_name": company_name,
            "segment": segment,
            "industry": industry,
            "status": random.choice(status_list),
            "risk_profile": risk_profile,
            "created_at": created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    df = pd.DataFrame(customers)
    df.to_csv(os.path.join(OUTPUT_DIR, "customers_raw.csv"), index=False)
    print(f"✅ {len(df)} clientes gerados em customers_raw.csv")
    return df


def generate_orders(customers_df):
    """Gera o histórico de pedidos e faturamento (ERP)."""
    orders = []
    order_id_counter = 1

    products = [
        {"name": "Plano Software Pro", "price": 1500.0},
        {"name": "Plano Software Enterprise", "price": 4500.0},
        {"name": "Consultoria de Implantação", "price": 8000.0},
        {"name": "Suporte Premium 24/7", "price": 2000.0},
        {"name": "Treinamento de Equipe", "price": 3000.0}
    ]

    for _, customer in customers_df.iterrows():
        cust_id = customer['customer_id']
        risk_profile = customer['risk_profile']
        cust_created = datetime.strptime(customer['created_at'], '%Y-%m-%d %H:%M:%S')

        # Controla a frequência de compras com base no perfil simulado
        if risk_profile == 'Risco Churn':
            # Parou de comprar nos últimos 90 dias
            max_order_date = END_DATE - timedelta(days=90)
            num_orders = random.randint(2, 5)
        elif risk_profile == 'Potencial Expansão':
            # Compras constantes e crescentes recentemente
            max_order_date = END_DATE
            num_orders = random.randint(10, 20)
        else:
            max_order_date = END_DATE
            num_orders = random.randint(3, 12)

        for _ in range(num_orders):
            order_date = fake.date_time_between(start_date=cust_created, end_date=max_order_date)
            product = random.choice(products)
            quantity = random.randint(1, 3)
            amount = product['price'] * quantity

            orders.append({
                "order_id": f"ORD-{order_id_counter:06d}",
                "customer_id": cust_id,
                "product_name": product['name'],
                "quantity": quantity,
                "total_amount": amount,
                "status": random.choice(['Concluído', 'Concluído', 'Concluído', 'Cancelado']),
                "order_date": order_date.strftime('%Y-%m-%d %H:%M:%S')
            })
            order_id_counter += 1

    df = pd.DataFrame(orders)
    df.to_csv(os.path.join(OUTPUT_DIR, "orders_raw.csv"), index=False)
    print(f"✅ {len(df)} pedidos gerados em orders_raw.csv")
    return df


def generate_interactions(customers_df):
    """Gera interações comerciais e registros de atendimento (Atendimento / Suporte)."""
    interactions = []
    interaction_id_counter = 1

    channels = ['Email', 'Reunião Teams', 'Telefone', 'Ticket Chamado']
    sentiments = ['Positivo', 'Neutro', 'Negativo']

    topics_negative = [
        "Reclamação sobre lentidão no sistema e bugs recorrentes.",
        "Cliente insatisfeito com atraso no suporte técnico.",
        "Solicitação de cancelamento por falta de ROI percebido.",
        "Questionamento sobre aumento de preço na renovação."
    ]

    topics_positive = [
        "Cliente elogiou o suporte e pediu proposta para mais licenças.",
        "Reunião trimestral de alinhamento com feedback muito bom.",
        "Interesse em contratar o módulo Enterprise no próximo mês.",
        "Solicitação de demo de novas funcionalidades."
    ]

    topics_neutral = [
        "Dúvida sobre emissão de nota fiscal do último pedido.",
        "Atualização dos contatos do time comercial no cadastro.",
        "Envio de material educativo sobre o produto."
    ]

    for _, customer in customers_df.iterrows():
        cust_id = customer['customer_id']
        risk_profile = customer['risk_profile']

        num_interactions = random.randint(2, 8)
        for _ in range(num_interactions):
            date = fake.date_time_between(start_date=START_DATE, end_date=END_DATE)

            if risk_profile == 'Risco Churn':
                sentiment = 'Negativo' if random.random() < 0.7 else 'Neutro'
                notes = random.choice(topics_negative)
            elif risk_profile == 'Potencial Expansão':
                sentiment = 'Positivo' if random.random() < 0.7 else 'Neutro'
                notes = random.choice(topics_positive)
            else:
                sentiment = random.choice(sentiments)
                notes = random.choice(topics_positive if sentiment == 'Positivo' else (topics_negative if sentiment == 'Negativo' else topics_neutral))

            interactions.append({
                "interaction_id": f"INT-{interaction_id_counter:06d}",
                "customer_id": cust_id,
                "channel": random.choice(channels),
                "sentiment": sentiment,
                "notes": notes,
                "created_at": date.strftime('%Y-%m-%d %H:%M:%S')
            })
            interaction_id_counter += 1

    df = pd.DataFrame(interactions)
    df.to_csv(os.path.join(OUTPUT_DIR, "interactions_raw.csv"), index=False)
    print(f"✅ {len(df)} interações geradas em interactions_raw.csv")
    return df


def generate_opportunities(customers_df):
    """Gera o pipeline de oportunidades comerciais (CRM Pipeline)."""
    opportunities = []
    opp_id_counter = 1

    stages = ['Qualificação', 'Proposta Enviada', 'Negociação', 'Fechado Ganho', 'Fechado Perdido']

    for _, customer in customers_df.iterrows():
        cust_id = customer['customer_id']
        risk_profile = customer['risk_profile']

        # Potencial de expansão gera oportunidades abertas maiores
        num_opps = random.randint(1, 3)
        for _ in range(num_opps):
            created = fake.date_time_between(start_date=datetime(2026, 1, 1), end_date=END_DATE)
            stage = random.choice(stages)

            if risk_profile == 'Potencial Expansão':
                val = round(random.uniform(15000.0, 50000.0), 2)
            else:
                val = round(random.uniform(2000.0, 15000.0), 2)

            opportunities.append({
                "opportunity_id": f"OPP-{opp_id_counter:05d}",
                "customer_id": cust_id,
                "title": f"Expansão - {customer['company_name']}",
                "stage": stage,
                "estimated_value": val,
                "created_at": created.strftime('%Y-%m-%d %H:%M:%S')
            })
            opp_id_counter += 1

    df = pd.DataFrame(opportunities)
    df.to_csv(os.path.join(OUTPUT_DIR, "opportunities_raw.csv"), index=False)
    print(f"✅ {len(df)} oportunidades geradas em opportunities_raw.csv")
    return df


if __name__ == "__main__":
    print("🚀 Gerando conjunto de dados sintéticos para o Customer 360...")
    cust_df = generate_customers()
    generate_orders(cust_df)
    generate_interactions(cust_df)
    generate_opportunities(cust_df)
    print("\n✨ Todos os arquivos foram gerados com sucesso na pasta `data/synthetic/`!")
