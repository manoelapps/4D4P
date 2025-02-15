from ninja import ModelSchema, Schema
from .models import Alunos
from typing import Optional
from datetime import date

class AlunosSchema(ModelSchema):
    class Meta:
        model = Alunos
        fields = ['nome', 'email', 'faixa', 'data_nascimento']

class ProgressoAlunoSchema(Schema):
    email: str
    nome: str
    faixa: str
    total_aulas: int
    aulas_necessarias_para_proxima_faixa: int

class AulasConcluidasSchema(Schema):
    qtd: Optional[int] = 1
    email_aluno: str 

class AlunoSchema(Schema):
    faixa: str
