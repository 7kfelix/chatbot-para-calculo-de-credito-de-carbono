"""
Utilitários para IA (Gemini) - VERSÃO MELHORADA E CORRIGIDA
"""
import google.generativeai as genai
import json


SYSTEM_PROMPT = """
Você é o Carbon, uma assistente virtual brasileira, calorosa e especialista em sustentabilidade. 
Você conversa de forma natural, como uma amiga que quer ajudar.

Seu objetivo é coletar informações para calcular a pegada de carbono mensal do usuário, mas sem parecer um formulário. 
Seja empática, use emojis ocasionalmente, e adapte suas respostas ao tom do usuário.

Informações que você precisa coletar (faça de forma conversacional):
1. TRANSPORTE:
   - Tem carro? Se sim, qual combustível (gasolina, etanol ou diesel)?
   - Quantos km roda por mês aproximadamente?
   - Usa transporte público? Quantos km por mês?

2. ENERGIA EM CASA:
   - Consumo de eletricidade em kWh (está na conta de luz)
   - Um botijão de gás de 13kg costuma durar quanto tempo (meses ou dias) na sua casa?

IMPORTANTE:
- Seja flexível na ordem das perguntas
- Se o usuário der várias informações de uma vez, agradeça e peça o que ainda falta
- Use linguagem casual e brasileira
- Quando tiver TODOS os dados, pergunte: "Perfeito! Tenho tudo que preciso. Quer que eu gere seu relatório agora? 😊"
- Se o usuário fizer perguntas sobre sustentabilidade, responda educadamente antes de continuar
"""

# Modelo RÁPIDO para chat (já configurado com o system_prompt)
model_chat = genai.GenerativeModel(
    'gemini-2.5-flash', 
    system_instruction=SYSTEM_PROMPT
)

# Modelo POTENTE para o relatório
model_report = genai.GenerativeModel('gemini-2.5-pro')

def generate_ai_response(conversation_history, max_retries=3):
    """
    Gera resposta da IA (usando o modelo RÁPIDO)
    O modelo agora é 'global', não é mais criado aqui dentro.
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"💬 Tentativa {attempt} - Gerando resposta (Chat Rápido)...")
            
            response = model_chat.generate_content(conversation_history)
            
            print(f"✅ Resposta gerada")
            return response.text
            
        except Exception as e:
            print(f"❌ Tentativa {attempt} falhou: {e}")
            if attempt == max_retries:
                return "Desculpa, tive um problema técnico. Pode repetir? 😅"
    
    return None


def generate_report_text(calculation_results, user_data=None, max_retries=2):
    """
    Gera texto narrativo DETALHADO do relatório
    
    Args:
        calculation_results: dict com cálculos de CO2
        user_data: dict opcional com dados brutos do usuário
    """
    
    total_monthly = calculation_results['total_kg_co2e']
    total_annual = total_monthly * 12
    total_annual_tons = total_annual / 1000
    
    details = calculation_results['details_kg_co2e']
    transport = details.get('transporte', 0)
    energy = details.get('energia_eletrica', 0)
    gas = details.get('gas_cozinha', 0)
    
    # Prevenção de divisão por zero se o total for 0
    if total_monthly == 0:
        print("⚠️ Alerta: total_monthly é 0. Evitando divisão por zero.")
        total_monthly = 1 # Evita erro, percentuais ficarão 0
    
    # Calcular árvores e custos
    trees_needed = int(total_annual / 22)  # 1 árvore compensa ~22kg CO2/ano
    cost_min = total_annual_tons * 40
    cost_max = total_annual_tons * 60
    
    # Identificar maior categoria
    categories = {
        'Transporte': transport,
        'Energia Elétrica': energy,
        'Gás de Cozinha': gas
    }
    max_category = max(categories.items(), key=lambda x: x[1])
    
    # Contexto adicional do usuário (se disponível)
    # A lógica aqui está CORRETA. Ela vai exibir o valor fracionado
    # que foi calculado no seu código principal.
    user_context = ""
    if user_data:
        if user_data.get('km_carro', 0) > 0:
            fuel_type = user_data.get('tipo_combustivel', 'combustível')
            user_context += f"\n- Carro: {user_data['km_carro']} km/mês ({fuel_type})"
        if user_data.get('km_onibus', 0) > 0:
            user_context += f"\n- Ônibus: {user_data['km_onibus']} km/mês"
        if user_data.get('kwh_eletricidade', 0) > 0:
            user_context += f"\n- Energia: {user_data['kwh_eletricidade']} kWh/mês"
        if user_data.get('kg_gas_glp', 0) > 0:
            # Esta linha converte o KG/mês (ex: 6.5kg) de volta 
            # para "botijões/mês" (ex: 0.5) para exibição. Perfeito!
            botijoes = user_data['kg_gas_glp'] / 13
            user_context += f"\n- Gás: {botijoes:.1f} botijão(ões)/mês"
    
    report_prompt = f"""
Você é o Carbon. Crie um relatório COMPLETO, DETALHADO e PERSONALIZADO sobre pegada de carbono.

DADOS DO USUÁRIO:
Total mensal: {total_monthly:.2f} kg CO2e
Total anual: {total_annual:.2f} kg CO2e ({total_annual_tons:.2f} toneladas)
{user_context}

Distribuição:
- Transporte: {transport:.2f} kg CO2e ({(transport/total_monthly*100):.1f}%)
- Energia: {energy:.2f} kg CO2e ({(energy/total_monthly*100):.1f}%)
- Gás: {gas:.2f} kg CO2e ({(gas/total_monthly*100):.1f}%)

Categoria de maior impacto: {max_category[0]} ({max_category[1]:.2f} kg CO2e)

ESTRUTURA DO RELATÓRIO (COPIE EXATAMENTE):

## 🌱 Seu Relatório de Pegada de Carbono

Olá! Aqui está sua análise completa. Vamos construir um futuro mais verde juntos! 💚

### 📊 Resultado Total

**Mensal:** {total_monthly:.2f} kg CO2e  
**Anual:** {total_annual:.2f} kg CO2e ({total_annual_tons:.2f} toneladas)

### 🔍 Análise Detalhada por Categoria

[Análise detalhada de CADA categoria com percentuais e interpretação. Destaque a categoria de maior impacto ({max_category[0]}) e explique o porquê em 2-3 frases. Compare com médias nacionais (média Brasil: 400-500 kg CO2e/mês)]

### 💡 Dicas Personalizadas para Redução

[Dê 5-6 dicas ESPECÍFICAS baseadas nas categorias de maior impacto. Use formato de lista numerada com **negrito** no título da dica]

### 🌳 Como Compensar Sua Pegada de Carbono

Para compensar suas emissões, você pode investir em projetos de reflorestamento ou comprar créditos de carbono certificados.

#### Árvores Necessárias

São necessárias **{trees_needed} árvores** para compensar sua emissão anual de {total_annual:.2f} kg CO2e.

**Melhores Espécies Nativas Brasileiras para Compensação:**

1. **Jequitibá (Cariniana legalis)** - Absorve até 50 toneladas de CO2 em 20 anos
2. **Ipê-roxo (Handroanthus impetiginosus)** - Absorve ~20 toneladas de CO2 em 20 anos
3. **Pau-brasil (Paubrasilia echinata)** - Absorve ~15 toneladas de CO2 em 20 anos
4. **Aroeira (Myracrodruon urundeuva)** - Resistente e de crescimento rápido
5. **Jatobá (Hymenaea courbaril)** - Árvore longeva, até 14 toneladas de CO2

**Recomendação:** Plante um mix de espécies nativas da sua região para melhor biodiversidade.

#### Organizações Parceiras

**1. 🌳 SOS Mata Atlântica** [Link: https://www.sosma.org.br](https://www.sosma.org.br)  
📞 Tel: (11) 3055-7888 | 📧 Email: atendimento@sosma.org.br  
Fundação desde 1986, líder em projetos de reflorestamento da Mata Atlântica. Plantio de mudas nativas com monitoramento via GPS.  
💰 Custo: R$ 30-50 por tonelada CO2

**2. 🌱 Iniciativa Verde** [Link: https://www.iniciativaverde.org.br](https://www.iniciativaverde.org.br)  
📞 Tel: (11) 3063-2211 | 📧 Email: contato@iniciativaverde.org.br  
ONG desde 1997, foco em reflorestamento e educação ambiental. Certificação transparente e relatórios anuais.  
💰 Custo: R$ 40-60 por tonelada CO2

**3. 🌿 Moss.Earth (MCO2 Token)** [Link: https://moss.earth](https://moss.earth)  
📧 Email: contato@moss.earth  
Primeira plataforma brasileira de crédito de carbono tokenizado. Projetos REDD+ na Amazônia certificados por Verra.  
💰 Custo: R$ 50-80 por tonelada CO2

**4. 🌲 IBF - Instituto Brasileiro de Florestas** [Link: https://www.ibflorestas.org.br](https://www.ibflorestas.org.br)  
📞 Tel: (31) 3491-7430 | 📧 Email: contato@ibflorestas.org.br  
Projetos de reflorestamento desde 2009. Acompanhamento via GPS e certificados personalizados.  
💰 Custo: R$ 35-55 por tonelada CO2

**5. 🍃 Biofílica Ambipar Environment** [Link: https://www.biofilica.com.br](https://www.biofilica.com.br)  
📞 Tel: (11) 3093-4400 | 📧 Email: contato@biofilica.com.br  
Desenvolvedora de projetos REDD+ na Amazônia. Certificação Gold Standard e parceria com grandes empresas.  
💰 Custo: R$ 45-70 por tonelada CO2

#### 💰 Investimento Estimado

**Compensação Mensal:** R$ {cost_min/12:.2f} a R$ {cost_max/12:.2f}

**Compensação Anual:** R$ {cost_min:.2f} a R$ {cost_max:.2f}

### 🎯 Próximos Passos

1. **Reduza primeiro:** Implemente as dicas de redução acima
2. **Escolha uma organização:** Compare projetos e certificações
3. **Invista em compensação:** Plante árvores ou compre créditos
4. **Monitore anualmente:** Refaça o cálculo e acompanhe sua evolução
5. **Compartilhe:** Inspire amigos e família a também medirem sua pegada

---

**Lembre-se:** A melhor compensação é REDUZIR emissões primeiro, depois compensar o restante. Cada ação conta! 🌱💚

REGRAS:
- COPIE a estrutura EXATAMENTE
- Use ## para título principal, ### para subtítulos
- Use **negrito** em títulos e nomes importantes
- Máximo 600 palavras
- Tom brasileiro, técnico mas acessível
- Links devem estar em formato Markdown [texto](url)
- Emojis: 🌱 💚 🌳 📊 🔍 💡 🎯 📞 📧 💰
"""
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"⏳ Tentativa {attempt} - Gerando relatório (Modelo Potente)...")
            
            # Usamos o 'model_report' global
            text = model_report.generate_content(report_prompt).text.strip()
            
            print(f"✅ Relatório gerado ({len(text)} caracteres)")
            return text
        except Exception as e:
            print(f"❌ Falha ao gerar relatório: {e}")
            if attempt == max_retries:
                # Sua função de fallback é uma ótima ideia!
                return generate_simple_report(calculation_results, trees_needed, cost_min, cost_max)
    
    return "Relatório gerado!"


def generate_simple_report(calculation_results, trees_needed, cost_min, cost_max):
    """Relatório fallback detalhado caso a IA falhe"""
    total = calculation_results['total_kg_co2e']
    total_annual = total * 12
    details = calculation_results['details_kg_co2e']
    
    # Prevenção de divisão por zero
    if total == 0:
        total = 1
    
    transport = details.get('transporte', 0)
    energy = details.get('energia_eletrica', 0)
    gas = details.get('gas_cozinha', 0)
    
    return f"""## 🌱 Seu Relatório de Pegada de Carbono

### 📊 Resultado Total

**Mensal:** {total:.2f} kg CO2e  
**Anual:** {total_annual:.2f} kg CO2e ({total_annual/1000:.2f} toneladas)

### 🔍 Análise por Categoria

- **Transporte:** {transport:.2f} kg CO2e ({(transport/total*100):.1f}%)
- **Energia Elétrica:** {energy:.2f} kg CO2e ({(energy/total*100):.1f}%)
- **Gás de Cozinha:** {gas:.2f} kg CO2e ({(gas/total*100):.1f}%)

### 🌳 Compensação

**Árvores necessárias:** {trees_needed} árvores/ano

**Melhores espécies:**
1. Jequitibá - até 50 ton CO2/20 anos
2. Ipê-roxo - ~20 ton CO2/20 anos
3. Pau-brasil - ~15 ton CO2/20 anos

### 💰 Investimento

**Anual:** R$ {cost_min:.2f} a R$ {cost_max:.2f}

### 🌍 Organizações Parceiras

1. **SOS Mata Atlântica** - [sosma.org.br](https://www.sosma.org.br) - (11) 3055-7888
2. **Iniciativa Verde** - [iniciativaverde.org.br](https://www.iniciativaverde.org.br) - (11) 3063-2211
3. **Moss.Earth** - [moss.earth](https://moss.earth)
4. **IBF** - [ibflorestas.org.br](https://www.ibflorestas.org.br) - (31) 3491-7430
5. **Biofílica** - [biofilica.com.br](https://www.biofilica.com.br) - (11) 3093-4400

Cada ação conta! Reduza primeiro, depois compense. 💚"""