import json
from src.config import settings, prompts
from src.proposal_builder.helpers import read_prompt
from src.proposal_builder.llm import create_llm

LLM = create_llm(settings)

async def agenerate_proposal(data: dict) -> str:
    project_desc = await agenerate_project_description(data)
    timeline_planing = await agenerate_timeline_planing(data)
    stakeholders_and_team = await agenerate_stakeholders_and_team(data)
    requirements = await agenerate_requirements(data)
    work_agreement = await agenerate_work_agreement(data)
    exc_summ = await agenerate_executive_summary(data, project_desc)

    proposal = "\n".join([
        exc_summ,
        project_desc,
        timeline_planing,
        stakeholders_and_team,
        requirements,
        work_agreement
    ])
    return proposal

async def agenerate_executive_summary(data: dict, description: str) -> str:
    messages = [
        {"role": "system", "content": prompts.SYSTEM_PROMPT},
        {"role": "user", "content": prompts.EXECUTIVE_SUMMARY + description}
    ]
    response = LLM.chat.completions.create(
        model=settings.AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
    )
    return response.choices[0].message.content

async def agenerate_project_description(data):
    fields = [
        "client_name",
        "language",
        "main_goals",
        "technology_focus",
        "general_description",
        "planning",
    ]
    data = {k: v for k, v in data.items() if k in fields}
    messages = [
        {"role": "system", "content": prompts.SYSTEM_PROMPT},
        {"role": "user", "content": prompts.PROJECT_DESCRIPTION + json.dumps(data)}
    ]
    response = LLM.chat.completions.create(
        model=settings.AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
    )
    return response.choices[0].message.content

async def agenerate_timeline_planing(data: dict) -> str:
    type_of_project_dict = {
        "Gen-OS": prompts.TIMELINE_AND_PLANING_GENOS,
        "Closed Project": prompts.TIMELINE_AND_PLANING_CLOSED_PROJECT,
        "Co-Creation": prompts.TIMELINE_AND_PLANING_COCREATION
    }
    messages = [
        {"role": "system", "content": prompts.SYSTEM_PROMPT},
        {"role": "user", "content": type_of_project_dict[data["project_type"]] + data["planning"]}
    ]
    response = LLM.chat.completions.create(
        model=settings.AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
    )
    return response.choices[0].message.content

async def agenerate_stakeholders_and_team(data: dict) -> str:
    fields = [
        "client_name",
        "language",
        "client_stakeholders",
    ]
    data = {k: v for k, v in data.items() if k in fields}
    messages = [
        {"role": "system", "content": prompts.SYSTEM_PROMPT},
        {"role": "user", "content": prompts.STAKEHOLDERS_AND_TEAM + json.dumps(data)}
    ]
    response = LLM.chat.completions.create(
        model=settings.AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
    )
    return response.choices[0].message.content

async def agenerate_requirements(data: dict) -> str:
    fields = [
        "client_name",
        "language",
        "client_expectations",
    ]
    data = {k: v for k, v in data.items() if k in fields}
    messages = [
        {"role": "system", "content": prompts.SYSTEM_PROMPT},
        {"role": "user", "content": prompts.REQUIREMENTS_AND_PRICING + json.dumps(data)}
    ]
    response = LLM.chat.completions.create(
        model=settings.AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
    )
    return response.choices[0].message.content

async def agenerate_work_agreement(data: dict) -> str:
    work_agreement_dict_en = {
        "Closed Project": "Payment of 30% on acceptance of the proposal, payment of 70% at the end",
        "Gen-OS": """Setup: Payment of 30% on acceptance of the proposal, payment of 70% at the end
Run: Monthly Payment / Annual Payment (5% discount)""",
        "Co-creation": "Payment based on work timesheets",
    }
    work_agreement_dict_pt = {
        "Closed Project": "Pagamento do 30% aquando da aceitação da proposta, 70% no final",
        "Gen-OS": """Setup: 30% aquando da aceitação da proposta, 70% no final
Run: Pagamentos Mensais/ Anuais (5% desconto)""",
        "Co-creation": "Pagamento com base em timesheets",
    }

    text_pt = f"""
Acordo de trabalho
Todo o trabalho será efetuado remotamente (preferencialmente).

Condições de pagamento 
{work_agreement_dict_pt[data["project_type"]]}

Pagamento devido no prazo de 30 dias a contar da data de apresentação da fatura
O IVA, se aplicável, deve ser aplicado a todos os valores da presente proposta

Validade
A presente proposta é válida por 30 dias úteis


Todas as faturas deverão ser pagas à:
Empresa: DareData, SA 
NIF: PT 515362166
Endereço: AV FONTES PEREIRA MELO , 31 5 C LISBOA 1050-117 LISBOA
"""
    text_en = f"""
Work agreement
All the work will be done remotely.

Payment terms
{work_agreement_dict_en[data['project_type']]}
Payment due within 30 days of invoice issue date
VAT, where applicable, should be applied to all figures in this proposal

Start date
Not defined, up to 10 working days after acceptance of the proposal


All bills should be paid to:
Company: DareData, SA 
VAT Number: PT 515362166
Address: AV FONTES PEREIRA MELO , 31 5 C LISBOA 1050-117 LISBOA
"""
    if data["language"] == "English":
        return text_en
    if data["language"] == "Portuguese":
        return text_pt
