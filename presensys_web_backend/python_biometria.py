import serial
import psycopg2
import time

PORTA_ARDUINO = "COM7"
BAUD_RATE = 9600

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "biometrics",
    "user": "postgres",
    "password": "950915"
}


def conectar_banco():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn


def criar_tabelas(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pessoas (
                id SERIAL PRIMARY KEY,
                sensor_id INTEGER UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                ra TEXT NOT NULL,
                criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS registros (
                id SERIAL PRIMARY KEY,
                pessoa_id INTEGER NOT NULL REFERENCES pessoas(id),
                sensor_id INTEGER NOT NULL,
                registrado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
        """)


def salvar_pessoa(conn, sensor_id, nome, ra):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO pessoas (sensor_id, nome, ra)
            VALUES (%s, %s, %s)
            ON CONFLICT (sensor_id)
            DO UPDATE SET
                nome = EXCLUDED.nome,
                ra = EXCLUDED.ra
            RETURNING id;
        """, (sensor_id, nome, ra))

        pessoa_id = cur.fetchone()[0]

    print(f"Pessoa salva no banco: ID sensor {sensor_id} | Nome: {nome} | RA: {ra}")
    return pessoa_id


def registrar_presenca(conn, sensor_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, nome, ra
            FROM pessoas
            WHERE sensor_id = %s;
        """, (sensor_id,))

        pessoa = cur.fetchone()

        if pessoa is None:
            print(f"Digital ID {sensor_id} reconhecida no sensor, mas sem cadastro no banco.")
            return

        pessoa_id, nome, ra = pessoa

        cur.execute("""
            INSERT INTO registros (pessoa_id, sensor_id)
            VALUES (%s, %s)
            RETURNING registrado_em;
        """, (pessoa_id, sensor_id))

        data_hora = cur.fetchone()[0]

    print(f"Presenca registrada: {nome} | RA: {ra} | Data/hora: {data_hora}")


def limpar_banco(conn):
    print()
    print("As digitais foram apagadas do sensor biometrico.")
    confirmar = input("Deseja apagar tambem pessoas e registros do PostgreSQL? Digite SIM para confirmar: ")

    if confirmar.strip().upper() != "SIM":
        print("Banco de dados mantido.")
        print()
        return

    with conn.cursor() as cur:
        cur.execute("""
            TRUNCATE TABLE registros, pessoas RESTART IDENTITY CASCADE;
        """)

    print("Banco de dados limpo com sucesso.")
    print()


def enviar_para_arduino(ser, texto):
    texto = texto.replace(";", " ")
    ser.write((texto + "\n").encode("utf-8"))


def main():
    conn = conectar_banco()
    criar_tabelas(conn)

    print("Conectando ao Arduino...")
    ser = serial.Serial(PORTA_ARDUINO, BAUD_RATE, timeout=1)

    time.sleep(2)

    print("Sistema iniciado.")
    print("Nao abra o Monitor Serial da IDE junto com este programa.")
    print("Aperte o botao no Arduino para cadastrar uma digital.")
    print("Segure o botao de limpar por 5 segundos para apagar as digitais.")
    print()

    while True:
        linha = ser.readline().decode("utf-8", errors="ignore").strip()

        if not linha:
            continue

        print("[ARDUINO]", linha)

        if linha == "ASK_NOME":
            nome = input("Digite o nome da pessoa: ").strip()
            enviar_para_arduino(ser, nome)

        elif linha == "ASK_RA":
            ra = input("Digite o RA da pessoa: ").strip()
            enviar_para_arduino(ser, ra)

        elif linha.startswith("CADASTRO_OK;"):
            partes = linha.split(";", 3)

            if len(partes) == 4:
                sensor_id = int(partes[1])
                nome = partes[2]
                ra = partes[3]

                salvar_pessoa(conn, sensor_id, nome, ra)

        elif linha.startswith("PRESENCA;"):
            partes = linha.split(";")

            if len(partes) >= 2:
                sensor_id = int(partes[1])
                registrar_presenca(conn, sensor_id)

        elif linha == "LIMPEZA_OK":
            limpar_banco(conn)

        elif linha == "LIMPEZA_ERRO":
            print("O Arduino tentou apagar as digitais, mas ocorreu erro no sensor.")
            print("O banco de dados NAO foi apagado.")


if __name__ == "__main__":
    main()