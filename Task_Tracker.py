from datetime import datetime
from argparse import ArgumentParser
import json
from sys import argv

def WriteTaskToJson(tarefas : list, id_tarefa : int, descricao : str, horario_criada : str,  horario_atualizada : str):
    
    nova_tarefa = {}
    nova_tarefa["id"] = id_tarefa
    nova_tarefa["description"] = descricao
    nova_tarefa["status"] = "todo"
    nova_tarefa["createdAt"] = horario_criada
    nova_tarefa["updatedAt"] = horario_atualizada

    tarefas.insert(0, nova_tarefa)
    tarefas_json = json.dumps(tarefas)

    with open("Tasks.json", "w") as file:
        file.write(tarefas_json)

def TratamentoAdd(descricao : str, arg2 = None):
    if arg2 is not None:
        print("Erro, a operação 'add' deve receber apenas 1 argumento (a descrição da tarefa a ser adicionada)")
        return
    
    if descricao is None or not isinstance(descricao, str):
        print("Erro, a operação 'add' deve receber uma curta descrição textual da tarefa a ser adicionada")
        return
    
    with open("Tasks.json", 'r') as file:
        tarefas : list = json.load(file)

    horario_atual = str(datetime.now())

    if len(tarefas) > 0:
        ultima_tarefa : dict = tarefas[0]
        id_ultima_tarefa = int(ultima_tarefa['id'])
        id_nova_tarefa = id_ultima_tarefa + 1

    else:
        id_nova_tarefa = 1

    WriteTaskToJson(tarefas, id_nova_tarefa, descricao, horario_atual, horario_atual)

    print(f"Tarefa adicionada com sucesso. ID da tarefa = {id_nova_tarefa}")

def ExlcuiTarefaSeExistir(tarefas : list, copia_tarefas : list, ids_alteradas : dict, task_id : int):

    for i,tarefa in enumerate(tarefas):
        if tarefa["id"] == task_id:
            copia_tarefas.pop(i)
            ids_alteradas[task_id] = "Excluída"
            return True
        elif tarefa["id"] > task_id:
            copia_tarefas[i]["id"] -= 1
            data_alteracao = str(datetime.now())
            copia_tarefas[i]["updatedAt"] = data_alteracao
            ids_alteradas[tarefa["id"]+1] = copia_tarefas[i]["id"]
        else:
            break

    return False

def AvisoTarefasAlteradas(ids_alteradas : dict):
    print("Operação 'delete' realizada com sucesso. As seguintes alterações foram realizadas no arquivo de tarefas:")
    for id_antiga,id_atual in ids_alteradas.items():
        print(f"Tarefa {id_antiga} -> Tarefa {id_atual}")

def TratamentoDelete(task_id : int, arg2 = None):

    if arg2 is not None:
        print("Erro, a operação 'delete' deve receber apenas 1 argumento")
        return
    
    if task_id is None:
        print("Erro, é necessário declarar o id da tarefa a ser excluída (sempre será um número inteiro maior ou igual a 1)")
        return
    
    try:
        task_id = int(task_id)
    except ValueError:
        print("Erro, o argumento passado deve ser um número inteiro")
        return
    
    if task_id < 1:
        print("Erro, id de uma tarefa deve ser um valor inteiro maior ou igual a 1")
        return
    
    with open("Tasks.json", 'r') as file:
        tarefas : list = json.load(file)
        copia_tarefas = tarefas

    ids_alteradas = {}
    
    if ExlcuiTarefaSeExistir(tarefas, copia_tarefas, ids_alteradas, task_id):
        with open("Tasks.json", 'w') as file:
            copia_tarefas_json = json.dumps(copia_tarefas)
            file.write(copia_tarefas_json)
        AvisoTarefasAlteradas(ids_alteradas)
    else:
        print("Tarefa especificada não encontrada, nenhuma alteração realizada")

def ExisteTarefaASerListada(tarefas : list, estado_de_interesse : str | list):

    existe = False

    tarefas_de_interesse = []

    for tarefa in tarefas:
        if tarefa["status"] in estado_de_interesse:
            tarefas_de_interesse.append(tarefa)
            existe = True

    if tarefas_de_interesse:
        print("Listando todas as tarefas especificadas:")
        for tarefa in tarefas_de_interesse:
            print(tarefa)
    
    return existe

def TratamentoList(status : str, arg2 = None):

    if arg2 is not None:
        print("Erro, a operação 'list' deve receber apenas 1 ou nenhum argumento")
        return

    if status not in [None, "done", "todo", "in-progress"]:
        print("Erro, tipo de estado de terefa buscado inválido. Os estados válidos de uma terefa são 'done', 'todo' ou 'in-progress'")
        print("Também é válido não especificar um estado ao não passar argumentos para a operação list. Neste caso, todas as tarefas serão listadas")
        return
    
    with open("Tasks.json", "r") as file:
        tarefas = json.load(file)

    if status is None:
        estado_de_interesse = ["done", "todo", "in-progress"]
    else:
        estado_de_interesse = status
    
    if not ExisteTarefaASerListada(tarefas, estado_de_interesse):
        print("Não existem tarefas armazenadas com o estado de interesse")

def AtualizaTarefa(tarefas : list, task_id : int, dado_a_ser_atualizado : str, dado_atualizado : str):
    tarefa_a_ser_atualizada = tarefas[len(tarefas)-task_id]
    tarefa_a_ser_atualizada[dado_a_ser_atualizado] = dado_atualizado
    tarefa_a_ser_atualizada["updatedAt"] = str(datetime.now())
    tarefas[len(tarefas)-task_id] = tarefa_a_ser_atualizada
    return json.dumps(tarefas)

def TratamentoUpdate(task_id : int, descricao : str):

    if descricao is None or task_id is None:
        print("Erro, a operação 'update' deve receber 2 argumentos")
        return
    
    if not isinstance(descricao, str):
        print("Erro, segundo argumento deve ser uma curta descrição de tarefa")
    
    try:
        task_id = int(task_id)
    except ValueError:
        print("Erro, o primeiro argumento passado deve ser um número inteiro")
        return
    
    if task_id < 1:
        print("Erro, id de uma tarefa deve ser um valor inteiro maior ou igual a 1")
        return
    
    with open("Tasks.json", 'r') as file:
        tarefas : list = json.load(file)

    tarefas_json = AtualizaTarefa(tarefas, task_id, "description", descricao)

    with open("Tasks.json", 'w') as file:
        file.write(tarefas_json)

    print(f"descrição da tarefa {task_id} atualizada com sucesso")

def TratamentoMark(mark : str, task_id : int, arg2 = None):

    if arg2 is not None:
        print("Erro, operações do tipo 'mark' só podem ter 1 argumento")
        return
    
    if task_id is None:
        print("Erro, operações do tipo 'mark' devem ser passadas junto com 1 argumento")

    try:
        task_id = int(task_id)
    except ValueError:
        print("Erro, o argumento passado deve ser um número inteiro")
        return
    
    if task_id < 1:
        print("Erro, id de uma tarefa deve ser um valor inteiro maior ou igual a 1")
        return
    
    with open("Tasks.json", 'r') as file:
        tarefas : list = json.load(file)

    novo_estado = '-'.join(mark[5:].split('-'))

    tarefas_json = AtualizaTarefa(tarefas, task_id, "status", novo_estado)

    with open("Tasks.json", 'w') as file:
        file.write(tarefas_json)

    print(f"Status da tarefa {task_id} atualizado com sucesso")

def main():
    parser = ArgumentParser()
    parser.add_argument("op", help="Operação a ser realizada pelo Task_Tracker. ex: add -> adicionar nova tarefa; list -> listar as tarefas", type=str)
    parser.add_argument("arg1", nargs='?', default=None)
    parser.add_argument("arg2", nargs='?', default=None)
    args = parser.parse_args()

    op : str = args.op
    arg1 = args.arg1
    arg2 = args.arg2

    if len(argv) > 4:
        print("Erro, o programa recebeu mais argumentos do que o esperado")

    try:
        file = open("Tasks.json", "r")
    except FileNotFoundError:
        file = open("Tasks.json", "w")
        file.write("[]")
    finally:
        file.close()

    match op:
        case "add":
            TratamentoAdd(arg1, arg2)
            return
        case "delete":
            TratamentoDelete(arg1, arg2)
            return
        case "list":
            TratamentoList(arg1, arg2)
            return
        case "update":
            TratamentoUpdate(arg1, arg2)
            return
        case "mark-todo" | "mark-in-progress" | "mark-done":
            TratamentoMark(op, arg1, arg2)
            return
        case _:
            print("Nome de Operação inválido. São válidas as operações: add, update, delete, mark-[todo/in-progress/done], list")
            return

if __name__ == "__main__":
    main()