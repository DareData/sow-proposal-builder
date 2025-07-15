import json
from config import settings, prompts
from proposal_builder.helpers import read_prompt
from proposal_builder.llm import create_llm

LLM = create_llm(settings)

def generate_proposal(data: dict) -> str:
    project_desc = generate_project_description(data)
    timeline_planning = generate_timeline_planning(data)
    stakeholders_and_team = generate_stakeholders_and_team(data)
    requirements = generate_requirements(data)
    work_agreement = generate_work_agreement(data)
    exc_summ = generate_executive_summary(data, project_desc)

    proposal = "\n".join([
        exc_summ,
        project_desc,
        timeline_planning,
        stakeholders_and_team,
        requirements,
        work_agreement
    ])
    return proposal

def generate_executive_summary(data: dict, description: str) -> str:
    executive_summary_dict = {
        "language": data["language"],
        "project description": description,
    }
    messages = [
        {"role": "system", "content": prompts.SYSTEM_PROMPT},
        {"role": "user", "content": prompts.EXECUTIVE_SUMMARY + json.dumps(executive_summary_dict) }
    ]
    response = LLM.chat.completions.create(
        model=settings.AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
    )
    return response.choices[0].message.content

def generate_project_description(data):
    fields = [
        "client_name",
        "language",
        "technology_focus",
        "general_description",
    ]
    selected_data = {k: v for k, v in data.items() if k in fields}
    content = prompts.PROJECT_DESCRIPTION + json.dumps(selected_data)
    if data["agentic_archetypes_guidelines"]=="Yes":
        content = content + "\n\n" + prompts.AGENTS_ARCHETYPES
    
    messages = [
        {"role": "system", "content": prompts.SYSTEM_PROMPT},
        {"role": "user", "content": content}
    ]
    response = LLM.chat.completions.create(
        model=settings.AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
    )
    final_response = response.choices[0].message.content
    if data["project_type"]=="Gen-OS":
            content = final_response + "\n\n" + "Improve the text above by taking into account the following" + "\n\n"+ prompts.GENOS + "\n\n"+ selected_data["language"]
            messages = [
                {"role": "system", "content": prompts.SYSTEM_PROMPT},
                {"role": "user", "content": content}
            ]
            response = LLM.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT,
                messages=messages,
            )
            final_response = response.choices[0].message.content
    
    return final_response

def generate_timeline_planning(data: dict) -> str:
    fields = [
        "language",
        "planning",
    ]
    selected_data = {k: v for k, v in data.items() if k in fields}
    type_of_project_dict = {
        "Gen-OS": prompts.TIMELINE_AND_PLANNING_GENOS,
        "Closed Project": prompts.TIMELINE_AND_PLANNING_CLOSED_PROJECT,
        "Co-Creation": prompts.TIMELINE_AND_PLANNING_COCREATION
    }
    messages = [
        {"role": "system", "content": prompts.SYSTEM_PROMPT},
        {"role": "user", "content": type_of_project_dict[data["project_type"]] + json.dumps(selected_data)}
    ]
    response = LLM.chat.completions.create(
        model=settings.AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
    )
    return response.choices[0].message.content

def generate_stakeholders_and_team(data: dict) -> str:
    fields = [
        "client_name",
        "language",
        "client_stakeholders",
        "daredata_team"
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

def generate_requirements(data: dict) -> str:
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

def generate_work_agreement(data: dict) -> str:
    work_agreement_dict_en = {
        "Closed Project": "Payment of 30% on acceptance of the proposal, payment of 70% at the end",
        "Gen-OS": "Setup: Payment of 30% on acceptance of the proposal, payment of 70% at the end\n\nRun: Monthly Payment / Annual Payment (5% discount)",
        "Co-Creation": "Payment based on work timesheets",
    }
    work_agreement_dict_pt = {
        "Closed Project": "Pagamento do 30% aquando da aceitação da proposta, 70% no final",
        "Gen-OS": "Setup: 30% aquando da aceitação da proposta, 70% no final\n\nRun: Pagamentos Mensais/ Anuais (5% desconto)",
        "Co-Creation": "Pagamento com base em timesheets",
    }

    text_pt = "\n\n".join([
        " ",
        "# 8. Condições Comerciais",
        "Acordo de trabalho",
        "Todo o trabalho será efetuado remotamente (preferencialmente).",
        " ",
        "Condições de pagamento",
        work_agreement_dict_pt[data["project_type"]],
        "Pagamento devido no prazo de 30 dias a contar da data de apresentação da fatura",
        "O IVA, se aplicável, deve ser aplicado a todos os valores da presente proposta",
        " ",
        "Validade",
        "A presente proposta é válida por 30 dias úteis",
        " ",
        "Todas as faturas deverão ser pagas à:",
        "Empresa: DareData, SA",
        "NIF: PT 515362166",
        "Endereço: AV FONTES PEREIRA MELO , 31 5 C LISBOA 1050-117 LISBOA"  
    ])
    
    text_en = "\n\n".join([
        " ",
        "# 8. Commercial Conditions",
        "Work agreement",
        "All the work will be done remotely.",
        " ",
        "Payment terms",
        work_agreement_dict_en[data['project_type']],
        "Payment due within 30 days of invoice issue date",
        "VAT, where applicable, should be applied to all figures in this proposal",
        " ",
        "Validity",
        "This proposal is valid for 30 working days",
        " ",
        "All bills should be paid to:",
        "Company: DareData, SA",
        "VAT Number: PT 515362166",
        "Address: AV FONTES PEREIRA MELO , 31 5 C LISBOA 1050-117 LISBOA"
    ])

    if data["language"] == "English":
        return text_en
    if data["language"] == "Portuguese":
        return text_pt
