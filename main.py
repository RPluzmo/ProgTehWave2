import pandas as pd
import os
import glob
import mysql.connector

OUTPUT_DIR = 'migrations'
DB_NAME = 'wave_friend2' # Tavas datubāzes nosaukums

def generate_sql_migrations():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Izveidojam pašu galveno datubāzes bāzes failu (0000_create_database.sql)
    db_create_sql = f"""DROP DATABASE IF EXISTS {DB_NAME};
        CREATE DATABASE IF NOT EXISTS {DB_NAME}
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_unicode_ci;
        """
    db_file_path = os.path.join(OUTPUT_DIR, '0000_create_database.sql')
    with open(db_file_path, 'w', encoding='utf-8') as f:
        f.write(db_create_sql)
    print(f"  -> Izveidots DB bāzes fails: {db_file_path}")

    # 2. Lasām Excel failus 
    excel_faili = sorted(glob.glob("*.xlsx"))
    if not excel_faili:
        print("Kļūda: Nav atrasts neviens .xlsx fails!")
        return

    for fails in excel_faili:
        fails_bez_paplasinajuma = os.path.splitext(fails)[0]
        
        try:
            table_name = fails_bez_paplasinajuma.split('_create_')[1].replace('_table', '')
        except IndexError:
            table_name = fails_bez_paplasinajuma 

        df = pd.read_excel(fails, header=None)
        
        header_idx = -1
        for idx, row in df.iterrows():
            row_values = [str(val).strip() for val in row.values]
            if 'Column name' in row_values:
                header_idx = idx
                break
        
        if header_idx == -1:
            continue

        df.columns = df.iloc[header_idx].astype(str).str.strip()
        df = df.iloc[header_idx + 1:].reset_index(drop=True)

        sql_lines = []
        foreign_keys = []

        for _, row in df.iterrows():
            col_name = str(row.get('Column name', '')).strip()
            if not col_name or col_name.lower() in ['nan', 'none']:
                continue

            data_type = str(row.get('Data Type', '')).strip().upper()
            length = str(row.get('Length', '')).strip()
            is_nullable = str(row.get('Is Nullable', '')).strip().upper()
            default_val = str(row.get('Default Value', '')).strip()
            constraints = str(row.get('Constraints', '')).strip()

            sql_type = data_type
            if data_type == 'INTEGER': sql_type = 'INT'
            elif data_type == 'STRING': sql_type = 'VARCHAR'
            
            if length and length.lower() not in ['nan', 'none']:
                if data_type == 'ENUM':
                    enum_vals = [f"'{val.strip()}'" for val in length.split(',')]
                    sql_type = f"ENUM({', '.join(enum_vals)})"
                else:
                    try: sql_type = f"{sql_type}({int(float(length))})"
                    except: sql_type = f"{sql_type}({length})"

            null_sql = "NOT NULL" if is_nullable == 'NO' else ""

            extra_keywords = []
            all_flags = (default_val + " " + constraints).lower()
            if 'auto increment' in all_flags: extra_keywords.append("AUTO_INCREMENT")
            if 'primary key' in all_flags: extra_keywords.append("PRIMARY KEY")

            default_sql = ""
            if default_val and default_val.lower() not in ['nan', 'none', 'auto increment']:
                if default_val.upper() == 'CURRENT TIMESTAMP': default_sql = "DEFAULT CURRENT_TIMESTAMP"
                elif default_val.upper() == 'FALSE': default_sql = "DEFAULT FALSE"
                elif default_val.upper() == 'TRUE': default_sql = "DEFAULT TRUE"
                else: default_sql = f"DEFAULT '{default_val}'"

            extra_sql = " ".join(extra_keywords)
            col_def = f"    {col_name} {sql_type} {null_sql} {default_sql} {extra_sql}".strip()
            sql_lines.append(" ".join(col_def.split()))

            if 'fk to' in constraints.lower():
                try:
                    fk_part = constraints.lower().split('fk to ')[1]
                    ref_info = fk_part.split(' ')[0]
                    ref_table = ref_info.split('(')[0]
                    ref_col = ref_info.split('(')[1].replace(')', '')
                    fk_sql = f"    CONSTRAINT fk_{table_name}_{col_name} FOREIGN KEY ({col_name}) REFERENCES {ref_table}({ref_col}) ON DELETE CASCADE ON UPDATE CASCADE"
                    foreign_keys.append(fk_sql)
                except: pass

        # 3. Pievienojam USE datubaze; un DROP TABLE IF EXISTS
        all_lines = sql_lines + foreign_keys
        
        final_sql = f"USE {DB_NAME};\n\n"
        final_sql += f"DROP TABLE IF EXISTS {table_name};\n\n"
        final_sql += f"CREATE TABLE {table_name} (\n" + ",\n".join(all_lines) + "\n);\n"

        sql_filename = os.path.join(OUTPUT_DIR, f"{fails_bez_paplasinajuma}.sql")
        with open(sql_filename, 'w', encoding='utf-8') as f:
            f.write(final_sql)
        
        print(f"  -> Veiksmīgi ģenerēts: {sql_filename}")

def execute_migrations_to_db():
    print("\n" + "="*40)
    print("Mēģinu izpildīt migrācijas Laragon datubāzē...")
    
    try:
        # Pieslēdzamies MySQL serverim
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()

        # Nolasām visus tikko izveidotos failus pareizā secībā
        sql_faili = sorted(glob.glob(os.path.join(OUTPUT_DIR, "*.sql")))
        
        for fails in sql_faili:
            print(f"  Izpildu datubāzē: {os.path.basename(fails)}...")
            with open(fails, 'r', encoding='utf-8') as f:
                sql_teksts = f.read()
                
                # DROŠAIS RISINĀJUMS: Sadalām visu SQL tekstu pa atsevišķām komandām tur, kur ir semikols
                sql_komandas = sql_teksts.split(';')
                
                for komanda in sql_komandas:
                    komanda = komanda.strip() # Noņemam liekās atstarpes un tukšās rindas
                    if komanda:               # Ja komanda nav tukša, izpildām to
                        cursor.execute(komanda)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Datubāze un tabulas ir veiksmīgi izveidotas!")
        
    except Exception as kļūda:
        print(f"Datubāzes kļūda: {kļūda}")
        print("Pārliecinies, ka Laragon/MySQL ir ieslēgts!")

if __name__ == '__main__':
    print("Sāku ģenerēt SQL failus...\n" + "-"*40)
    generate_sql_migrations()
    
    # Šeit mēs izsaucam jauno funkciju, kas reāli uzbūvē datubāzi!
    execute_migrations_to_db()
    print("-" * 40 + "\nViss process ir pabeigts!")