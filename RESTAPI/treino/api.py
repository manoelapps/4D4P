from ninja import Router
from ninja.errors import HttpError
from .schemas import AlunosSchema, ProgressoAlunoSchema, AulasConcluidasSchema, AlunoSchema
from .models import Alunos, AulasConcluidas
from datetime import date
from .graduacao import *
from typing import List
import math

treino_router = Router()

@treino_router.post('/', response={200: AlunosSchema})
def criar_aluno(request, aluno_schema: AlunosSchema):
    nome = aluno_schema.dict()['nome']
    email = aluno_schema.dict()['email']
    faixa = aluno_schema.dict()['faixa']
    data_nascimento = aluno_schema.dict()['data_nascimento']

    if Alunos.objects.filter(email=email).exists():
        raise HttpError(400, "E-mail já cadastrado.")

    aluno = Alunos(nome=nome, email=email, faixa=faixa, data_nascimento=data_nascimento)
    aluno.save()
    
    return aluno

@treino_router.get('/alunos/', response=List[AlunosSchema])
def listar_alunos(request):
    alunos = Alunos.objects.all()
    return alunos





@treino_router.get('/progresso_aluno/', response={200: ProgressoAlunoSchema})
def progresso_aluno(request, email_aluno: str):
    aluno = Alunos.objects.get(email=email_aluno)
    
    total_aulas_concluidas = AulasConcluidas.objects.filter(aluno=aluno).count()
    
    faixa_atual = aluno.get_faixa_display()
    
    n = order_belt.get(faixa_atual, 0)
  
    total_aulas_proxima_faixa = calcula_aulas_necessarios_proximo_nivel(n)

    total_aulas_concluidas_faixa = AulasConcluidas.objects.filter(aluno=aluno, faixa_atual=aluno.faixa).count()

    aulas_faltantes = max(total_aulas_proxima_faixa - total_aulas_concluidas_faixa, 0)

    return {
        'email': aluno.email,
        'nome': aluno.nome,
        'faixa': aluno.get_faixa_display(),
        'total_aulas': total_aulas_concluidas,
        'aulas_necessarias_para_proxima_faixa': aulas_faltantes
    }

@treino_router.post('/aulas_concluidas/', response={200: str})
def aulas_concluidas(request, aulas_concluidas: AulasConcluidasSchema):
    qtd = aulas_concluidas.dict()['qtd']
    email_aluno = aulas_concluidas.dict()['email_aluno']

    if qtd <= 0:
        raise HttpError(400, "Quantidade de aulas concluidas deve ser maior que zero.")

    aluno = Alunos.objects.get(email=email_aluno)

    for _ in range(qtd):
        ac = AulasConcluidas(
            aluno = aluno,
            faixa_atual = aluno.faixa
        )

        ac.save()

    return "Aulas concluidas registradas com sucesso."

@treino_router.put('/aluno_update/{aluno_id}', response={200: AlunosSchema})
def aluno_update(request, aluno_id: int, aluno_data: AlunosSchema):
    aluno = Alunos.objects.get(id=aluno_id)
    idade = date.today().year - aluno.data_nascimento.year

    if idade < 18 and aluno_data.dict()['faixa'] in ['A', 'R', 'M', 'P']:
        raise HttpError(400, "A idade do aluno precisa ser maior ou igual a 18 anos para receber essa Faixa.")
    for key, value in aluno_data.dict().items():
        if value:
            setattr(aluno, key, value)
    aluno.save()

    return aluno

@treino_router.put('/aluno_graduacao_update/{aluno_id}', response={200: AlunoSchema})
def aluno_graduacao_update(request, aluno_id: int, aluno_data: AlunoSchema):
    aluno = Alunos.objects.get(id=aluno_id)
    idade = date.today().year - aluno.data_nascimento.year

    if idade < 18 and aluno_data.dict()['faixa'] in ['A', 'R', 'M', 'P']:
        raise HttpError(400, "A idade do aluno precisa ser maior ou igual a 18 anos para receber essa Faixa.")
    for key, value in aluno_data.dict().items():
        if value:
            setattr(aluno, key, value)
    aluno.save()

    return aluno