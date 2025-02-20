import os
import shutil
import csv
import ast

def remove_changed_methods(root_dir='.'):
    """
    Remove todas as pastas chamadas "changed-methods" a partir do diretório root_dir.
    """
    for current_root, dirs, files in os.walk(root_dir, topdown=False):
        for d in dirs:
            if d == "changed-methods":
                full_path = os.path.join(current_root, d)
                shutil.rmtree(full_path)
                print(f"Removido: {full_path}")

def process_csv(csv_file="results-with-build-information.csv"):
    """
    Processa cada linha do CSV e cria as pastas/arquivos conforme especificado.
    """
    with open(csv_file, newline='', encoding='utf-8') as file:
        leitor = csv.reader(file, delimiter=';')
        for row in leitor:
            # Se a linha estiver vazia ou for o header, pula
            if not row or row[0] == "project":
                continue

            # Extração dos valores (OBS1)
            project = row[0]
            merge_commit = row[1]
            className = row[2]
            method = row[3]
            left_modifications_str = row[4]
            right_modifications_str = row[7]

            # Converte as strings de listas para listas de inteiros
            try:
                left_modifications = ast.literal_eval(left_modifications_str)
            except Exception:
                left_modifications = []
            try:
                right_modifications = ast.literal_eval(right_modifications_str)
            except Exception:
                right_modifications = []

            # Construção dos caminhos (OBS2: "changed-methods" é literal)
            project_path = os.path.join(project)
            merge_commit_path = os.path.join(project_path, merge_commit)
            changed_methods_path = os.path.join(merge_commit_path, "changed-methods")
            class_path = os.path.join(changed_methods_path, className)
            method_path = os.path.join(class_path, method)

            # Cria as pastas necessárias
            os.makedirs(method_path, exist_ok=True)

            # Caminhos dos arquivos a serem criados
            left_right_file = os.path.join(method_path, "left-right-lines.csv")
            right_left_file = os.path.join(method_path, "right-left-lines.csv")

            # Criação do arquivo "left-right-lines.csv"
            with open(left_right_file, "w", encoding="utf-8") as lr_file:
                # 6.1 para cada valor da coluna "left modifications": className, sink, valor
                for valor in left_modifications:
                    lr_file.write(f"{className},sink,{valor}\n")
                # 6.2 para cada valor da coluna "right modifications": className, source, valor
                for valor in right_modifications:
                    lr_file.write(f"{className},source,{valor}\n")

            # Criação do arquivo "right-left-lines.csv"
            with open(right_left_file, "w", encoding="utf-8") as rl_file:
                # 7.1 para cada valor da coluna "left modifications": className, source, valor
                for valor in left_modifications:
                    rl_file.write(f"{className},source,{valor}\n")
                # 7.2 para cada valor da coluna "right modifications": className, sink, valor
                for valor in right_modifications:
                    rl_file.write(f"{className},sink,{valor}\n")

            print(f"Processado: {project}/{merge_commit}/{className}/{method}")

def main():
    # OBS4: Remove todas as pastas "changed-methods" antes de iniciar
    remove_changed_methods()

    # Processa o arquivo CSV
    process_csv()

if __name__ == '__main__':
    main()
