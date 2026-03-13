
import streamlit as st
import pandas as pd
import numpy as np
import datetime

# 1. Configurare pagină
st.set_page_config(page_title="Project Tracker", page_icon="🚀", layout="wide")

# 2. Titlu și introducere
st.title("🚀 Dashboard Management Proiecte")
st.markdown("Monitorizează progresul task-urilor și performanța echipei în timp real.")

# 3. Generare date fictive
@st.cache_data
def load_project_data():
    proiecte = ['Website Nou', 'App Mobil', 'Campanie Marketing', 'Audit Securitate', 'Migrare Cloud']
    statusuri = ['In Progress', 'Completed', 'Backlog', 'Blocked']
    prioritati = ['High', 'Medium', 'Low']
    
    data = []
    for _ in range(100):
        start_date = datetime.date(2024, 1, 1) + datetime.timedelta(days=np.random.randint(0, 60))
        progres = np.random.randint(0, 101)
        # Un task "Completed" are mereu progres 100
        status = np.random.choice(statusuri)
        if status == 'Completed':
            progres = 100
            
        data.append({
            "Task": f"Task ID-{np.random.randint(1000, 9999)}",
            "Proiect": np.random.choice(proiecte),
            "Status": status,
            "Prioritate": np.random.choice(prioritati),
            "Progres (%)": progres,
            "Data Start": start_date,
            "Responsabil": np.random.choice(['Ana', 'Marius', 'Elena', 'Radu'])
        })
    return pd.DataFrame(data)

df = load_project_data()

# 4. Sidebar - Filtre
st.sidebar.header("🔍 Filtrează Datele")
selected_project = st.sidebar.multiselect(
    "Selectează Proiectele:",
    options=df['Proiect'].unique(),
    default=df['Proiect'].unique()
)

selected_status = st.sidebar.multiselect(
    "Status Task:",
    options=df['Status'].unique(),
    default=df['Status'].unique()
)

# Aplicare filtre
mask = df['Proiect'].isin(selected_project) & df['Status'].isin(selected_status)
filtered_df = df.loc[mask]

# 5. Randul de sus: KPI-uri
st.subheader("Indicatori Cheie")
c1, c2, c3, c4 = st.columns(4)

total_tasks = len(filtered_df)
avg_progress = filtered_df['Progres (%)'].mean()
completed_tasks = len(filtered_df[filtered_df['Status'] == 'Completed'])
blocked_tasks = len(filtered_df[filtered_df['Status'] == 'Blocked'])

c1.metric("Total Task-uri", total_tasks)
c2.metric("Progres Mediu", f"{avg_progress:.1f}%")
c3.metric("Finalizate", completed_tasks, delta=f"{completed_tasks/total_tasks:.1%}" if total_tasks > 0 else 0)
c4.metric("Blocate", blocked_tasks, delta_color="inverse")

st.divider()

# 6. Vizualizări
col_stanga, col_dreapta = st.columns(2)

with col_stanga:
    st.subheader("Distribuția Statusului")
    status_counts = filtered_df.groupby('Status').size().reset_index(name='Număr')
    st.bar_chart(status_counts.set_index('Status'))

with col_dreapta:
    st.subheader("Progresul pe Proiecte")
    project_progress = filtered_df.groupby('Proiect')['Progres (%)'].mean().reset_index()
    st.bar_chart(project_progress.set_index('Proiect'))

st.divider()

# 7. Tabel cu date
st.subheader("📋 Listă Detaliată Task-uri")
# Colorăm coloana de progres folosind st.column_config
st.dataframe(
    filtered_df,
    column_config={
        "Progres (%)": st.column_config.ProgressColumn(
            "Progres (%)",
            help="Cât de aproape este task-ul de finalizare",
            format="%d%%",
            min_value=0,
            max_value=100,
        ),
    },
    use_container_width=True,
    hide_index=True
)

