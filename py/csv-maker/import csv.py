import csv

while True:
    # variables
    list_data = []
    first_row = []
    counter = 1

    # funcion que sirve para detectar int o str con respecto a los inputs
    # (no sé si en verdad es importante pero pues que vivan los tipos de datos)
    def detect_type(data):   
        try:
            data = int(data)
            return data
        except ValueError:
            return data

    # funcion para crear el archivo csv
    def create_csv(list):
        with open("csv_file.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(list)

    # information de lo que hace esta mondá
    print("Esto es un pequeño programa para automatizar la tarea de crear archivos csv, sirve como un panel     de 'copiar y pegar información' para evitar usar el código directamente")
    print   ("--------------------------------------------------------------------------------------------------")
    print("Para empezar debes escribir la primer fila, esta delimita la cantidad de informacion para las    demás filas, ya que bueno pues la primera fila tiene la información esencial como el nombre, apellido y    eso (explico para la mrd)")
    print   ("--------------------------------------------------------------------------------------------------")
    print("Para ir agregando palabras a la fila, solo añadelas al input y dale enter")
    print("Escribe 1 para terminar con la fila principal (osea no poner mas palabras)")
    print("Escribe 2 para terminar reiniciar el programa (por alguna equivocación)")
    print("Escribe 3 para terminar el programa (sin hacer nada)")
    print   ("--------------------------------------------------------------------------------------------------")
    print("Palabras agregadas para la primera fila:")
    print("No has agregado nada" if first_row == [] else first_row[0])

    # el input inicial
    data = input("(Primera fila) Columna 1: ")

    # bucle para escribir las columnas
    while data != "2" or data != "1":
        first_row.append(data)
        counter += 1

        print   ("--------------------------------------------------------------------------------------------------")
        print("Escribe 1 para terminar con la fila principal (osea no poner mas palabras)")
        print("Escribe 2 para terminar el programa")
        print   ("--------------------------------------------------------------------------------------------------")
        print("Palabras agregadas para la primera fila:")
        print("No has agregado nada" if first_row == [] else first_row)

        data = input(f"(primera fila) Columna {counter}: ")

        if data == "1" or data == "2":
            list_data.append(first_row)
            break
    
    # me dio pereza seguir comentando el codigo :/
    if data == "1":
        print   ("-------------------------------------------------------------------------------------------------")
        rows_data = input("Elige cuantas filas vas a hacer: ")

        for i in range(int(rows_data)):
            row_list = []

            for row in range(len(first_row)):
                row_data = input(f"Ingresa el valor de la fila {i+1} columna {row+1}: ")
                typeOf = detect_type(row_data)

                row_list.append(typeOf)

            list_data.append(row_list)

        print   ("-------------------------------------------------------------------------------------------------")
        print("Terminaste, archivo csv hecho, resultado:")

        create_csv(list_data)

        for i in range(len(list_data)):
            print(list_data[i])
        break

    elif data == "2":
        print   ("-------------------------------------------------------------------------------------------------")
        print("Reincio:")
        continue

    elif data == "3":
        print   ("-------------------------------------------------------------------------------------------------")
        print("Programa terminado")
        break