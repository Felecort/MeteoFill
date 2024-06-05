

def edit_env_var(env_file, var_name, new_value):
    with open(env_file, 'r') as file:
        lines = file.readlines()

    # Находим индекс строки
    var_index = next((i for i, line in enumerate(lines) if line.startswith(f"{var_name}=")), None)

    if var_index is not None:
        lines[var_index] = f"{var_name}={new_value}\n"

        with open(env_file, 'w') as file:
            file.writelines(lines)


def validate_input():
    while True:
        user_input = input("Введите целое положительное число - частоту опроса метеостанции в секундах: ")
        try:
            number = int(user_input)
            if number <= 0:
                raise ValueError
            print(number)
            edit_env_var('.env', 'REQUEST_FREQUENCY', number)
            break
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите целое число - частоту опроса метеостанции в секундах.")


if __name__ == "__main__":
    validate_input()
