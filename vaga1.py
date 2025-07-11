
import streamlit as st
import pandas as pd
import sqlite3

def main():
    # Conectar ou criar banco de dados
    conn = sqlite3.connect('cadastros.db')
    cursor = conn.cursor()

    # Criar tabela, se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trabalhadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        funcao TEXT,
        nome TEXT,
        contato TEXT
    )
    """)
    conn.commit()

    st.title("📋 Cadastro de Trabalhadores")

    # Formulário de cadastro
    st.subheader("Candidatos para vaga de...")
    funcao = st.selectbox("Você é candidato a vaga de?", ["pedreiro", "ajudante", "carpinteiro"])
    nome = st.text_input("Qual seu nome?")
    contato = st.text_input("Seu número para contato?")

    if st.button("Cadastrar"):
        if nome and contato:
            cursor.execute("INSERT INTO trabalhadores (funcao, nome, contato) VALUES (?, ?, ?)",
                           (funcao, nome, contato))
            conn.commit()
            st.success(f"{funcao.capitalize()} cadastrado com sucesso: Nome: {nome}, Contato: {contato}")
        else:
            st.warning("⚠ Por favor, preencha todos os campos!")

    # Visualizar cadastros
    st.subheader("👀 Lista de cadastrados")
    df = pd.read_sql_query("SELECT funcao, nome, contato FROM trabalhadores", conn)
    st.dataframe(df)

    # Campo de senha única
    st.subheader("🔑 Área restrita")
    master_password = st.text_input("Digite a senha:", type="password")

    if not df.empty:
        if st.button("📥 Baixar arquivo TXT"):
            if master_password == "1234":
                # Montar cabeçalho bonito centralizado
                titulo = "LISTA DE CADASTRADOS".center(52) + "\n"
                divisoria = "-"*52 + "\n"
                colunas = f"{'Função'.center(15)}|{'Nome'.center(20)}|{'Contato'.center(15)}\n"
                divisoria_meio = "-"*52 + "\n"

                txt_content = titulo + divisoria + colunas + divisoria_meio

                # Montar linhas de dados
                for row in df.itertuples(index=False):
                    linha = f"{row.funcao.ljust(15)}|{row.nome.ljust(20)}|{row.contato.ljust(15)}\n"
                    txt_content += linha

                txt_content += divisoria

                st.download_button(
                    label="Clique aqui para baixar o TXT",
                    data=txt_content,
                    file_name='cadastros.txt',
                    mime='text/plain'
                )
            else:
                st.error("❌ Senha incorreta.")
    else:
        st.info("Ainda não há cadastros para exportar.")

    # Botão para excluir registros (protegido pela mesma senha)
    if st.button("🗑 Excluir todos os registros"):
        if master_password == "1234":
            cursor.execute("DELETE FROM trabalhadores")
            conn.commit()
            st.success("✅ Todos os registros foram excluídos com sucesso!")
            st.experimental_rerun()
        else:
            st.error("❌ Senha incorreta.")

    conn.close()

if "_main_":
    main()