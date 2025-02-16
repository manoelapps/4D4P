import flet as ft
import requests
import warnings
warnings.simplefilter("ignore", DeprecationWarning)


# URL base da API – ajuste conforme necessário
API_BASE_URL = "http://localhost:8000/api"

def main(page: ft.Page):
    page.title = "Criar Aluno"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    nome_field = ft.TextField(label="Nome")
    email_field = ft.TextField(label="Email")
    faixa_field = ft.TextField(label="Faixa")
    data_nascimento_field = ft.TextField(label="Data de Nascimento (YYYY-MM-DD)")
    create_result = ft.Text()

    def create_aluno_click(e):
        payload = {
            "nome": nome_field.value,
            "email": email_field.value,
            "faixa": faixa_field.value,
            "data_nascimento": data_nascimento_field.value
        }

        response = requests.post(API_BASE_URL + "/", json=payload)
        

    create_button = ft.ElevatedButton(text="Criar Aluno", on_click=create_aluno_click)

    
    criar_aluno_tab = ft.Column(
        [
            nome_field,
            email_field,
            faixa_field,
            data_nascimento_field,
            create_button,
            create_result,
        ],
        scroll=True,
    )

    students_table = ft.DataTable(
        columns=[
            #ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Faixa")),
            ft.DataColumn(ft.Text("Data Nascimento")),
        ],
        rows=[],
    )
    list_result = ft.Text()

    def listar_alunos_click(e):
        try:
            response = requests.get(API_BASE_URL + "/alunos/")
            if response.status_code == 200:
                alunos = response.json()
                # Limpa as linhas anteriores
                students_table.rows.clear()
                for aluno in alunos:
                    row = ft.DataRow(
                        cells=[
                            #ft.DataCell(ft.Text(str(aluno.get("id", "")))),
                            ft.DataCell(ft.Text(aluno.get("nome", ""))),
                            ft.DataCell(ft.Text(aluno.get("email", ""))),
                            ft.DataCell(ft.Text(aluno.get("faixa", ""))),
                            ft.DataCell(ft.Text(aluno.get("data_nascimento", ""))),
                        ]
                    )
                    students_table.rows.append(row)
                list_result.value = f"{len(alunos)} alunos encontrados."
            else:
                list_result.value = f"Erro: {response.text}"
        except Exception as ex:
            list_result.value = f"Exceção: {ex}"
        page.update()

    list_button = ft.ElevatedButton(text="Listar Alunos", on_click=listar_alunos_click)
    listar_alunos_tab = ft.Column([students_table, list_result,list_button], scroll=True)

    email_aula_field = ft.TextField(label="Email do Aluno")
    qtd_field = ft.TextField(label="Quantidade de Aulas", value="1")
    aula_result = ft.Text()

    def marcar_aula_click(e):
        try:
            qtd = int(qtd_field.value)
            payload = {
                "qtd": qtd,
                "email_aluno": email_aula_field.value,
            }
            response = requests.post(API_BASE_URL + "/aulas_concluidas/", json=payload)
            if response.status_code == 200:
                # A API retorna uma mensagem de sucesso
                mensagem = response.json()  # pode ser uma string ou objeto
                aula_result.value = f"Sucesso: {mensagem}"
            else:
                aula_result.value = f"Erro: {response.text}"
        except Exception as ex:
            aula_result.value = f"Exceção: {ex}"
        page.update()

    aula_button = ft.ElevatedButton(text="Marcar Aula Realizada", on_click=marcar_aula_click)
    aula_tab = ft.Column([email_aula_field, qtd_field, aula_button, aula_result], scroll=True)

    def carregar_alunos(dropdown):
        if getattr(dropdown, "carregado", False):  
            return

        try:
            alunos = requests.get(API_BASE_URL + "/alunos/").json()
            dropdown.options = [
                ft.dropdown.Option(key=str(aluno["email"]), text=aluno["nome"])
                for aluno in alunos
            ]
            dropdown.value = None
            dropdown.carregado = True 
            dropdown.update()
        except Exception as e:
            print(f"Erro ao carregar alunos: {e}")
    email_progress_field = ft.Dropdown(
        label="Email do Aluno",
        options=[ft.dropdown.Option(key="-1", text="Carregar alunos...")],
        value="-1",
        on_focus=lambda e: carregar_alunos(email_progress_field),
        )
    progress_result = ft.Text()

    def consultar_progresso_click(e):
        try:
            email = email_progress_field.value
            response = requests.get(
                API_BASE_URL + "/progresso_aluno/", params={"email_aluno": email}
            )
            if response.status_code == 200:
                progress = response.json()
                progress_result.value = (
                    f"Nome: {progress.get('nome', '')}\n"
                    f"Email: {progress.get('email', '')}\n"
                    f"Faixa Atual: {progress.get('faixa', '')}\n"
                    f"Aulas Totais: {progress.get('total_aulas', 0)}\n"
                    f"Aulas necessárias para a próxima faixa: {progress.get('aulas_necessarias_para_proxima_faixa', 0)}"
                )
            else:
                progress_result.value = f"Erro: {response.text}"
        except Exception as ex:
            progress_result.value = f"Exceção: {ex}"
        page.update()

    progress_button = ft.ElevatedButton(text="Consultar Progresso", on_click=consultar_progresso_click)
    progresso_tab = ft.Column([email_progress_field, progress_button, progress_result], scroll=True)

    id_aluno_field_atualizar = ft.Dropdown(
        label="Escolha um aluno",
        options=[ft.dropdown.Option(key="-1", text="Carregar alunos...")],
        value="-1",
        on_focus=lambda e: carregar_alunos_dropdown(id_aluno_field_atualizar),
    )

    nome_update_field = ft.TextField(label="Novo Nome")
    email_update_field = ft.TextField(label="Novo Email")
    faixa_update_atualizar_field = ft.TextField(label="Nova Faixa")
    data_nascimento_update_field = ft.TextField(label="Nova Data de Nascimento (YYYY-MM-DD)")
    update_result_atualizar = ft.Text()
    #instrucao = ft.Text(value="Utilize essa pagina para Atualizar/Corrigir os dados do aluno", size=20, color=ft.colors.BLUE)

    def atualizar_aluno_click(e):
        try:
            aluno_id = id_aluno_field_atualizar.value  # Captura o valor selecionado
            if not aluno_id:
                update_result_atualizar.value = "Selecione um aluno no dropdown."
            else:
                aluno_id = int(aluno_id)  # Converte para inteiro
                payload = {}

                # Preenchendo os campos do payload
                if nome_update_field.value:
                    payload["nome"] = nome_update_field.value
                if email_update_field.value:
                    payload["email"] = email_update_field.value
                if faixa_update_atualizar_field.value:
                    payload["faixa"] = faixa_update_atualizar_field.value
                if data_nascimento_update_field.value:
                    payload["data_nascimento"] = data_nascimento_update_field.value

                # Enviando a requisição PUT para atualizar o aluno
                response = requests.put(API_BASE_URL + f"/aluno_update/{aluno_id}", json=payload)
            
            if response.status_code == 200:
                aluno = response.json()
                update_result_atualizar.value = f"Aluno atualizado: {aluno}"
            else:
                update_result_atualizar.value = f"Erro: {response.text}"
        except Exception as ex:
            update_result_atualizar.value = f"Exceção: {ex}"
        page.update()



    update_button = ft.ElevatedButton(text="Atualizar Aluno", on_click=atualizar_aluno_click)
    atualizar_tab = ft.Column(
        [
            id_aluno_field_atualizar,
            nome_update_field,
            email_update_field,
            faixa_update_atualizar_field,
            data_nascimento_update_field,
            update_button,
            update_result_atualizar,
            #instrucao
        ],
        scroll=True,
    )
    def carregar_alunos_dropdown(dropdown):
        if getattr(dropdown, "carregado", False):  # Se já carregou, não faz nada
            return

        try:
            alunos = requests.get(API_BASE_URL + "/alunos/").json()
            dropdown.options = [
                ft.dropdown.Option(key=str(aluno["id"]), text=aluno["nome"])
                for aluno in alunos
            ]
            dropdown.value = None  # Remove o placeholder após carregar os dados
            dropdown.carregado = True  # Marca como carregado
            dropdown.update()
        except Exception as e:
            print(f"Erro ao carregar alunos: {e}")

    id_aluno_field_faixa = ft.Dropdown(
        label="Escolha um aluno",
        options=[ft.dropdown.Option(key="-1", text="Carregar alunos...")],
        value="-1",
        on_focus=lambda e: carregar_alunos_dropdown(id_aluno_field_faixa),
    )
    faixa_update_fx_field = ft.TextField(label="Nova Faixa")
    update_faixa_result = ft.Text()

    def atualizar_faixa_aluno_click(e):
        try:
            aluno_id = id_aluno_field_faixa.value
            if not aluno_id:
                update_faixa_result.value = "ID do aluno é necessário."
            else:
                # Converte o ID para inteiro antes de enviar
                aluno_id = int(aluno_id)
                payload = {
                    "faixa": faixa_update_fx_field.value
                }
                response = requests.put(API_BASE_URL + f"/aluno_graduacao_update/{aluno_id}", json=payload)
                if response.status_code == 200:
                    update_faixa_result.value = "Nova faixa para o aluno atualizada com sucesso!"
                else:
                    update_faixa_result.value = f"Erro: {response.text}"
        except ValueError:
            update_faixa_result.value = f"{type(aluno_id)}ID do aluno deve ser um número válido."
        except Exception as ex:
            update_faixa_result.value = f"Exceção: {ex}"
        page.update()

    update_button = ft.ElevatedButton(text="Atualizar Faixa", on_click=atualizar_faixa_aluno_click)
    atualizar_faixa_tab = ft.Column(
        [
            id_aluno_field_faixa,
            faixa_update_fx_field,
            update_button,
            update_faixa_result,
        ],
        scroll=True,
    )

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Criar Aluno", content=criar_aluno_tab),
            ft.Tab(text="Listar Alunos", content=listar_alunos_tab),
            ft.Tab(text="Aula Realizada", content=aula_tab),
            ft.Tab(text="Progresso do Aluno", content=progresso_tab),
            ft.Tab(text="Atualizar Faixa", content=atualizar_faixa_tab),
            ft.Tab(text="Atualizar Aluno", content=atualizar_tab),
        ]
    )

    page.add(tabs)

if __name__ == "__main__":
    ft.app(target=main)
