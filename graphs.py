import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.style as style
import pandas as pd

from utils import DATABASE_PATH, create_connection

NUM_PESSOAS = 153
style.use("fivethirtyeight")

db = create_connection(DATABASE_PATH)

linguas = pd.read_sql("SELECT * FROM linguas", db)

map_lingua = {
    "Português": "Português",
    "Inglês": "Inglês",
    "Alemão": "Alemão",
    "Francês": "Francês",
    "Espanhol": "Espanhol",
    "Portuguese": "Português",
    "Brazilian Portuguese": "Português",
    "English": "Inglês",
    "inglês": "Inglês",
    "ingles": "Inglês",
    "German": "Alemão",
    "French": "Francês",
    "Spanish": "Espanhol",
    "Epanhol": "Espanhol",
}

linguas["lingua"] = linguas["lingua"].map(map_lingua)

# PLOT 1.1
# Língua x Porcentagem de Pessoas que Falam a Língua
lingua_pct_falado = linguas["lingua"].value_counts().drop("Português")
lingua_pct_falado = 100 * lingua_pct_falado / NUM_PESSOAS
lingua_pct_falado.plot.bar()
plt.title("Línguas x Porcentagem de Pessoas que Falam")
plt.ylabel("Pessoas (%)")
plt.xticks(rotation=45)
plt.savefig("graphs/plot1_1.png", dpi=700, format="png", bbox_inches="tight")
plt.show()


# PLOT 1.2
# Língua x Porcentagem de Fluência
lingua_ingles = linguas.loc[linguas["lingua"] == "Inglês", "nivel"]
lingua_ingles_pct = 100 * lingua_ingles.value_counts(normalize=True)
lingua_ingles_pct.plot.pie(autopct="%.1f%%")
plt.ylabel("")
plt.title("Fluência em Inglês")
plt.savefig("graphs/plot1_2.png", dpi=700, format="png", bbox_inches="tight")
plt.show()


# PLOT 2
# Competência x Pessoas que Possuem
competencias = pd.read_sql("SELECT * FROM competencias", db)
top_competencias = competencias["competencia"].value_counts().head(30)

fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(top_competencias.index, top_competencias.values)
ax.set_title("Competências")
ax.invert_yaxis()
ax.tick_params(axis="y", labelsize=8)
plt.savefig("graphs/plot2.png", dpi=700, format="png", bbox_inches="tight")
plt.show()


# PLOT 3
# Interesse x Pessoas que Possuem
interesses = pd.read_sql("SELECT * FROM interesses", db)
top_interesses = interesses["interesse"].value_counts().head(30)

fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(top_interesses.index, top_interesses.values)
ax.set_title("Interesses")
ax.invert_yaxis()
ax.tick_params(axis="y", labelsize=8)
plt.savefig("graphs/plot3.png", dpi=700, format="png", bbox_inches="tight")
plt.show()


# PLOT 4
# Pessoas Empregadas ao Longo do Tempo
experiencias = pd.read_sql("SELECT * FROM experiencias", db)
experiencias["data_comeco"] = pd.to_datetime(experiencias["data_comeco"])
experiencias["data_fim"] = experiencias["data_fim"].str.replace(
    "atualmente", "2023-01-01"
)
experiencias["data_fim"] = pd.to_datetime(experiencias["data_fim"])

date_min = "2018-01-01"
date_max = "2023-01-01"
date_range = pd.date_range(date_min, date_max, freq="M")
date_employed = pd.DataFrame(date_range, columns=["data"])

num_employed = []
for data in date_employed["data"].values:
    employed = 0
    for row, df in experiencias.iterrows():
        if data > df["data_comeco"] and data < df["data_fim"]:
            employed += 1

    num_employed.append(employed)

date_employed["empregados"] = num_employed


fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(date_employed["data"], num_employed)

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator((1, 4, 7, 10)))
ax.xaxis.set_major_formatter(mdates.DateFormatter("\n%Y"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b"))

plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
plt.savefig("graphs/plot4.png", dpi=700, format="png", bbox_inches="tight")
ax.tick_params(axis="x", labelsize=4, labelrotation=30)
plt.show()


db.close()
